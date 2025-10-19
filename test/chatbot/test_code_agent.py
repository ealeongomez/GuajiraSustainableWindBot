"""
==============================================================================
Project: GuajiraSustainableWindBot
File: test_code_agent.py
Description:
    Test suite for the text-to-python multi-agent system.
    Validates code generation, execution, and result formatting.

Author: Eder Arley León Gómez
Created on: 2025-10-19
==============================================================================
"""

# ==============================================================================================
# Libraries 
# ==============================================================================================

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Verify OPENAI_API_KEY
if not os.getenv("OPENAI_API_KEY"):
    print(f"{Fore.RED}❌ Error: OPENAI_API_KEY not found in .env{Style.RESET_ALL}")
    sys.exit(1)

# ==============================================================================================
# Test Cases
# ==============================================================================================

TEST_QUERIES = [
    {
        "category": "Consultas de Datos Simples",
        "queries": [
            "¿Cuál es la velocidad promedio del viento en Riohacha?",
            "¿Cuál es la temperatura máxima registrada en Maicao?",
            "¿Cuántos registros tenemos de Albania?",
            "¿Cuál es la humedad promedio en Uribia?"
        ],
        "expected_type": "data_query",
        "expected_code": True
    },
    {
        "category": "Consultas Generales",
        "queries": [
            "¿Qué es un modelo LSTM?",
            "¿Cómo funciona la energía eólica?",
            "Explica la sostenibilidad energética"
        ],
        "expected_type": "general",
        "expected_code": False
    },
    {
        "category": "Análisis Complejos",
        "queries": [
            "Compara el viento promedio entre Riohacha y Maicao",
            "¿Qué municipio tiene mayor velocidad de viento?",
            "¿Cuál es la correlación entre temperatura y viento en Albania?"
        ],
        "expected_type": "comparison",
        "expected_code": True
    }
]

# ==============================================================================================
# Tests
# ==============================================================================================

def test_supervisor_routing():
    """Test supervisor routing logic."""
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🧪 Test 1: Supervisor Routing{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    try:
        from supervisor_code_agent_test import SupervisorAgent, supervisor_llm
        
        supervisor = SupervisorAgent(supervisor_llm)
        
        total_tests = 0
        passed_tests = 0
        
        for test_case in TEST_QUERIES:
            category = test_case["category"]
            queries = test_case["queries"]
            expected_code = test_case["expected_code"]
            
            print(f"\n{Fore.MAGENTA}📋 {category}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}{'─'*70}{Style.RESET_ALL}")
            
            for query in queries[:2]:  # Test first 2 of each category to save API calls
                total_tests += 1
                print(f"\n{Fore.CYAN}Query:{Style.RESET_ALL} {query}")
                
                try:
                    routing = supervisor.route_query(query)
                    
                    print(f"  Tipo: {routing['type']}")
                    print(f"  Municipios: {routing['municipalities']}")
                    print(f"  Necesita código: {routing['needs_code']}")
                    
                    if routing['needs_code'] == expected_code:
                        print(f"{Fore.GREEN}  ✅ PASS{Style.RESET_ALL}")
                        passed_tests += 1
                    else:
                        print(f"{Fore.RED}  ❌ FAIL - Expected code={expected_code}, got {routing['needs_code']}{Style.RESET_ALL}")
                        
                except Exception as e:
                    print(f"{Fore.RED}  ❌ ERROR: {e}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 Routing Test Summary{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"Total:  {total_tests}")
        print(f"{Fore.GREEN}Passed: {passed_tests}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {total_tests - passed_tests}{Style.RESET_ALL}\n")
        
        return passed_tests, total_tests - passed_tests
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ Fatal error: {e}{Style.RESET_ALL}\n")
        import traceback
        print(traceback.format_exc())
        return 0, 1


def test_code_execution():
    """Test Python code generation and execution."""
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🧪 Test 2: Code Generation & Execution{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    try:
        from supervisor_code_agent_test import CodeMunicipalityAgent, agent_llm, data_manager
        
        # Test with Riohacha
        agent = CodeMunicipalityAgent("riohacha", agent_llm, data_manager)
        
        test_query = "¿Cuál es la velocidad promedio del viento?"
        
        print(f"{Fore.CYAN}Consulta de prueba:{Style.RESET_ALL} {test_query}")
        print(f"{Fore.CYAN}Municipio:{Style.RESET_ALL} Riohacha\n")
        
        response = agent.answer(test_query)
        
        print(f"\n{Fore.GREEN}Respuesta generada:{Style.RESET_ALL}")
        print(response)
        
        if response and "error" not in response.lower():
            print(f"\n{Fore.GREEN}✅ Test de ejecución de código: PASS{Style.RESET_ALL}\n")
            return 1, 0
        else:
            print(f"\n{Fore.RED}❌ Test de ejecución de código: FAIL{Style.RESET_ALL}\n")
            return 0, 1
            
    except Exception as e:
        print(f"\n{Fore.RED}❌ Fatal error: {e}{Style.RESET_ALL}\n")
        import traceback
        print(traceback.format_exc())
        return 0, 1


def test_data_availability():
    """Test that municipality data is loaded."""
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🧪 Test 3: Data Availability{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    try:
        from supervisor_code_agent_test import data_manager, MUNICIPALITIES
        
        available = 0
        for municipality in MUNICIPALITIES:
            df = data_manager.get_data(municipality)
            if df is not None and len(df) > 0:
                print(f"{Fore.GREEN}✅ {municipality}: {len(df):,} registros{Style.RESET_ALL}")
                available += 1
            else:
                print(f"{Fore.RED}❌ {municipality}: No data{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Disponibilidad: {available}/{len(MUNICIPALITIES)}{Style.RESET_ALL}\n")
        
        if available == len(MUNICIPALITIES):
            return available, 0
        else:
            return available, len(MUNICIPALITIES) - available
            
    except Exception as e:
        print(f"\n{Fore.RED}❌ Fatal error: {e}{Style.RESET_ALL}\n")
        return 0, 1


# ==============================================================================================
# Main Test Runner
# ==============================================================================================

def run_all_tests():
    """Run all test suites."""
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🚀 Text-to-Python Multi-Agent Test Suite{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    total_passed = 0
    total_failed = 0
    
    # Test 1: Data availability
    passed, failed = test_data_availability()
    total_passed += passed
    total_failed += failed
    
    # Test 2: Supervisor routing
    run_routing = input(f"\n{Fore.YELLOW}¿Ejecutar test de routing? (consume API tokens) [y/N]: {Style.RESET_ALL}").strip().lower()
    if run_routing == 'y':
        passed, failed = test_supervisor_routing()
        total_passed += passed
        total_failed += failed
    else:
        print(f"{Fore.YELLOW}Saltando test de routing{Style.RESET_ALL}")
    
    # Test 3: Code execution
    run_code = input(f"\n{Fore.YELLOW}¿Ejecutar test de ejecución de código? (consume API tokens) [y/N]: {Style.RESET_ALL}").strip().lower()
    if run_code == 'y':
        passed, failed = test_code_execution()
        total_passed += passed
        total_failed += failed
    else:
        print(f"{Fore.YELLOW}Saltando test de código{Style.RESET_ALL}")
    
    # Final summary
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🏁 Test Summary{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Passed: {total_passed}{Style.RESET_ALL}")
    print(f"{Fore.RED}Failed: {total_failed}{Style.RESET_ALL}")
    
    if total_failed == 0:
        print(f"\n{Fore.GREEN}✨ All tests passed! System ready.{Style.RESET_ALL}\n")
    else:
        print(f"\n{Fore.YELLOW}⚠️  Some tests failed. Review logs above.{Style.RESET_ALL}\n")


if __name__ == "__main__":
    run_all_tests()

