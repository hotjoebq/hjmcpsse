#!/usr/bin/env python3
"""
Simple test client for the hjmcpsse MCP server - Direct function testing
"""

import sys
import os

# Add the src directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_calculator():
    """Test the calculator functionality directly"""
    print("🧮 Testing Calculator Tool:")
    print("-" * 40)
    
    try:
        from hjmcpsse.tools.calculator import calculate
        
        # Test simple expression
        result1 = calculate("2 + 3 * 4")
        print(f"Expression: {result1.expression}")
        print(f"Result: {result1.result}")
        print(f"Success: {result1.success}")
        if result1.error:
            print(f"Error: {result1.error}")
        print()
        
        # Test complex expression with functions
        result2 = calculate("sqrt(16) + sin(pi/2)")
        print(f"Expression: {result2.expression}")
        print(f"Result: {result2.result}")
        print(f"Success: {result2.success}")
        if result2.error:
            print(f"Error: {result2.error}")
        print()
        
        # Test division by zero
        result3 = calculate("1 / 0")
        print(f"Expression: {result3.expression}")
        print(f"Result: {result3.result}")
        print(f"Success: {result3.success}")
        if result3.error:
            print(f"Error: {result3.error}")
        print()
        
        # Test invalid expression
        result4 = calculate("2 +* 3")
        print(f"Expression: {result4.expression}")
        print(f"Result: {result4.result}")
        print(f"Success: {result4.success}")
        if result4.error:
            print(f"Error: {result4.error}")
        print()
        
    except Exception as e:
        print(f"❌ Error testing calculator: {e}")
        import traceback
        traceback.print_exc()

def test_filesystem():
    """Test the filesystem functionality directly"""
    print("📁 Testing Filesystem Resource:")
    print("-" * 40)
    
    try:
        from hjmcpsse.resources.filesystem import list_directory, get_file_content
        
        # Test directory listing
        current_dir = os.path.dirname(__file__)
        listing = list_directory(current_dir)
        print(f"Directory: {listing.path}")
        print(f"Directories: {[d.name for d in listing.directories]}")
        print(f"Files: {[f.name for f in listing.files]}")
        print()
        
        # Test file reading (try to read this test file)
        test_file_path = __file__
        content = get_file_content(test_file_path)
        print(f"File content preview (first 200 chars):")
        print(content[:200] + "..." if len(content) > 200 else content)
        print()
        
    except Exception as e:
        print(f"❌ Error testing filesystem: {e}")
        import traceback
        traceback.print_exc()

def test_code_generator():
    """Test the code generator functionality directly"""
    print("� Testing Code Generator Prompt:")
    print("-" * 40)
    
    try:
        from hjmcpsse.prompts.code_generator import generate_code_prompt, get_code_template
        
        # Test code prompt generation
        prompt_result = generate_code_prompt(
            description="Create a function to calculate fibonacci numbers",
            language="python",
            style="clean",
            include_tests=True,
            include_docs=True
        )
        
        print("Generated prompt:")
        print(prompt_result.prompt)
        print()
        
        if prompt_result.suggestions:
            print("Suggestions:")
            for suggestion in prompt_result.suggestions:
                print(f"  - {suggestion}")
            print()
        
        # Test template generation
        template = get_code_template("python", "function")
        print("Function template:")
        print(template)
        print()
        
        class_template = get_code_template("python", "class")
        print("Class template:")
        print(class_template)
        print()
        
    except Exception as e:
        print(f"❌ Error testing code generator: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all tests"""
    print("🚀 Testing hjmcpsse MCP Server Components")
    print("=" * 50)
    print()
    
    test_calculator()
    test_filesystem()
    test_code_generator()
    
    print("✅ All component tests completed!")

if __name__ == "__main__":
    main()
