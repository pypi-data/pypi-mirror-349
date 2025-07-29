# MCP-Image-Analysis4Puzzle

A specialized MCP server that uses Gemini 2.5 Pro to analyze and solve mathematical puzzles for children's education.

## Overview

MCP-Image-Analysis4Puzzle is a dedicated server that helps teachers, parents, and students analyze mathematical puzzles through image processing. Using Google's Gemini 2.5 Pro model, it provides detailed, grade-appropriate analysis and solutions for various types of mathematical puzzles.

## Key Features

### Mathematical Subject Analysis
- Number Sense & Operations (counting, arithmetic, fractions)
- Geometry & Spatial Reasoning (shapes, patterns, transformations)
- Algebra & Early Functions (sequences, patterns, simple equations)
- Measurement & Data (time, money, graphs)
- Logic & Problem Solving (visual puzzles, word problems)

### Educational Support
- Grade-level appropriate analysis (K-6)
- Common Core Standards alignment
- Step-by-step solution guidance
- Visual learning aids suggestions
- Extension activities

### Smart Validation
- Automatic puzzle type detection
- Grade-level appropriateness check
- Mathematical content verification
- Learning objective identification

## Requirements

- Python 3.11 or higher
- Google Gemini API key
- MCP-compatible client (Cursor, Claude Desktop, etc.)
- Internet connection for API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/mcp-image-analysis4puzzle.git
cd mcp-image-analysis4puzzle
```

2. Set up a virtual environment:
```bash
# Using venv
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
.venv\Scripts\activate     # On Windows

# Or using uv (recommended)
uv venv
source .venv/bin/activate  # On Unix/macOS
.venv\Scripts\activate     # On Windows
```

3. Install dependencies:
```bash
# Using pip
pip install -r requirements.txt

# Or using uv (recommended)
uv pip install -r requirements.txt
```

4. Create and configure your environment file:
```bash
cp .env.example .env
```

5. Add your Gemini API key to `.env`:
```
GEMINI_API_KEY=your_api_key_here
```

## Configuration

### For Cursor IDE

The server is automatically configured when using Cursor IDE.

### For Claude Desktop

Add to your `claude_desktop_config.json`:

- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
    "mcpServers": {
        "mcp-image-analysis4puzzle": {
            "command": "uv",
            "args": [
                "--directory",
                "/path/to/mcp-image-analysis4puzzle",
                "run",
                "server.py"
            ],
            "env": {
                "GEMINI_API_KEY": "your_api_key_here"
            }
        }
    }
}
```

## Usage

1. Start your MCP-compatible client (Cursor or Claude Desktop)
2. Upload a mathematical puzzle image
3. Ask for analysis using commands like:
   - "Analyze this math puzzle for grade 2"
   - "Help solve this geometry puzzle"
   - "What math concepts are in this puzzle?"

### Example Analysis

When you upload a puzzle image, you'll receive:

```
PUZZLE ANALYSIS

Subject: Number Sense & Operations
Grade Level: 2nd Grade (7-8 years)
Topic: Skip Counting & Patterns

Mathematical Concepts:
- Pattern recognition
- Skip counting by 2s
- Number relationships
- Early multiplication concepts

Step-by-Step Solution:
1. Observe the number sequence
2. Identify the pattern
3. Apply the pattern rule
4. Verify the answer

Learning Standards:
- CCSS.MATH.CONTENT.2.OA.C.3
- CCSS.MATH.PRACTICE.MP7
- CCSS.MATH.PRACTICE.MP8

Visual Aids:
- Number line
- Counting objects
- Pattern blocks
- Drawing tools

Extension Activities:
1. Create similar patterns
2. Find patterns in real life
3. Connect to multiplication
4. Practice with different numbers
```

## Development

To run the server in development mode:

```bash
fastmcp dev server.py
```

This starts the server and makes the MCP Inspector available at http://localhost:5173

## Project Structure

```
mcp-image-analysis4puzzle/
├── server.py           # Main MCP server implementation
├── prompts.py         # Gemini prompt templates
├── utils.py           # Utility functions
├── requirements.txt   # Python dependencies
├── .env              # Environment configuration
└── README.md         # Documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Acknowledgments

- Google Gemini API
- FastMCP Framework
- Claude AI Platform
- Cursor IDE Team 