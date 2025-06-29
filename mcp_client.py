#!/usr/bin/env python3
"""
MCP Client to connect AI models to hjmcpsse server
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class HjmcpsseClient:
    """Client to interact with hjmcpsse MCP server"""
    
    def __init__(self, server_path: str = None):
        """Initialize the MCP client
        
        Args:
            server_path: Path to the hjmcpsse server directory
        """
        self.server_path = server_path or "C:/CDrive/Workshops/CustomAI/mcpsse/hjmcpsse/src"
        self.session = None
        
    async def connect(self):
        """Connect to the MCP server"""
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "hjmcpsse"],
            cwd=self.server_path
        )
        
        self.client_context = stdio_client(server_params)
        self.read, self.write = await self.client_context.__aenter__()
        self.session = ClientSession(self.read, self.write)
        await self.session.__aenter__()
        await self.session.initialize()
        
    async def disconnect(self):
        """Disconnect from the MCP server"""
        if self.session:
            await self.session.__aexit__(None, None, None)
        if hasattr(self, 'client_context'):
            await self.client_context.__aexit__(None, None, None)
    
    async def list_tools(self):
        """Get available tools"""
        if not self.session:
            raise RuntimeError("Not connected to server")
        return await self.session.list_tools()
    
    async def list_resources(self):
        """Get available resources"""
        if not self.session:
            raise RuntimeError("Not connected to server")
        return await self.session.list_resources()
    
    async def list_prompts(self):
        """Get available prompts"""
        if not self.session:
            raise RuntimeError("Not connected to server")
        return await self.session.list_prompts()
    
    async def call_tool(self, tool_name: str, arguments: dict):
        """Call a tool with arguments"""
        if not self.session:
            raise RuntimeError("Not connected to server")
        return await self.session.call_tool(tool_name, arguments)
    
    async def get_resource(self, uri: str):
        """Get a resource by URI"""
        if not self.session:
            raise RuntimeError("Not connected to server")
        return await self.session.read_resource(uri)
    
    async def get_prompt(self, prompt_name: str, arguments: dict = None):
        """Get a prompt with optional arguments"""
        if not self.session:
            raise RuntimeError("Not connected to server")
        return await self.session.get_prompt(prompt_name, arguments or {})

class AIModelInterface:
    """Interface for AI models to use MCP tools"""
    
    def __init__(self, client: HjmcpsseClient):
        self.client = client
        
    async def calculate(self, expression: str):
        """Use the calculator tool"""
        result = await self.client.call_tool("calculator", {"expression": expression})
        return result.content
    
    async def browse_directory(self, path: str):
        """Browse a directory using filesystem resource"""
        uri = f"files://{path}"
        result = await self.client.get_resource(uri)
        return result.content
    
    async def get_code_template(self, language: str = "python", template_type: str = "function"):
        """Get a code template"""
        result = await self.client.call_tool("get_template", {
            "language": language,
            "template_type": template_type
        })
        return result.content
    
    async def generate_code_prompt(self, description: str, language: str = "python", 
                                 style: str = "clean", include_tests: bool = True):
        """Generate a code prompt"""
        result = await self.client.get_prompt("code_generator", {
            "description": description,
            "language": language,
            "style": style,
            "include_tests": include_tests
        })
        return result.messages[0].content.text if result.messages else ""

async def example_ai_interaction():
    """Example of how an AI model would interact with the MCP server"""
    
    # Create and connect client
    client = HjmcpsseClient()
    ai_interface = AIModelInterface(client)
    
    try:
        await client.connect()
        print("✅ Connected to hjmcpsse MCP server")
        
        # List available capabilities
        tools = await client.list_tools()
        print(f"\n📋 Available tools: {[tool.name for tool in tools.tools]}")
        
        resources = await client.list_resources()
        print(f"📁 Available resources: {len(resources.resources)} resource types")
        
        prompts = await client.list_prompts()
        print(f"💬 Available prompts: {[prompt.name for prompt in prompts.prompts]}")
        
        # Simulate AI model using tools
        print("\n🤖 AI Model using MCP tools:")
        print("=" * 40)
        
        # Use calculator
        calc_result = await ai_interface.calculate("sqrt(144) + 5 * 3")
        print(f"🧮 Math calculation: {calc_result}")
        
        # Browse directory
        dir_result = await ai_interface.browse_directory("/c/CDrive/Workshops/CustomAI/mcpsse")
        print(f"📁 Directory contents: {dir_result[:100]}...")
        
        # Get code template
        template_result = await ai_interface.get_code_template("python", "function")
        print(f"📝 Code template: {template_result}")
        
        # Generate code prompt
        prompt_result = await ai_interface.generate_code_prompt(
            "Create a function to validate email addresses"
        )
        print(f"💡 Generated prompt: {prompt_result[:100]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await client.disconnect()
        print("\n✅ Disconnected from server")

async def main():
    """Run the example"""
    await example_ai_interaction()

if __name__ == "__main__":
    asyncio.run(main())
