"""
Code generation prompts for MCP server
"""

from typing import List, Optional
from dataclasses import dataclass


@dataclass
class CodePromptData:
    """Data structure for code generation prompts"""
    prompt: str
    suggestions: List[str]
    language: str
    style: str


def generate_code_prompt(
    description: str,
    language: str = "python",
    style: str = "clean",
    include_tests: bool = False,
    include_docs: bool = True
) -> CodePromptData:
    """Generate a structured prompt for code generation
    
    Args:
        description: Description of the code to generate
        language: Programming language (default: python)
        style: Code style preference (clean, functional, object-oriented)
        include_tests: Whether to include unit tests
        include_docs: Whether to include documentation
        
    Returns:
        CodePromptData with the generated prompt and suggestions
    """
    
    prompt_parts = []
    
    if language.lower() == "python":
        prompt_parts.append(f"Write Python code that {description}.")
        if style == "functional":
            prompt_parts.append("Use a functional programming approach with pure functions.")
        elif style == "object-oriented":
            prompt_parts.append("Use object-oriented design with appropriate classes and methods.")
        else:
            prompt_parts.append("Write clean, readable code following Python best practices.")
    elif language.lower() == "javascript":
        prompt_parts.append(f"Write JavaScript code that {description}.")
        if style == "functional":
            prompt_parts.append("Use functional programming patterns with arrow functions and immutable data.")
        elif style == "object-oriented":
            prompt_parts.append("Use ES6+ classes and modern JavaScript features.")
        else:
            prompt_parts.append("Write clean, modern JavaScript following best practices.")
    elif language.lower() == "typescript":
        prompt_parts.append(f"Write TypeScript code that {description}.")
        prompt_parts.append("Include proper type annotations and interfaces.")
    else:
        prompt_parts.append(f"Write {language} code that {description}.")
    
    if include_docs:
        if language.lower() == "python":
            prompt_parts.append("Include comprehensive docstrings for all functions and classes.")
        elif language.lower() in ["javascript", "typescript"]:
            prompt_parts.append("Include JSDoc comments for all functions and classes.")
        else:
            prompt_parts.append("Include appropriate documentation comments.")
    
    if include_tests:
        if language.lower() == "python":
            prompt_parts.append("Include unit tests using pytest or unittest.")
        elif language.lower() in ["javascript", "typescript"]:
            prompt_parts.append("Include unit tests using Jest or similar testing framework.")
        else:
            prompt_parts.append("Include appropriate unit tests.")
    
    prompt_parts.extend([
        "Ensure proper error handling and edge case management.",
        "Follow naming conventions and code organization best practices.",
        "Make the code maintainable and extensible."
    ])
    
    suggestions = []
    
    if "function" in description.lower():
        suggestions.append("Consider breaking complex logic into smaller helper functions")
        suggestions.append("Add input validation and type checking")
    
    if "class" in description.lower():
        suggestions.append("Follow SOLID principles for class design")
        suggestions.append("Consider using composition over inheritance where appropriate")
    
    if "api" in description.lower() or "endpoint" in description.lower():
        suggestions.append("Include proper HTTP status codes and error responses")
        suggestions.append("Add request validation and sanitization")
    
    if "data" in description.lower() or "database" in description.lower():
        suggestions.append("Consider data validation and sanitization")
        suggestions.append("Implement proper error handling for data operations")
    
    if include_tests:
        suggestions.append("Test both happy path and error scenarios")
        suggestions.append("Consider edge cases and boundary conditions")
    
    if language.lower() == "python":
        suggestions.extend([
            "Use type hints for better code documentation",
            "Consider using dataclasses or Pydantic for data structures",
            "Follow PEP 8 style guidelines"
        ])
    elif language.lower() in ["javascript", "typescript"]:
        suggestions.extend([
            "Use const/let instead of var",
            "Consider using async/await for asynchronous operations",
            "Use destructuring and spread operators where appropriate"
        ])
    
    prompt = " ".join(prompt_parts)
    
    return CodePromptData(
        prompt=prompt,
        suggestions=suggestions,
        language=language,
        style=style
    )


def get_code_template(language: str = "python", template_type: str = "function") -> str:
    """Get a code template for common patterns
    
    Args:
        language: Programming language
        template_type: Type of template (function, class, script)
        
    Returns:
        Code template string
    """
    templates = {
        "python": {
            "function": '''def {function_name}({parameters}):
    """Function that {description}.
    
    Args:
        {args_description}
    
    Returns:
        {return_description}
    """
    pass''',
            "class": '''class {class_name}:
    """Class that {description}.
    
    Attributes:
        {attributes_description}
    """
    
    def __init__(self, {init_parameters}):
        """Initialize {class_name}.
        
        Args:
            {init_args_description}
        """
        pass
    
    def {method_name}(self, {method_parameters}):
        """Method that {method_description}.
        
        Args:
            {method_args_description}
        
        Returns:
            {method_return_description}
        """
        pass''',
            "script": '''#!/usr/bin/env python3
"""
{script_description}
"""

import argparse
import sys


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="{script_description}")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    pass


if __name__ == "__main__":
    main()'''
        },
        "javascript": {
            "function": '''/**
 * Function that {description}
 * @param {{type}} {parameter} - {parameter_description}
 * @returns {{type}} {return_description}
 */
function {function_name}({parameters}) {{
    // Implementation here
}}''',
            "class": '''/**
 * Class that {description}
 */
class {class_name} {{
    /**
     * Create a {class_name}
     * @param {{type}} {parameter} - {parameter_description}
     */
    constructor({constructor_parameters}) {{
        // Initialize properties
    }}
    
    /**
     * Method that {method_description}
     * @param {{type}} {parameter} - {parameter_description}
     * @returns {{type}} {return_description}
     */
    {method_name}({method_parameters}) {{
        // Implementation here
    }}
}}''',
            "script": '''#!/usr/bin/env node

/**
 * {script_description}
 */

const args = process.argv.slice(2);

function main() {
    // Your code here
}

if (require.main === module) {
    main();
}'''
        }
    }
    
    lang_templates = templates.get(language.lower(), templates["python"])
    return lang_templates.get(template_type, lang_templates["function"])
