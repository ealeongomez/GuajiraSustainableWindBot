"""
Code Agent Module - Text-to-Python Multi-Agent System
======================================================

This module provides a multi-agent system for wind data analysis
using text-to-python methodology for zero-hallucination responses.

Main Components:
- DataManager: Loads and caches municipality data
- SafePythonREPL: Secure Python code execution environment
- SupervisorAgent: Routes queries to appropriate agents
- CodeMunicipalityAgent: Municipality-specific data analysis
- GeneralAgent: Handles conceptual questions
- CodeMultiAgentSystem: Orchestrates all agents

Author: Eder Arley León Gómez
Date: 2025-10-19
"""

from .data_manager import DataManager
from .safe_repl import SafePythonREPL
from .supervisor import SupervisorAgent
from .municipality_agent import CodeMunicipalityAgent
from .general_agent import GeneralAgent
from .system import CodeMultiAgentSystem

__all__ = [
    'DataManager',
    'SafePythonREPL',
    'SupervisorAgent',
    'CodeMunicipalityAgent',
    'GeneralAgent',
    'CodeMultiAgentSystem'
]

__version__ = '1.0.0'

