#!/usr/bin/env python3
"""
Entry point for hjmcpsse MCP server
"""

import sys
from .server import main

if __name__ == "__main__":
    sys.exit(main())
