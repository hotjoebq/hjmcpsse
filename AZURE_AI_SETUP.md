# Azure AI Foundry + MCP Server Integration Setup

## 📋 Prerequisites

1. **Azure AI Foundry Hub and Project**
2. **Model Deployment** (e.g., GPT-4o, GPT-4, GPT-3.5-turbo)
3. **Azure AI SDK** installed
4. **Authentication** configured

## 🚀 Quick Setup

### 1. Install Required Dependencies

Add these to your `requirements.txt`:
```
azure-ai-inference>=1.0.0
azure-identity>=1.15.0
azure-core>=1.29.0
```

Install them:
```bash
source ../venv_py312/Scripts/activate
pip install azure-ai-inference azure-identity azure-core
```

### 2. Get Your Azure AI Foundry Details

From Azure AI Foundry Studio:
1. Go to your project
2. Click "Deployments" 
3. Note your:
   - **Endpoint URL** (e.g., `https://your-project.cognitiveservices.azure.com/`)
   - **Model deployment name** (e.g., `gpt-4o`)
   - **API Key** (from Keys and Endpoint section)

### 3. Set Environment Variables

**Git Bash / Linux:**
```bash
export AZURE_AI_API_KEY="your-api-key-here"
export AZURE_AI_ENDPOINT="https://hjmrdevproj-ai-services-dev-nyuxwr.cognitiveservices.azure.com/"
export AZURE_AI_MODEL="gpt-4o"
export AZURE_AI_API_VERSION="2024-02-15-preview"
# Optional: if deployment name differs from model name
# export AZURE_AI_DEPLOYMENT="your-deployment-name"
```

**PowerShell:**
```powershell
$env:AZURE_AI_API_KEY="your-api-key-here"
$env:AZURE_AI_ENDPOINT="https://hjmrdevproj-ai-services-dev-nyuxwr.cognitiveservices.azure.com/"
$env:AZURE_AI_MODEL="gpt-4o"
$env:AZURE_AI_API_VERSION="2024-02-15-preview"
# Optional: if deployment name differs from model name
# $env:AZURE_AI_DEPLOYMENT="your-deployment-name"
```

**Windows Command Prompt:**
```cmd
set AZURE_AI_API_KEY=your-api-key-here
set AZURE_AI_ENDPOINT=https://hjmrdevproj-ai-services-dev-nyuxwr.cognitiveservices.azure.com/
set AZURE_AI_MODEL=gpt-4o
```

## 🧪 Testing

### Run Demo Conversation
```bash
python azure_ai_integration.py --mode demo
```

### Interactive Chat
```bash
python azure_ai_integration.py --mode chat
```

## 🔧 Configuration Options

Edit the `AzureAIConfig` in `azure_ai_integration.py`:

```python
config = AzureAIConfig(
    endpoint=os.getenv("AZURE_AI_ENDPOINT"),
    model_name=os.getenv("AZURE_AI_MODEL", "gpt-4o"),
    api_key=os.getenv("AZURE_AI_API_KEY"),
    use_managed_identity=False,  # Set True for Azure-hosted deployments
    max_tokens=4000,
    temperature=0.7
)
```

## 🛡️ Security Best Practices

### For Development:
- Use API keys stored in environment variables
- Never commit API keys to source control

### For Production:
- Use Managed Identity when deployed to Azure
- Store secrets in Azure Key Vault
- Set `use_managed_identity=True`

## 🎯 Available MCP Tools

Your Azure AI model will have access to:

1. **Calculator Tool**
   - Mathematical expressions
   - Functions: sqrt, sin, cos, log, etc.
   - Constants: pi, e

2. **Filesystem Browser**
   - List directory contents
   - Read file contents
   - Safe path handling

3. **Code Template Generator**
   - Function, class, script templates
   - Multiple languages: Python, JavaScript, TypeScript, Java, C#

4. **Code Prompt Generator**
   - Structured prompts for code generation
   - Style preferences
   - Documentation and test inclusion

## 💬 Example Prompts

Try these with your Azure AI model:

```
"Calculate the area of a circle with radius 5"
"List the files in my current project directory"
"Generate a Python class template"
"Create a code prompt for building a REST API"
"What's the square root of 144 plus sin(pi/2)?"
"Show me the contents of my README.md file"
```

## 🔍 Troubleshooting

### Common Issues:

1. **Authentication Error**
   - Verify API key is correct
   - Check endpoint URL format
   - Ensure model is deployed

2. **API Version Error**
   - Try different API versions: `2024-02-15-preview`, `2023-12-01-preview`, `2023-05-15`
   - Check Azure AI Foundry documentation for supported versions
   - Some models require specific API versions

3. **Model Not Found Error**
   - Verify model deployment name in Azure AI Foundry
   - Check if deployment name differs from model name
   - Set `AZURE_AI_DEPLOYMENT` if different from `AZURE_AI_MODEL`

4. **DNS Resolution Issues**
   - Ensure endpoint URL includes `https://` and ends with `/`
   - Try alternative endpoint formats:
     - `https://your-resource.openai.azure.com/` (for Azure OpenAI)
     - `https://your-resource.cognitiveservices.azure.com/` (for Cognitive Services)

5. **Import Errors**
   - Install required packages: `pip install azure-ai-inference azure-identity`
   - Activate virtual environment

6. **Tool Execution Errors**
   - Check file paths exist
   - Verify calculator expression syntax
   - Review error logs

### Debug Mode:
Set logging level to DEBUG:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Next Steps

1. **Deploy to Azure**: Use Managed Identity authentication
2. **Add Custom Tools**: Extend `MCPToolRegistry` with your own tools
3. **Web Interface**: Create a web app using Flask/FastAPI
4. **Monitoring**: Add Application Insights for production monitoring

## 🔗 References

- [Azure AI Foundry Documentation](https://docs.microsoft.com/azure/ai-services/)
- [Azure AI Inference SDK](https://docs.microsoft.com/python/api/overview/azure/ai-inference/)
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
