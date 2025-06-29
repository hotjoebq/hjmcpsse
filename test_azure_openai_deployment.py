import os
import sys
import json

try:
    from dotenv import load_dotenv
except ImportError:
    print("python-dotenv not found. Please install with: pip install python-dotenv")
    sys.exit(1)

import requests

# Load .env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

endpoint = os.environ.get("AZURE_AI_ENDPOINT")
deployment = os.environ.get("AZURE_AI_DEPLOYMENT")
api_key = os.environ.get("AZURE_AI_API_KEY")
api_version = os.environ.get("AZURE_AI_API_VERSION")

if not all([endpoint, deployment, api_key, api_version]):
    print("❌ Missing one or more required environment variables. Please check your .env file.")
    sys.exit(1)

# Remove trailing slash from endpoint if present
endpoint = endpoint.rstrip("/")

url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"
headers = {
    "api-key": api_key,
    "Content-Type": "application/json"
}

# Simple prompt for test
data = {
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello!"}
    ],
    "max_tokens": 32
}

print(f"\nTesting Azure OpenAI deployment: {deployment}")
print(f"Endpoint: {endpoint}")
print(f"API version: {api_version}")
print(f"Request URL: {url}")

try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Deployment is working! Response:")
        print(json.dumps(result, indent=2))
    else:
        print("\n❌ Deployment test failed. Response:")
        print(response.text)
except Exception as e:
    print(f"Error connecting to Azure OpenAI: {e}")
