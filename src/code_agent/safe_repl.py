"""
Safe Python REPL - Secure code execution environment
"""

import sys
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from io import StringIO
from typing import Dict, Any

from .config import OUTPUT_DIR


class SafePythonREPL:
    """Safe Python REPL with access to preloaded municipality data."""
    
    def __init__(self, data_manager):
        """
        Initialize Safe Python REPL.
        
        Args:
            data_manager: DataManager instance with loaded data
        """
        self.data_manager = data_manager
        self.globals = {
            'pd': pd,
            'plt': plt,
            'data_manager': data_manager,
            'OUTPUT_DIR': OUTPUT_DIR,
            'Path': Path,
            '__builtins__': {
                'print': print,
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'round': round,
                'sum': sum,
                'min': min,
                'max': max,
                'abs': abs,
                'range': range,
                'list': list,
                'dict': dict,
                'tuple': tuple,
            }
        }
        
        # Add all municipality dataframes to globals
        for municipality, df in data_manager.get_all_data().items():
            self.globals[f'df_{municipality}'] = df
    
    def run(self, code: str) -> str:
        """
        Execute Python code safely and return result.
        
        Args:
            code: Python code to execute
            
        Returns:
            Output string from code execution
        """
        try:
            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            # Execute code
            exec(code, self.globals)
            
            # Restore stdout
            sys.stdout = old_stdout
            
            # Get output
            output = captured_output.getvalue()
            
            if output:
                return output.strip()
            else:
                return "Código ejecutado exitosamente (sin output)"
                
        except Exception as e:
            sys.stdout = old_stdout
            error_msg = f"Error ejecutando código:\n{type(e).__name__}: {str(e)}"
            return error_msg

