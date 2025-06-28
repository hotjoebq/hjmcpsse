# hjmcpsse MCP Server Testing Guide

This guide provides instructions for testing the hjmcpsse MCP (Model Context Protocol) server and its components.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ installed
- Virtual environment activated
- All dependencies installed (see `requirements.txt`)

### Project Structure
```
hjmcpsse/
├── src/
│   └── hjmcpsse/
│       ├── server.py           # Main MCP server
│       ├── tools/
│       │   └── calculator.py   # Calculator tool
│       ├── resources/
│       │   └── filesystem.py   # File system resource
│       └── prompts/
│           └── code_generator.py # Code generation prompts
├── test_client.py              # Test client
└── TESTING.md                  # This file
```

## 🛠️ Setup Instructions

### 1. Activate Virtual Environment
**Git Bash:**
```bash
cd /c/CDrive/Workshops/CustomAI/mcpsse
source venv_py312/Scripts/activate
```

**PowerShell:**
```powershell
cd "C:\CDrive\Workshops\CustomAI\mcpsse"
.\venv_py312\Scripts\Activate.ps1
```

### 2. Navigate to Project Directory
```bash
cd hjmcpsse
```

## 🧪 Testing Methods

### Method 1: Direct Component Testing (Recommended)

This method tests the underlying functions directly without MCP protocol overhead.

**Run the test client:**
```bash
python test_client.py
```

**What it tests:**
- ✅ Calculator tool with various expressions
- ✅ Filesystem resource (directory listing and file reading)
- ✅ Code generator prompts and templates
- ✅ Error handling for edge cases

### Method 2: MCP Server Testing

Start the MCP server and test it as a running service.

**Step 1: Start the Server**
```bash
cd src
python -m hjmcpsse --host localhost --port 8000
```

You should see:
```
Starting hjmcpsse MCP server with SSE transport on localhost:8000...
```

**Step 2: Test Server Status**
Open a new terminal and check if the server is running:
```bash
curl http://localhost:8000
```

## 🧮 Calculator Tool Tests

The calculator tool supports:

### Basic Operations
```python
# Test expressions
"2 + 3 * 4"          # Result: 14
"10 / 2 - 1"         # Result: 4.0
"2 ** 3"             # Result: 8
```

### Mathematical Functions
```python
# Advanced functions
"sqrt(16)"           # Result: 4.0
"sin(pi/2)"          # Result: 1.0
"cos(0)"             # Result: 1.0
"log(e)"             # Result: 1.0
"abs(-5)"            # Result: 5
```

### Error Handling
```python
# Error cases
"1 / 0"              # Error: Division by zero
"2 +* 3"             # Error: Invalid mathematical expression
"undefined_var"      # Error: Undefined variable
```

## 📁 Filesystem Resource Tests

The filesystem resource provides:

### Directory Listing
- Lists all directories and files in a given path
- Shows file sizes in KB
- Handles non-existent paths gracefully

### File Content Reading
- Reads text file contents
- Handles binary files appropriately
- Provides error messages for inaccessible files

## 💬 Code Generator Tests

The code generator provides:

### Prompt Generation
- Creates structured prompts for code generation
- Supports multiple programming languages
- Includes optional tests and documentation
- Provides helpful suggestions

### Code Templates
- Function templates
- Class templates
- Script templates
- Language-specific formatting

## 🔧 Troubleshooting

### Common Issues

**1. Module Not Found Errors**
```bash
# Ensure you're in the correct directory and virtual environment is activated
cd /c/CDrive/Workshops/CustomAI/mcpsse/hjmcpsse
source ../venv_py312/Scripts/activate
```

**2. Import Errors in test_client.py**
```bash
# Make sure you're running from the hjmcpsse directory
pwd  # Should show .../hjmcpsse
python test_client.py
```

**3. Server Won't Start**
```bash
# Check if virtual environment is activated
which python  # Should point to venv_py312

# Check if dependencies are installed
pip list | grep mcp
```

**4. Permission Errors (Windows)**
```bash
# If PowerShell blocks script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Server Logs

When running the server, watch for these log messages:
- `✅ Starting hjmcpsse MCP server...` - Server starting successfully
- `❌ Server error: ...` - Check error message for issues
- `🔍 Incoming request: ...` - Server receiving requests

## 📋 Test Checklist

Use this checklist to verify all components work:

### Calculator Tool
- [ ] Basic arithmetic operations
- [ ] Mathematical functions (sqrt, sin, cos, etc.)
- [ ] Error handling (division by zero, invalid syntax)
- [ ] Complex expressions with multiple operations

### Filesystem Resource
- [ ] Directory listing works
- [ ] File content reading works
- [ ] Error handling for non-existent paths
- [ ] Proper file size reporting

### Code Generator
- [ ] Prompt generation with description
- [ ] Different programming languages
- [ ] Template generation (function, class, script)
- [ ] Suggestions provided

### Server Functionality
- [ ] Server starts without errors
- [ ] Server responds to health checks
- [ ] All tools registered properly
- [ ] Resources accessible
- [ ] Prompts available

## 🎯 Expected Output

When running `python test_client.py`, you should see output similar to:

```
🚀 Testing hjmcpsse MCP Server Components
==================================================

🧮 Testing Calculator Tool:
----------------------------------------
Expression: 2 + 3 * 4
Result: 14
Success: True

Expression: sqrt(16) + sin(pi/2)
Result: 5.0
Success: True

📁 Testing Filesystem Resource:
----------------------------------------
Directory: /c/CDrive/Workshops/CustomAI/mcpsse/hjmcpsse
Directories: ['src', '__pycache__']
Files: ['test_client.py', 'TESTING.md', ...]

💬 Testing Code Generator Prompt:
----------------------------------------
Generated prompt:
Create a Python function that meets the following requirements:
...

✅ All component tests completed!
```

## 🚀 Next Steps

After successful testing:

1. **Integrate with MCP clients** - Connect to Claude Desktop or other MCP-compatible tools
2. **Add more tools** - Extend functionality with additional tools
3. **Deploy the server** - Set up for production use
4. **Configure authentication** - Add security if needed

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Review server logs for error messages
4. Ensure virtual environment is properly activated

---

**Happy Testing! 🎉**
