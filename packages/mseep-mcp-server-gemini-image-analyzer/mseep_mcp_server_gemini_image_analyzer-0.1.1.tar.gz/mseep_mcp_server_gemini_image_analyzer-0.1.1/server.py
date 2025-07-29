import base64
import os
import logging
import sys
import tempfile
import json
from io import BytesIO
from typing import Optional, Any, Union, List

import PIL.Image
from google import genai
from google.genai import types
from mcp.server.fastmcp import FastMCP

from prompts import get_image_analysis_prompt, get_puzzle_validation_prompt

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("mcp-server-gemini-image-analyzer")


# ==================== Gemini API Interaction ====================

async def call_gemini(
    contents: List[Any], 
    model: str = "gemini-2.5-pro-exp-03-25", 
    config: Optional[types.GenerateContentConfig] = None
) -> str:
    """Call Gemini API with image and text for analysis.
    
    Args:
        contents: The content to send to Gemini. list containing text and/or images
        model: The Gemini model to use
        config: Optional configuration for the Gemini API call
        
    Returns:
        str: The text response from Gemini
        
    Raises:
        Exception: If there's an error calling the Gemini API
    """
    try:
        # Initialize Gemini client
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
            
        client = genai.Client(api_key=api_key)
        
        # Generate content using Gemini
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=config
        )
        
        logger.info(f"Response received from Gemini API using model {model}")
        
        return response.candidates[0].content.parts[0].text.strip()

    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}")
        raise


# ==================== Image Processing Functions ====================

async def save_temp_image_and_process(image: PIL.Image.Image, role: str) -> str:
    """Save image to temporary file and process with Gemini API.
    
    This approach is more efficient as it allows Gemini to process the file directly.
    
    Args:
        image: PIL Image object
        role: The analytical role for image analysis
        
    Returns:
        str: Analysis result from Gemini
    """
    try:
        # Create temp file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            temp_path = tmp_file.name
            
        # Save image to temp file
        image.save(temp_path)
        logger.info(f"Saved image to temporary file: {temp_path}")
        
        # Create analysis prompt
        analysis_prompt = get_image_analysis_prompt(role)
        
        # Process with file-based method which is more efficient
        source_image = PIL.Image.open(temp_path)
        
        # Call Gemini API with image and prompt
        analysis_result = await call_gemini(
            [analysis_prompt, source_image],
            model="gemini-2.5-pro-exp-03-25"
        )
        
        # Clean up temp file
        try:
            os.remove(temp_path)
            logger.info(f"Removed temporary file: {temp_path}")
        except Exception as e:
            logger.warning(f"Could not remove temporary file {temp_path}: {e}")
            
        return analysis_result
        
    except Exception as e:
        logger.error(f"Error in save_temp_image_and_process: {str(e)}")
        raise

async def load_image_from_base64(encoded_image: str) -> PIL.Image.Image:
    """Load an image from a base64-encoded string.
    
    Args:
        encoded_image: Base64 encoded image data with header
        
    Returns:
        PIL Image object
    """
    if not encoded_image.startswith('data:image/'):
        raise ValueError("Invalid image format. Expected data:image/[format];base64,[data]")
    
    try:
        # Extract the base64 data from the data URL
        image_format, image_data = encoded_image.split(';base64,')
        image_format = image_format.replace('data:', '')  # Get the MIME type e.g., "image/png"
        image_bytes = base64.b64decode(image_data)
        source_image = PIL.Image.open(BytesIO(image_bytes))
        logger.info(f"Successfully loaded image with format: {image_format}")
        return source_image
    except ValueError as e:
        logger.error(f"Error: Invalid image data format: {str(e)}")
        raise ValueError("Invalid image data format. Image must be in format 'data:image/[format];base64,[data]'")
    except base64.binascii.Error as e:
        logger.error(f"Error: Invalid base64 encoding: {str(e)}")
        raise ValueError("Invalid base64 encoding. Please provide a valid base64 encoded image.")
    except PIL.UnidentifiedImageError:
        logger.error("Error: Could not identify image format")
        raise ValueError("Could not identify image format. Supported formats include PNG, JPEG, GIF, WebP.")
    except Exception as e:
        logger.error(f"Error: Could not load image: {str(e)}")
        raise


# ==================== MCP Tools ====================

async def validate_puzzle_image(image: PIL.Image.Image) -> dict:
    """Validate if an image contains a mathematical puzzle.
    
    Args:
        image: PIL Image object
        
    Returns:
        dict: Validation results including is_puzzle, puzzle_type, confidence, etc.
    """
    try:
        # Create temp file for validation
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
            temp_path = tmp_file.name
            
        # Save image to temp file
        image.save(temp_path)
        
        # Get validation prompt
        validation_prompt = get_puzzle_validation_prompt()
        
        # Process with file-based method
        source_image = PIL.Image.open(temp_path)
        
        # Call Gemini API for validation
        validation_result = await call_gemini(
            [validation_prompt, source_image],
            model="gemini-2.5-pro-exp-03-25"
        )
        
        # Clean up temp file
        try:
            os.remove(temp_path)
        except Exception as e:
            logger.warning(f"Could not remove temporary file {temp_path}: {e}")
            
        # Parse the validation result
        try:
            result_dict = json.loads(validation_result)
            return result_dict
        except json.JSONDecodeError:
            logger.error("Failed to parse validation result as JSON")
            return {
                "is_puzzle": False,
                "puzzle_type": "none",
                "confidence": 0,
                "reasoning": "Failed to validate image format",
                "age_range": "none"
            }
            
    except Exception as e:
        logger.error(f"Error in validate_puzzle_image: {str(e)}")
        raise

@mcp.tool()
async def analyze_image(encoded_image: str, role: str = "puzzle expert") -> str:
    """Analyze an image using Google's Gemini 2.5 Pro model.

    Args:
        encoded_image: Base64 encoded image data with header.
        role: The type of analysis to perform. Default is "puzzle expert".
              Examples: "puzzle expert", "art expert", "fashion critic", "interior designer", 
                        "technical reviewer", "photography expert"
        
    Returns:
        Detailed analysis of the image in the specified style/role
    """
    try:
        logger.info(f"Processing analyze_image request with role: {role}")

        # Load and validate the image
        source_image = await load_image_from_base64(encoded_image)
        
        # If role is puzzle expert, validate the image first
        if "puzzle" in role.lower():
            validation_result = await validate_puzzle_image(source_image)
            
            if not validation_result["is_puzzle"]:
                return f"""This image does not appear to be a mathematical puzzle.

Reason: {validation_result['reasoning']}

For mathematical puzzle analysis, please provide an image that:
1. Contains clear mathematical elements (numbers, operations, patterns, shapes)
2. Is structured as a puzzle or problem to solve
3. Is appropriate for children's education
4. Has clear mathematical learning objectives

Type of image detected: {validation_result['puzzle_type']}
Confidence: {validation_result['confidence']}%"""
        
        # Process the image by saving to a temporary file first for better performance
        return await save_temp_image_and_process(source_image, role)
        
    except Exception as e:
        error_msg = f"Error analyzing image: {str(e)}"
        logger.error(error_msg)
        return error_msg

# Keep the original name for backward compatibility
@mcp.tool()
async def analyze_image_from_encoded(encoded_image: str, role: str = "puzzle expert") -> str:
    """Analyze an image using Google's Gemini model with a specified analysis style or role.

    Args:
        encoded_image: Base64 encoded image data with header. Must be in format:
                    "data:image/[format];base64,[data]"
                    Where [format] can be: png, jpeg, jpg, gif, webp, etc.
        role: The type of analysis to perform. Default is "puzzle expert".
              Examples: "puzzle expert", "art expert", "fashion critic", "interior designer", 
                        "technical reviewer", "photography expert"
        
    Returns:
        Detailed analysis of the image in the specified style/role
    """
    # Just call the main analyze_image function
    return await analyze_image(encoded_image, role)

@mcp.tool()
async def analyze_image_from_file(image_file_path: str, role: str = "art expert") -> str:
    """Analyze an image file using Google's Gemini model with a specified analysis style or role.

    Args:
        image_file_path: Path to the image file to be analyzed
        role: The type of analysis to perform. Default is "art expert".
              Examples: "art expert", "fashion critic", "interior designer", 
                        "technical reviewer", "photography expert"
        
    Returns:
        Detailed analysis of the image in the specified style/role
    """
    try:
        logger.info(f"Processing analyze_image_from_file request with role: {role}")
        logger.info(f"Image file path: {image_file_path}")

        # Validate file path
        if not os.path.exists(image_file_path):
            raise ValueError(f"Image file not found: {image_file_path}")
            
        # Load the source image directly using PIL
        try:
            source_image = PIL.Image.open(image_file_path)
            logger.info(f"Successfully loaded image from file: {image_file_path}")
        except PIL.UnidentifiedImageError:
            logger.error("Error: Could not identify image format")
            raise ValueError("Could not identify image format. Supported formats include PNG, JPEG, GIF, WebP.")
        except Exception as e:
            logger.error(f"Error: Could not load image: {str(e)}")
            raise 
        
        # Create analysis prompt
        analysis_prompt = get_image_analysis_prompt(role)
        
        # Call Gemini API with image and prompt
        analysis_result = await call_gemini(
            [analysis_prompt, source_image],
            model="gemini-2.5-pro-exp-03-25"
        )
        
        return analysis_result
        
    except Exception as e:
        error_msg = f"Error analyzing image: {str(e)}"
        logger.error(error_msg)
        return error_msg


@mcp.tool()
async def upload_and_analyze_image(image_data: str, role: str = "art expert") -> str:
    """Upload an image and analyze it using Google's Gemini model.
    
    This is the preferred method for image analysis as it processes the image
    directly from a file path for better performance.

    Args:
        image_data: Base64 encoded image data (can be with or without format header)
        role: The type of analysis to perform. Default is "art expert".
              Examples: "art expert", "fashion critic", "interior designer", 
                        "technical reviewer", "photography expert"
        
    Returns:
        Detailed analysis of the image in the specified style/role
    """
    try:
        logger.info(f"Processing upload_and_analyze_image request with role: {role}")
        
        # Check if image_data already has a header
        if not image_data.startswith('data:image/'):
            # Add a default header if missing
            image_data = f"data:image/png;base64,{image_data}"
        
        # Load the image
        source_image = await load_image_from_base64(image_data)
        
        # Process using the temp file method for better performance
        return await save_temp_image_and_process(source_image, role)
        
    except Exception as e:
        error_msg = f"Error analyzing uploaded image: {str(e)}"
        logger.error(error_msg)
        return error_msg


@mcp.tool()
async def execute_code_with_gemini(code_query: str) -> str:
    """Execute code or get code solutions using Gemini 2.5 Pro Preview with code execution capabilities.
    
    This tool allows you to:
    1. Get code solutions for programming problems
    2. Debug existing code
    3. Generate code with AI assistance
    4. Run and execute code to see results
    
    Args:
        code_query: Description of the code task or problem to solve
        
    Returns:
        Generated code and/or execution results from Gemini
    """
    try:
        logger.info(f"Processing code execution request: {code_query}")
        
        # Initialize Gemini client
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
            
        client = genai.Client(api_key=api_key)

        # Set up the model and tools
        model = "gemini-2.5-pro-preview-03-25"
        
        # Create contents with the user's query
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=code_query),
                ],
            ),
        ]
        
        # Enable code execution tool
        tools = [
            types.Tool(code_execution=types.ToolCodeExecution),
        ]
        
        # Configure the response
        generate_content_config = types.GenerateContentConfig(
            tools=tools,
            response_mime_type="text/plain",
        )

        # Collect the complete response
        complete_response = []
        
        # Stream the response
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                continue
                
            # Handle text output
            if chunk.candidates[0].content.parts[0].text:
                text_part = chunk.candidates[0].content.parts[0].text
                complete_response.append(text_part)
                
            # Handle executable code output
            if chunk.candidates[0].content.parts[0].executable_code:
                code_part = chunk.candidates[0].content.parts[0].executable_code
                complete_response.append(f"\n```python\n{code_part}\n```\n")
                
            # Handle code execution results
            if chunk.candidates[0].content.parts[0].code_execution_result:
                result_part = chunk.candidates[0].content.parts[0].code_execution_result
                complete_response.append(f"\nExecution Result:\n```\n{result_part}\n```\n")
        
        return "".join(complete_response)
        
    except Exception as e:
        error_msg = f"Error executing code with Gemini: {str(e)}"
        logger.error(error_msg)
        return error_msg


if __name__ == "__main__":
    logger.info("Starting Gemini Image Analyzer MCP server...")
    
    mcp.run(transport="stdio")

    logger.info("Server stopped")