import argparse
import asyncio
import logging
from .server import main as server_main

def main():
    """Main entry point for hjmcpsse MCP server"""
    parser = argparse.ArgumentParser(description="hjmcpsse MCP Server with SSE transport")
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host to bind the server to (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the server to (default: 8000)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set the logging level (default: INFO)"
    )
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting hjmcpsse MCP server on {args.host}:{args.port}")
    
    try:
        asyncio.run(server_main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server failed to start: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
