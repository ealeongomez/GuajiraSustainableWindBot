"""
Prompt Templates Module
========================

This module contains prompt templates for the GuajiraSustainableWindBot project.

Available templates:
- windbot_prompt.txt: Main conversational prompt for WindBot
"""

from pathlib import Path


PROMPT_DIR = Path(__file__).parent


def load_prompt(prompt_name: str) -> str:
    """
    Load a prompt template from file.
    
    Args:
        prompt_name (str): Name of the prompt file (without .txt extension)
        
    Returns:
        str: Content of the prompt template
        
    Raises:
        FileNotFoundError: If the prompt file doesn't exist
    """
    prompt_path = PROMPT_DIR / f"{prompt_name}.txt"
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt template '{prompt_name}' not found at {prompt_path}")
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


def list_prompts() -> list:
    """
    List all available prompt templates.
    
    Returns:
        list: List of available prompt template names
    """
    return [p.stem for p in PROMPT_DIR.glob("*.txt")]
