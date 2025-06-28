from typing import Dict, Any, List
from pydantic import BaseModel


class CodeGenerationPrompt(BaseModel):
    description: str
    language: str = "python"
    style: str = "clean"
    include_tests: bool = False
    include_docs: bool = True


class GeneratedPrompt(BaseModel):
    prompt: str
    context: Dict[str, Any]
    suggestions: List[str]


def generate_code_prompt(
    description: str,
    language: str = "python",
    style: str = "clean",
    include_tests: bool = False,
    include_docs: bool = True
) -> GeneratedPrompt:
    """Generate a structured prompt for code generation"""
    
    base_prompt = f"""Generate {language} code that {description}.

Requirements:
- Write clean, readable, and well-structured code
- Follow {language} best practices and conventions
- Use appropriate variable and function names
- Handle edge cases and errors appropriately"""
    
    if style == "functional":
        base_prompt += "\n- Prefer functional programming patterns where appropriate"
    elif style == "object-oriented":
        base_prompt += "\n- Use object-oriented design principles"
    elif style == "clean":
        base_prompt += "\n- Focus on simplicity and clarity"
    
    if include_docs:
        base_prompt += "\n- Include comprehensive docstrings and comments"
    
    if include_tests:
        base_prompt += "\n- Include unit tests for the main functionality"
    
    context = {
        "language": language,
        "style": style,
        "include_tests": include_tests,
        "include_docs": include_docs,
        "description": description
    }
    
    suggestions = [
        "Consider using type hints for better code clarity",
        "Add input validation for robustness",
        "Think about performance implications",
        "Consider logging for debugging purposes"
    ]
    
    if language.lower() == "python":
        suggestions.extend([
            "Follow PEP 8 style guidelines",
            "Use virtual environments for dependencies",
            "Consider using dataclasses or pydantic for data structures"
        ])
    
    return GeneratedPrompt(
        prompt=base_prompt,
        context=context,
        suggestions=suggestions
    )


def get_code_template(language: str, template_type: str) -> str:
    """Get a code template for common patterns"""
    
    templates = {
        "python": {
            "class": '''class {ClassName}:
    """A class that {description}."""
    
    def __init__(self):
        pass
    
    def {method_name}(self):
        """Method that {method_description}."""
        pass''',
            
            "function": '''def {function_name}({parameters}):
    """Function that {description}.
    
    Args:
        {args_description}
    
    Returns:
        {return_description}
    """
    pass''',
            
            "script": '''#!/usr/bin/env python3
"""
{script_description}
"""

import argparse
import logging


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="{script_description}")
    args = parser.parse_args()
    
    pass


if __name__ == "__main__":
    main()'''
        }
    }
    
    return templates.get(language, {}).get(template_type, "# Template not found")
