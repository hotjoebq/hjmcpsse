import argparse
import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP
from .resources.filesystem import list_directory, get_file_content
from .tools.calculator import calculate
from .prompts.code_generator import generate_code_prompt, get_code_template

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_file_resource(path: str) -> str:
    """Browse filesystem and get file/directory information"""
    try:
        file_path = Path(path)
        
        if file_path.is_dir():
            listing = list_directory(path)
            result = f"Directory: {listing.path}\n\n"
            
            if listing.directories:
                result += "Directories:\n"
                for dir_info in listing.directories:
                    result += f"  📁 {dir_info.name}\n"
                result += "\n"
            
            if listing.files:
                result += "Files:\n"
                for file_info in listing.files:
                    size_kb = file_info.size / 1024
                    result += f"  📄 {file_info.name} ({size_kb:.1f} KB)\n"
            
            return result
        
        elif file_path.is_file():
            content = get_file_content(path)
            return f"File: {path}\n\n{content}"
        
        else:
            return f"Path not found: {path}"
    
    except Exception as e:
        return f"Error accessing {path}: {str(e)}"


def calculator(expression: str) -> Dict[str, Any]:
    """Calculate mathematical expressions safely
    
    Args:
        expression: Mathematical expression to evaluate (e.g., "2 + 3 * 4")
    """
    result = calculate(expression)
    return {
        "expression": result.expression,
        "result": result.result,
        "success": result.success,
        "error": result.error if not result.success else None
    }


def code_generator(
    description: str,
    language: str = "python",
    style: str = "clean",
    include_tests: bool = False,
    include_docs: bool = True
) -> str:
    """Generate structured prompts for code generation
    
    Args:
        description: Description of the code to generate
        language: Programming language (default: python)
        style: Code style preference (clean, functional, object-oriented)
        include_tests: Whether to include unit tests
        include_docs: Whether to include documentation
    """
    prompt_data = generate_code_prompt(
        description=description,
        language=language,
        style=style,
        include_tests=include_tests,
        include_docs=include_docs
    )
    
    result = prompt_data.prompt
    
    if prompt_data.suggestions:
        suggestions_text = "\n".join(f"- {suggestion}" for suggestion in prompt_data.suggestions)
        result += f"\n\nAdditional suggestions:\n{suggestions_text}"
    
    return result


def get_template(language: str = "python", template_type: str = "function") -> Dict[str, Any]:
    """Get code templates for common patterns
    
    Args:
        language: Programming language (default: python)
        template_type: Type of template (class, function, script)
    """
    template = get_code_template(language, template_type)
    return {
        "language": language,
        "template_type": template_type,
        "template": template
    }


def main():
    """Run the MCP server"""
    parser = argparse.ArgumentParser(description="hjmcpsse MCP Server")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--log-level", default="INFO", help="Log level")
    
    args = parser.parse_args()
    
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))
    
    mcp = FastMCP("hjmcpsse", host=args.host, port=args.port)
    
    mcp.resource("files://{path}")(get_file_resource)
    mcp.tool()(calculator)
    mcp.prompt("code_generator")(code_generator)
    mcp.tool()(get_template)
    
    logger.info(f"Starting hjmcpsse MCP server with SSE transport on {args.host}:{args.port}...")
    
    try:
        mcp.run(transport="sse")
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
