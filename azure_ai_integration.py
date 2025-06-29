#!/usr/bin/env python3
"""
Azure AI Foundry integration for hjmcpsse MCP server
This creates a bridge between Azure AI models and the MCP server
"""

import asyncio
import json
import os
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage, ToolMessage
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
import sys
import requests

# Configure logging early so logger is available for dotenv loading
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env if present
def _try_load_dotenv():
    try:
        from dotenv import load_dotenv
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
            logger.info(f"Loaded environment variables from {dotenv_path}")
    except ImportError:
        logger.warning("python-dotenv not installed; skipping .env loading.")
    except Exception as e:
        logger.warning(f"Could not load .env file: {e}")

_try_load_dotenv()

# Add src directory to path for MCP server imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import our MCP server components directly for efficiency
from hjmcpsse.tools.calculator import calculate
from hjmcpsse.resources.filesystem import list_directory, get_file_content
from hjmcpsse.prompts.code_generator import generate_code_prompt, get_code_template

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AzureAIConfig:
    """Configuration for Azure AI Foundry connection"""
    endpoint: str
    model_name: str
    api_key: Optional[str] = None
    api_version: str = "2024-02-15-preview"  # Common API version for Azure OpenAI
    use_managed_identity: bool = True
    max_tokens: int = 4000
    temperature: float = 0.7
    deployment_name: Optional[str] = None  # Sometimes different from model_name

class MCPToolRegistry:
    """Registry of MCP tools available to Azure AI models"""
    
    def __init__(self):
        self.tools = {
            "calculator": {
                "type": "function",
                "function": {
                    "name": "calculator",
                    "description": "Calculate mathematical expressions safely. Supports basic arithmetic, functions like sqrt, sin, cos, log, and constants like pi, e.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Mathematical expression to evaluate (e.g., '2 + 3 * 4', 'sqrt(16)', 'sin(pi/2)')"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            },
            "browse_filesystem": {
                "type": "function",
                "function": {
                    "name": "browse_filesystem",
                    "description": "Browse directories and read file contents from the local filesystem.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "File or directory path to browse"
                            },
                            "action": {
                                "type": "string",
                                "enum": ["list", "read"],
                                "description": "Action to perform: 'list' for directory contents, 'read' for file content"
                            }
                        },
                        "required": ["path", "action"]
                    }
                }
            },
            "get_code_template": {
                "type": "function",
                "function": {
                    "name": "get_code_template",
                    "description": "Get code templates for common programming patterns.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "language": {
                                "type": "string",
                                "enum": ["python", "javascript", "typescript", "java", "csharp"],
                                "description": "Programming language for the template"
                            },
                            "template_type": {
                                "type": "string",
                                "enum": ["function", "class", "script"],
                                "description": "Type of code template to generate"
                            }
                        },
                        "required": ["language", "template_type"]
                    }
                }
            },
            "generate_code_prompt": {
                "type": "function", 
                "function": {
                    "name": "generate_code_prompt",
                    "description": "Generate structured prompts for code generation with best practices.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "description": {
                                "type": "string",
                                "description": "Description of the code to generate"
                            },
                            "language": {
                                "type": "string",
                                "enum": ["python", "javascript", "typescript", "java", "csharp"],
                                "description": "Programming language (default: python)"
                            },
                            "style": {
                                "type": "string",
                                "enum": ["clean", "functional", "object-oriented"],
                                "description": "Code style preference (default: clean)"
                            },
                            "include_tests": {
                                "type": "boolean",
                                "description": "Whether to include unit tests (default: false)"
                            },
                            "include_docs": {
                                "type": "boolean", 
                                "description": "Whether to include documentation (default: true)"
                            }
                        },
                        "required": ["description"]
                    }
                }
            }
        }
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with the given arguments"""
        try:
            if tool_name == "calculator":
                result = calculate(arguments["expression"])
                return {
                    "success": True,
                    "data": {
                        "expression": result.expression,
                        "result": result.result,
                        "success": result.success,
                        "error": result.error
                    }
                }
            
            elif tool_name == "browse_filesystem":
                path = arguments["path"]
                action = arguments["action"]
                
                if action == "list":
                    listing = list_directory(path)
                    return {
                        "success": True,
                        "data": {
                            "path": listing.path,
                            "directories": [{"name": d.name, "size": d.size} for d in listing.directories],
                            "files": [{"name": f.name, "size": f.size} for f in listing.files]
                        }
                    }
                elif action == "read":
                    content = get_file_content(path)
                    return {
                        "success": True,
                        "data": {
                            "path": path,
                            "content": content[:5000] + "..." if len(content) > 5000 else content  # Limit content size
                        }
                    }
                    
            elif tool_name == "get_code_template":
                template = get_code_template(
                    arguments.get("language", "python"),
                    arguments.get("template_type", "function")
                )
                return {
                    "success": True,
                    "data": {
                        "language": arguments.get("language", "python"),
                        "template_type": arguments.get("template_type", "function"),
                        "template": template
                    }
                }
                
            elif tool_name == "generate_code_prompt":
                prompt_result = generate_code_prompt(
                    description=arguments["description"],
                    language=arguments.get("language", "python"),
                    style=arguments.get("style", "clean"),
                    include_tests=arguments.get("include_tests", False),
                    include_docs=arguments.get("include_docs", True)
                )
                return {
                    "success": True,
                    "data": {
                        "prompt": prompt_result.prompt,
                        "suggestions": prompt_result.suggestions
                    }
                }
            
            else:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}"
                }
                
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }

class AzureAIMCPClient:
    """Azure AI Foundry client with MCP server integration"""
    
    def __init__(self, config: AzureAIConfig):
        self.config = config
        self.tool_registry = MCPToolRegistry()
        self.client = None
        self._setup_client()
    
    def _setup_client(self):
        """Initialize Azure AI client with proper authentication"""
        try:
            if self.config.use_managed_identity:
                # Use Managed Identity for Azure-hosted environments
                credential = DefaultAzureCredential()
                logger.info("Using Managed Identity for authentication")
            elif self.config.api_key:
                # Use API key for development/testing
                credential = AzureKeyCredential(self.config.api_key)
                logger.info("Using API key for authentication")
            else:
                raise ValueError("Either use_managed_identity must be True or api_key must be provided")
            
            # Ensure endpoint has proper format for Azure AI services
            endpoint = self.config.endpoint
            if not endpoint.endswith('/'):
                endpoint += '/'
            
            # For Azure OpenAI, we might need to construct the full endpoint
            if 'openai.azure.com' in endpoint:
                # This is Azure OpenAI format
                self.client = ChatCompletionsClient(
                    endpoint=endpoint,
                    credential=credential,
                    api_version=self.config.api_version
                )
            else:
                # This is standard Azure AI services format
                self.client = ChatCompletionsClient(
                    endpoint=endpoint,
                    credential=credential
                )
            
            logger.info(f"Connected to Azure AI endpoint: {endpoint}")
            logger.info(f"Using API version: {getattr(self.config, 'api_version', 'default')}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Azure AI client: {e}")
            raise
    
    async def chat_with_tools(self, messages: List[Dict[str, str]], max_tool_calls: int = 5) -> Dict[str, Any]:
        """
        Chat with Azure AI model using MCP tools (function-calling loop)
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            max_tool_calls: Maximum number of tool calls allowed in a conversation
            
        Returns:
            Dictionary with response and tool call history
        """
        try:
            rest_messages = []
            for msg in messages:
                rest_messages.append({"role": msg["role"], "content": msg["content"]})

            tool_call_history = []
            for iteration in range(max_tool_calls):
                # On the first request, include tool definitions
                include_tools = (iteration == 0)
                url = f"{self.config.endpoint.rstrip('/')}/openai/deployments/{self.config.deployment_name}/chat/completions?api-version={self.config.api_version}"
                headers = {
                    "api-key": self.config.api_key,
                    "Content-Type": "application/json"
                }
                data = {
                    "messages": rest_messages,
                    "max_tokens": self.config.max_tokens,
                    "temperature": self.config.temperature
                }
                if include_tools:
                    data["tools"] = list(self.tool_registry.tools.values())
                response = requests.post(url, headers=headers, data=json.dumps(data))
                if response.status_code != 200:
                    logger.error(f"REST API call failed: {response.text}")
                    raise Exception(f"REST API call failed: {response.text}")
                result = response.json()
                choice = result["choices"][0]
                message = choice["message"]
                # Check for tool calls
                if "tool_calls" in message and message["tool_calls"]:
                    tool_messages = []
                    for tool_call in message["tool_calls"]:
                        tool_name = tool_call["function"]["name"]
                        tool_args = json.loads(tool_call["function"]["arguments"])
                        logger.info(f"Executing tool: {tool_name} with args: {tool_args}")
                        tool_result = await self.tool_registry.execute_tool(tool_name, tool_args)
                        tool_call_history.append({
                            "tool": tool_name,
                            "arguments": tool_args,
                            "result": tool_result
                        })
                        # Add tool result to conversation as a 'tool' message
                        tool_messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "content": json.dumps(tool_result)
                        })
                    # Append the assistant's tool_call message and the tool response(s)
                    rest_messages.append({
                        k: v for k, v in message.items() if k in ("role", "content", "tool_calls")
                    })
                    rest_messages.extend(tool_messages)
                    # Next request: do NOT include 'tools' field
                    continue
                else:
                    # Model provided final response
                    return {
                        "response": message["content"],
                        "tool_calls": tool_call_history,
                        "finish_reason": choice["finish_reason"],
                        "total_tokens": result["usage"]["total_tokens"] if "usage" in result else None
                    }
            return {
                "response": "Maximum tool calls reached.",
                "tool_calls": tool_call_history,
                "finish_reason": "max_tool_calls",
                "total_tokens": None
            }
        except Exception as e:
            logger.error(f"Error in chat_with_tools (REST tool-calling): {e}")
            raise

async def example_azure_ai_conversation():
    """Example conversation using Azure AI with MCP tools"""
    # Configuration - replace with your Azure AI Foundry details
    endpoint = os.getenv("AZURE_AI_ENDPOINT")
    api_key = os.getenv("AZURE_AI_API_KEY")
    model_name = os.getenv("AZURE_AI_MODEL", "gpt-4o")
    api_version = os.getenv("AZURE_AI_API_VERSION", "2024-02-15-preview")
    deployment_name = os.getenv("AZURE_AI_DEPLOYMENT")

    # Print config for verification
    print("[Config] Using the following Azure AI connection values:")
    print(f"  Endpoint:        {endpoint}")
    print(f"  Model name:      {model_name}")
    print(f"  Deployment name: {deployment_name}")
    print(f"  API version:     {api_version}")
    print(f"  API key present: {'Yes' if api_key else 'No'}")

    # Print .env contents except API key
    try:
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            print("\n[.env file contents (excluding API key)]:")
            with open(dotenv_path, 'r') as f:
                for line in f:
                    if 'API_KEY' in line:
                        print('AZURE_AI_API_KEY=***hidden***')
                    else:
                        print(line.rstrip())
    except Exception as e:
        print(f"[Warning] Could not read .env file: {e}")

    # Always require deployment_name, never prompt for it
    if not deployment_name:
        print("❌ Please set AZURE_AI_DEPLOYMENT in your .env file to your deployment name from Azure Portal.")
        return

    config = AzureAIConfig(
        endpoint=endpoint,
        model_name=model_name,
        api_key=api_key,
        api_version=api_version,
        deployment_name=deployment_name,
        use_managed_identity=False  # Set to True in Azure-hosted environments
    )
    
    if not config.api_key and not config.use_managed_identity:
        print("❌ Please set AZURE_AI_API_KEY environment variable or configure managed identity")
        return
    
    try:
        # Create client
        ai_client = AzureAIMCPClient(config)
        
        print("🚀 Azure AI Foundry + MCP Server Integration Demo")
        print("=" * 50)
        
        # Example conversation
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant with access to calculator, filesystem, and code generation tools. Use these tools when appropriate to help users."
            },
            {
                "role": "user",
                "content": "Can you calculate the square root of 144, then list the files in my current directory, and finally generate a Python function template?"
            }
        ]
        
        print("🤖 User:", messages[-1]["content"])
        print("\n🔄 Processing with Azure AI model...")
        
        result = await ai_client.chat_with_tools(messages)
        
        print(f"\n✅ AI Response:")
        print(result["response"])
        
        print(f"\n📊 Tool Calls Made ({len(result['tool_calls'])}):")
        for i, tool_call in enumerate(result["tool_calls"], 1):
            print(f"  {i}. {tool_call['tool']}: {tool_call['arguments']}")
            if tool_call['result']['success']:
                print(f"     ✅ Success: {str(tool_call['result']['data'])[:100]}...")
            else:
                print(f"     ❌ Error: {tool_call['result']['error']}")
        
        if result.get("total_tokens"):
            print(f"\n📈 Tokens used: {result['total_tokens']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.exception("Full error details:")

async def interactive_chat():
    """Interactive chat session with Azure AI and MCP tools"""
    # Configuration
    config = AzureAIConfig(
        endpoint=input("Enter Azure AI Foundry endpoint: ").strip(),
        model_name=input("Enter model name (e.g., gpt-4o): ").strip() or "gpt-4o",
        use_managed_identity=False,
        api_key=os.getenv("AZURE_AI_API_KEY") or input("Enter API key: ").strip(),
        deployment_name=os.getenv("AZURE_AI_DEPLOYMENT")  # <-- Fix: load deployment name from .env
    )
    
    try:
        ai_client = AzureAIMCPClient(config)
        
        print("\n🎉 Azure AI + MCP Chat Session Started!")
        print("Available tools: calculator, browse_filesystem, get_code_template, generate_code_prompt")
        print("Type 'quit' to exit\n")
        
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant with access to calculator, filesystem browsing, and code generation tools. Use these tools when appropriate to help users. Be concise but thorough in your responses."
            }
        ]
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
                
            if not user_input:
                continue
            
            messages.append({"role": "user", "content": user_input})
            
            print("🤖 Assistant: ", end="", flush=True)
            
            try:
                result = await ai_client.chat_with_tools(messages)
                print(result["response"])
                
                messages.append({"role": "assistant", "content": result["response"]})
                
                if result["tool_calls"]:
                    print(f"🔧 Used {len(result['tool_calls'])} tool(s)")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Setup error: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Azure AI Foundry + MCP Server Integration")
    parser.add_argument("--mode", choices=["demo", "chat"], default="demo",
                       help="Run mode: demo for example conversation, chat for interactive session")
    
    args = parser.parse_args()
    
    if args.mode == "demo":
        asyncio.run(example_azure_ai_conversation())
    else:
        asyncio.run(interactive_chat())
