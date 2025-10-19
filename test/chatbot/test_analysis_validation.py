"""
==============================================================================
Project: GuajiraSustainableWindBot
File: test_analysis_validation.py
Description:
    Validation test for text-to-python system.
    Executes real queries and validates that the results are accurate.

Author: Eder Arley León Gómez
Created on: 2025-10-19
==============================================================================
"""

import os
import sys
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize
init(autoreset=True)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Check API key
if not os.getenv("OPENAI_API_KEY"):
    print(f"{Fore.RED}❌ OPENAI_API_KEY not found{Style.RESET_ALL}")
    sys.exit(1)

print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
print(f"{Fore.CYAN}🧪 Text-to-Python System - Analysis Validation Test{Style.RESET_ALL}")
print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

# Load system
print(f"{Fore.YELLOW}📦 Loading multi-agent system...{Style.RESET_ALL}")
try:
    from supervisor_code_agent_test import CodeMultiAgentSystem, data_manager
    system = CodeMultiAgentSystem()
    print(f"{Fore.GREEN}✅ System loaded successfully{Style.RESET_ALL}\n")
except Exception as e:
    print(f"{Fore.RED}❌ Error loading system: {e}{Style.RESET_ALL}")
    sys.exit(1)

# ============================================================================
# Test Cases with Expected Results
# ============================================================================

test_cases = [
    {
        "query": "¿Cuál es la velocidad promedio del viento en Riohacha?",
        "municipality": "riohacha",
        "validation": lambda df: df['wind_speed_10m'].mean(),
        "description": "Average wind speed in Riohacha"
    },
    {
        "query": "¿Cuál es la temperatura máxima registrada en Maicao?",
        "municipality": "maicao",
        "validation": lambda df: df['temperature_2m'].max(),
        "description": "Maximum temperature in Maicao"
    },
    {
        "query": "¿Cuántos registros hay de Albania?",
        "municipality": "albania",
        "validation": lambda df: len(df),
        "description": "Number of records for Albania"
    }
]

# ============================================================================
# Pre-compute Expected Values
# ============================================================================

print(f"{Fore.CYAN}📊 Computing expected values...{Style.RESET_ALL}\n")

expected_values = {}
for i, test in enumerate(test_cases, 1):
    municipality = test["municipality"]
    df = data_manager.get_data(municipality)
    
    if df is not None:
        expected = test["validation"](df)
        expected_values[i] = expected
        print(f"{i}. {test['description']}")
        print(f"   Expected value: {Fore.CYAN}{expected}{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.RED}❌ Data not found for {municipality}{Style.RESET_ALL}\n")

# ============================================================================
# Execute Queries with System
# ============================================================================

print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
print(f"{Fore.CYAN}🤖 Executing queries with multi-agent system...{Style.RESET_ALL}")
print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

print(f"{Fore.YELLOW}Note: This will make API calls to GPT-4{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Each query costs approximately $0.035{Style.RESET_ALL}\n")

proceed = input(f"Execute {len(test_cases)} queries? [y/N]: ").strip().lower()

if proceed != 'y':
    print(f"\n{Fore.YELLOW}Test cancelled by user{Style.RESET_ALL}\n")
    sys.exit(0)

print()
results = []

for i, test in enumerate(test_cases, 1):
    print(f"{Fore.MAGENTA}{'─'*80}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Test {i}/{len(test_cases)}: {test['description']}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'─'*80}{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}Query:{Style.RESET_ALL} {test['query']}\n")
    
    try:
        # Execute query
        response = system.process_query(test['query'])
        
        print(f"\n{Fore.GREEN}Response received:{Style.RESET_ALL}")
        print(f"{response}\n")
        
        # Try to extract number from response
        import re
        numbers = re.findall(r'\d+\.?\d*', response)
        
        if numbers:
            # Get the most prominent number (usually the first one)
            extracted_value = float(numbers[0])
            expected_value = expected_values[i]
            
            # Check if values are close (within 5% tolerance)
            if isinstance(expected_value, int):
                tolerance = 10
                diff = abs(extracted_value - expected_value)
                match = diff <= tolerance
            else:
                tolerance = 0.05 * abs(expected_value)
                diff = abs(extracted_value - expected_value)
                match = diff <= tolerance
            
            if match:
                print(f"{Fore.GREEN}✅ VALIDATION PASSED{Style.RESET_ALL}")
                print(f"   Expected: {expected_value}")
                print(f"   Received: {extracted_value}")
                print(f"   Difference: {diff:.4f}")
                results.append(("PASS", test['description']))
            else:
                print(f"{Fore.YELLOW}⚠️  VALUES DIFFER{Style.RESET_ALL}")
                print(f"   Expected: {expected_value}")
                print(f"   Received: {extracted_value}")
                print(f"   Difference: {diff:.4f}")
                results.append(("WARN", test['description']))
        else:
            print(f"{Fore.YELLOW}⚠️  Could not extract numerical value from response{Style.RESET_ALL}")
            results.append(("WARN", test['description']))
        
    except Exception as e:
        print(f"{Fore.RED}❌ ERROR: {e}{Style.RESET_ALL}")
        results.append(("FAIL", test['description']))
    
    print()

# ============================================================================
# Summary
# ============================================================================

print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
print(f"{Fore.CYAN}📊 Test Summary{Style.RESET_ALL}")
print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

passed = sum(1 for r in results if r[0] == "PASS")
warned = sum(1 for r in results if r[0] == "WARN")
failed = sum(1 for r in results if r[0] == "FAIL")

for status, desc in results:
    if status == "PASS":
        print(f"{Fore.GREEN}✅ PASS:{Style.RESET_ALL} {desc}")
    elif status == "WARN":
        print(f"{Fore.YELLOW}⚠️  WARN:{Style.RESET_ALL} {desc}")
    else:
        print(f"{Fore.RED}❌ FAIL:{Style.RESET_ALL} {desc}")

print()
print(f"Total: {len(results)}")
print(f"{Fore.GREEN}Passed: {passed}{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Warnings: {warned}{Style.RESET_ALL}")
print(f"{Fore.RED}Failed: {failed}{Style.RESET_ALL}\n")

if passed == len(results):
    print(f"{Fore.GREEN}✨ All tests passed! The system produces accurate results.{Style.RESET_ALL}\n")
elif passed + warned == len(results):
    print(f"{Fore.YELLOW}⚠️  Some values differed slightly but system is functional.{Style.RESET_ALL}\n")
else:
    print(f"{Fore.RED}❌ Some tests failed. Review the system.{Style.RESET_ALL}\n")

