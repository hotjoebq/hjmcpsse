# hjmcpsse

A Python MCP (Model Context Protocol) server with SSE (Server-Sent Events) transport.

## ⚠️ Important: Python Version Requirement

**This project requires Python 3.10 or higher.** The MCP package dependencies are not compatible with Python 3.9 or earlier versions.

If you're getting installation errors like:
```
ERROR: Could not find a version that satisfies the requirement mcp>=1.10.0 (from versions: none)
```

This means you're using Python 3.9 or earlier. See the [Troubleshooting](#troubleshooting) section below for upgrade instructions.

## Features

This MCP server provides:

- **Resource**: File system browser (`files://` URI scheme) for exploring directories and reading files
- **Tool**: Safe calculator for evaluating mathematical expressions
- **Prompt**: Code generator for creating structured prompts for code generation
- **Transport**: SSE (Server-Sent Events) for real-time communication

## Requirements

- **Python 3.10 or higher** (required for MCP package compatibility)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/hotjoebq/hjmcpsse.git
cd hjmcpsse
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
# or
pip install -r requirements.txt
```

## Usage

### Running the Server

Start the MCP server:
```bash
python -m hjmcpsse
```

Or with custom options:
```bash
python -m hjmcpsse --host localhost --port 8000 --log-level DEBUG
```

### VSCode Development

This project is configured for VSCode development:

1. Open the project in VSCode
2. Install the Python extension
3. Select the virtual environment as your Python interpreter
4. Use F5 to run/debug the server with the pre-configured launch settings

### Testing with mcp-cli

Once the server is running, you can test it using the `mcp-cli` tool:

#### Test the Resource (File System Browser)
```bash
# List current directory
mcp-cli tool read "files://." --server hjmcpsse

# List a specific directory
mcp-cli tool read "files:///home/user/Documents" --server hjmcpsse

# Read a file
mcp-cli tool read "files:///path/to/file.txt" --server hjmcpsse
```

#### Test the Calculator Tool
```bash
# Basic calculation
mcp-cli tool call calculator --server hjmcpsse --input '{"expression": "2 + 3 * 4"}'

# Complex expression with math functions
mcp-cli tool call calculator --server hjmcpsse --input '{"expression": "sqrt(16) + sin(pi/2)"}'

# Error handling
mcp-cli tool call calculator --server hjmcpsse --input '{"expression": "1 / 0"}'
```

#### Test the Code Generator Prompt
```bash
# Generate a Python function prompt
mcp-cli tool call code_generator --server hjmcpsse --input '{"description": "a function that sorts a list of numbers", "language": "python", "include_tests": true}'

# Generate a class prompt
mcp-cli tool call code_generator --server hjmcpsse --input '{"description": "a class for managing user accounts", "style": "object-oriented", "include_docs": true}'
```

#### Test the Template Tool
```bash
# Get a Python function template
mcp-cli tool call get_template --server hjmcpsse --input '{"language": "python", "template_type": "function"}'

# Get a Python class template
mcp-cli tool call get_template --server hjmcpsse --input '{"language": "python", "template_type": "class"}'
```

## MCP Client Configuration

To use this server with an MCP client, add the following configuration:

```json
{
  "servers": {
    "hjmcpsse": {
      "command": "python",
      "args": ["-m", "hjmcpsse"],
      "env": {}
    }
  }
}
```

For SSE transport specifically:
```json
{
  "servers": {
    "hjmcpsse": {
      "url": "http://localhost:8000/sse",
      "transport": "sse"
    }
  }
}
```

## Project Structure

```
hjmcpsse/
├── src/hjmcpsse/
│   ├── __init__.py
│   ├── __main__.py          # Entry point
│   ├── server.py            # Main MCP server
│   ├── resources/
│   │   ├── __init__.py
│   │   └── filesystem.py    # File system resource
│   ├── tools/
│   │   ├── __init__.py
│   │   └── calculator.py    # Calculator tool
│   └── prompts/
│       ├── __init__.py
│       └── code_generator.py # Code generation prompts
├── .vscode/
│   ├── launch.json          # VSCode debug configuration
│   └── settings.json        # VSCode settings
├── pyproject.toml           # Project configuration
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black src/
isort src/
```

### Type Checking
```bash
mypy src/
```

## Components

### File System Resource (`files://`)
- Browse directories and list contents
- Read text file contents
- Provides structured information about files and directories
- Handles permissions and error cases gracefully

### Calculator Tool
- Safely evaluates mathematical expressions
- Supports basic arithmetic operations (+, -, *, /, %, **)
- Includes functions like abs(), round(), min(), max(), sum()
- Advanced math functions: sqrt(), sin(), cos(), tan(), log(), exp()
- Mathematical constants: pi, e
- Comprehensive error handling for invalid expressions

### Code Generator Prompt
- Creates structured prompts for code generation
- Supports multiple programming languages
- Configurable code style preferences
- Optional inclusion of tests and documentation
- Provides helpful suggestions and best practices

### Template Tool
- Provides code templates for common patterns
- Supports functions, classes, and script templates
- Language-specific templates with proper structure

## Error Handling

The server includes comprehensive error handling:
- Invalid file paths and permissions
- Mathematical expression errors (division by zero, syntax errors)
- Network and transport errors
- Graceful degradation for unsupported operations

## Security

- File system access is read-only
- Calculator uses AST parsing for safe expression evaluation
- No arbitrary code execution
- Input validation and sanitization

## Troubleshooting

### Python Version Issues

**Problem**: Getting `ERROR: Could not find a version that satisfies the requirement mcp>=1.10.0`

**Cause**: You're using Python 3.9 or earlier, but the MCP package requires Python 3.10+.

**Solution**: Upgrade to Python 3.10 or higher:

#### Option 1: Use Python 3.10+ in VSCode (Recommended)
1. **Check available Python versions:**
   ```bash
   python3.10 --version || echo "Python 3.10 not found"
   python3.11 --version || echo "Python 3.11 not found" 
   python3.12 --version || echo "Python 3.12 not found"
   ```

2. **Create new virtual environment with Python 3.10+:**
   ```bash
   python3.10 -m venv venv_py310
   source venv_py310/bin/activate  # On Windows: venv_py310\Scripts\activate
   pip install --upgrade pip
   ```

3. **Select the new Python interpreter in VSCode:**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Python: Select Interpreter"
   - Choose the Python from your new `venv_py310/bin/python`

#### Option 2: Install Python 3.10+ on your system
```bash
# On Ubuntu/Debian:
sudo apt update && sudo apt install python3.10 python3.10-venv

# On macOS with Homebrew:
brew install python@3.10

# On Windows: Download from python.org
```

#### Option 3: Use pyenv (if available)
```bash
pyenv install 3.10.0
pyenv local 3.10.0
```

#### Verify the fix:
```bash
python --version  # Should show 3.10+
pip install -r requirements.txt
python -m hjmcpsse --help
```

### Network/Proxy Issues

If you have Python 3.10+ but still can't install the MCP package:

1. **Check PyPI connectivity:**
   ```bash
   curl -s https://pypi.org/simple/mcp/ | head -5
   ```

2. **Try installing with verbose output:**
   ```bash
   pip install -v mcp>=1.10.0
   ```

3. **Clear pip cache:**
   ```bash
   pip cache purge
   ```

## License

MIT License
