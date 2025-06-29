#!/usr/bin/env python3
"""
Quick test script for Azure AI endpoint
"""

import os
import requests

def test_endpoint():
    endpoint = os.getenv("AZURE_AI_ENDPOINT")
    api_key = os.getenv("AZURE_AI_API_KEY")
    
    print("🔍 Testing Azure AI Endpoint")
    print(f"Endpoint: {endpoint}")
    print(f"API Key: {'*' * 20 + api_key[-4:] if api_key else 'Not set'}")
    
    if not endpoint:
        print("❌ AZURE_AI_ENDPOINT not set")
        return False
        
    if not api_key:
        print("❌ AZURE_AI_API_KEY not set")
        return False
    
    # Test basic connectivity
    try:
        print("\n🌐 Testing DNS resolution...")
        import socket
        hostname = endpoint.replace('https://', '').replace('http://', '').rstrip('/')
        socket.gethostbyname(hostname)
        print("✅ DNS resolution successful")
        
        print("\n🔗 Testing HTTPS connection...")
        response = requests.get(endpoint, timeout=10)
        print(f"✅ HTTPS connection successful (Status: {response.status_code})")
        
        return True
        
    except socket.gaierror as e:
        print(f"❌ DNS resolution failed: {e}")
        print("💡 Check if the endpoint URL is correct")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_endpoint()
