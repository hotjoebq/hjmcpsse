#!/usr/bin/env python3
"""
Azure AI Foundry Configuration Helper
Helps you find and configure your Azure AI Foundry connection details
"""

import os

def configure_azure_ai():
    """Interactive configuration for Azure AI Foundry"""
    
    print("🔧 Azure AI Foundry Configuration Helper")
    print("=" * 50)
    
    print("\n📋 You need to gather these details from Azure AI Foundry Studio:")
    print("1. Go to: https://ai.azure.com")
    print("2. Select your project")
    print("3. Go to 'Deployments' in the left sidebar")
    print("4. Click on your model deployment")
    print("5. Copy the details from there")
    
    print("\n🔍 Current Environment Variables:")
    current_endpoint = os.getenv("AZURE_AI_ENDPOINT")
    current_key = os.getenv("AZURE_AI_API_KEY")
    current_model = os.getenv("AZURE_AI_MODEL")
    
    print(f"AZURE_AI_ENDPOINT: {current_endpoint or 'Not set'}")
    print(f"AZURE_AI_API_KEY: {'***' + current_key[-4:] if current_key else 'Not set'}")
    print(f"AZURE_AI_MODEL: {current_model or 'Not set'}")
    
    print("\n📝 Please enter your Azure AI Foundry details:")
    
    # Get endpoint
    endpoint = input(f"\n🌐 Endpoint URL (current: {current_endpoint or 'none'}): ").strip()
    if not endpoint and current_endpoint:
        endpoint = current_endpoint
    
    while not endpoint or not endpoint.startswith('https://'):
        print("❌ Please enter a valid HTTPS endpoint URL")
        endpoint = input("🌐 Endpoint URL: ").strip()
    
    # Get API key
    api_key = input(f"\n🔑 API Key (current: {'***' + current_key[-4:] if current_key else 'none'}): ").strip()
    if not api_key and current_key:
        api_key = current_key
    
    while not api_key:
        print("❌ API Key is required")
        api_key = input("🔑 API Key: ").strip()
    
    # Get model name
    model = input(f"\n🤖 Model deployment name (current: {current_model or 'gpt-4o'}): ").strip()
    if not model:
        model = current_model or "gpt-4o"
    
    # Get API version
    current_api_version = os.getenv("AZURE_AI_API_VERSION", "2024-02-15-preview")
    api_version = input(f"\n📋 API Version (current: {current_api_version}): ").strip()
    if not api_version:
        api_version = current_api_version
    
    # Determine endpoint type
    endpoint_type = "openai" if "openai.azure.com" in endpoint else "cognitive"
    print(f"\n🔍 Detected endpoint type: {endpoint_type}")
    
    if endpoint_type == "cognitive":
        print("💡 For Cognitive Services endpoints, you might need:")
        print("   - Deployment name (which can be different from model name)")
        deployment_name = input(f"\n🚀 Deployment name (if different from model name, current: {model}): ").strip()
        if not deployment_name:
            deployment_name = model
    
    # Generate environment variable commands
    print(f"\n✅ Configuration complete! Here are your environment variables:")
    print("\n📋 For Git Bash / Linux:")
    print(f'export AZURE_AI_ENDPOINT="{endpoint}"')
    print(f'export AZURE_AI_API_KEY="{api_key}"')
    print(f'export AZURE_AI_MODEL="{model}"')
    print(f'export AZURE_AI_API_VERSION="{api_version}"')
    if 'deployment_name' in locals() and deployment_name != model:
        print(f'export AZURE_AI_DEPLOYMENT="{deployment_name}"')
    
    print("\n📋 For PowerShell:")
    print(f'$env:AZURE_AI_ENDPOINT="{endpoint}"')
    print(f'$env:AZURE_AI_API_KEY="{api_key}"')
    print(f'$env:AZURE_AI_MODEL="{model}"')
    print(f'$env:AZURE_AI_API_VERSION="{api_version}"')
    if 'deployment_name' in locals() and deployment_name != model:
        print(f'$env:AZURE_AI_DEPLOYMENT="{deployment_name}"')
    
    print("\n📋 For Windows Command Prompt:")
    print(f'set AZURE_AI_ENDPOINT={endpoint}')
    print(f'set AZURE_AI_API_KEY={api_key}')
    print(f'set AZURE_AI_MODEL={model}')
    print(f'set AZURE_AI_API_VERSION={api_version}')
    if 'deployment_name' in locals() and deployment_name != model:
        print(f'set AZURE_AI_DEPLOYMENT={deployment_name}')
    
    # Save to .env file
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    try:
        with open(env_file, 'w') as f:
            f.write(f"AZURE_AI_ENDPOINT={endpoint}\n")
            f.write(f"AZURE_AI_API_KEY={api_key}\n")
            f.write(f"AZURE_AI_MODEL={model}\n")
            f.write(f"AZURE_AI_API_VERSION={api_version}\n")
            if 'deployment_name' in locals() and deployment_name != model:
                f.write(f"AZURE_AI_DEPLOYMENT={deployment_name}\n")
        print(f"\n💾 Configuration saved to: {env_file}")
        print("You can load these with: source .env (in bash)")
    except Exception as e:
        print(f"\n⚠️  Could not save .env file: {e}")
    
    return {
        "endpoint": endpoint,
        "api_key": api_key,
        "model": model,
        "api_version": api_version,
        "deployment_name": locals().get('deployment_name', model)
    }

def test_configuration(config):
    """Test the Azure AI configuration"""
    print(f"\n🧪 Testing configuration...")
    
    try:
        from azure.ai.inference import ChatCompletionsClient
        from azure.core.credentials import AzureKeyCredential
        
        client = ChatCompletionsClient(
            endpoint=config["endpoint"],
            credential=AzureKeyCredential(config["api_key"])
        )
        
        print("✅ Successfully created Azure AI client")
        print(f"✅ Endpoint: {config['endpoint']}")
        print(f"✅ Model: {config['model']}")
        
        return True
        
    except ImportError:
        print("❌ Azure AI SDK not installed. Run: pip install azure-ai-inference azure-identity")
        return False
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        print("\n🔍 Common issues:")
        print("- Check that your endpoint URL is correct")
        print("- Verify your API key is valid")
        print("- Ensure your model is deployed")
        return False

if __name__ == "__main__":
    try:
        config = configure_azure_ai()
        
        # Ask if user wants to test
        test = input("\n🧪 Test the configuration now? (y/n): ").strip().lower()
        if test in ['y', 'yes']:
            test_configuration(config)
            
    except KeyboardInterrupt:
        print("\n\n👋 Configuration cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
