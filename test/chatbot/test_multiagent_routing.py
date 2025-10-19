"""
==============================================================================
Project: GuajiraSustainableWindBot
File: test_multiagent_routing.py
Description:
    Automated tests for the multi-agent supervisor system.
    Tests routing logic, agent selection, and response generation.

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

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Verify OPENAI_API_KEY exists
if not os.getenv("OPENAI_API_KEY"):
    print(f"{Fore.RED}❌ Error: OPENAI_API_KEY not found in .env file{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Please add your OpenAI API key to .env{Style.RESET_ALL}")
    sys.exit(1)

# Import the multi-agent system
try:
    from supervisor_multiagent_test import MultiAgentSystem
except ImportError as e:
    print(f"{Fore.RED}❌ Error importing MultiAgentSystem: {e}{Style.RESET_ALL}")
    sys.exit(1)

# ==============================================================================================
# Test Cases
# ==============================================================================================

TEST_CASES = [
    {
        "category": "Specific Municipality",
        "queries": [
            "¿Cuál es la velocidad promedio del viento en Riohacha?",
            "Dame información sobre el clima en Maicao",
            "¿Cómo es el viento en Albania?",
            "Háblame sobre Uribia"
        ],
        "expected_routing": "specific"
    },
    {
        "category": "General Knowledge",
        "queries": [
            "¿Qué es un modelo LSTM?",
            "¿Cómo funciona la energía eólica?",
            "Explica qué es la sostenibilidad",
            "¿Qué es la predicción de series temporales?"
        ],
        "expected_routing": "general"
    },
    {
        "category": "Multi-Municipality",
        "queries": [
            "Compara Riohacha con Maicao",
            "¿Qué municipio tiene mayor viento: Albania o Uribia?",
            "Diferencias entre Manaure y Fonseca"
        ],
        "expected_routing": "multiple"
    }
]

# ==============================================================================================
# Test Functions
# ==============================================================================================

def test_supervisor_routing():
    """
    Test that the supervisor correctly routes queries.
    """
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🧪 Testing Multi-Agent Supervisor Routing{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    try:
        # Initialize system
        print(f"{Fore.YELLOW}⏳ Initializing Multi-Agent System...{Style.RESET_ALL}")
        system = MultiAgentSystem()
        print(f"{Fore.GREEN}✅ System initialized successfully{Style.RESET_ALL}\n")
        
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        for test_case in TEST_CASES:
            category = test_case["category"]
            queries = test_case["queries"]
            expected_routing = test_case["expected_routing"]
            
            print(f"\n{Fore.MAGENTA}📋 Category: {category}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}{'─'*70}{Style.RESET_ALL}")
            
            for query in queries:
                total_tests += 1
                print(f"\n{Fore.CYAN}Query {total_tests}:{Style.RESET_ALL} {query}")
                
                try:
                    # Test routing
                    routing = system.supervisor.route_query(query)
                    actual_routing = routing["type"]
                    
                    # Check if routing matches expected
                    if actual_routing == expected_routing:
                        print(f"{Fore.GREEN}✅ PASS - Routed to: {actual_routing}{Style.RESET_ALL}")
                        passed_tests += 1
                    else:
                        print(f"{Fore.RED}❌ FAIL - Expected: {expected_routing}, Got: {actual_routing}{Style.RESET_ALL}")
                        failed_tests += 1
                    
                    # Show municipalities if applicable
                    if routing["municipalities"]:
                        print(f"   {Fore.YELLOW}📍 Municipalities: {', '.join(routing['municipalities'])}{Style.RESET_ALL}")
                    
                except Exception as e:
                    print(f"{Fore.RED}❌ ERROR: {e}{Style.RESET_ALL}")
                    failed_tests += 1
        
        # Summary
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 Test Summary{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"Total Tests:  {total_tests}")
        print(f"{Fore.GREEN}Passed:       {passed_tests}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed:       {failed_tests}{Style.RESET_ALL}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%\n")
        
        return passed_tests, failed_tests
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ Fatal error during testing: {e}{Style.RESET_ALL}\n")
        return 0, 1


def test_full_response_generation():
    """
    Test complete response generation for sample queries.
    """
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🧪 Testing Full Response Generation{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    try:
        system = MultiAgentSystem()
        
        sample_queries = [
            "¿Cuál es el promedio de viento en Riohacha?",
            "¿Qué es energía eólica?",
        ]
        
        for i, query in enumerate(sample_queries, 1):
            print(f"\n{Fore.MAGENTA}Test {i}/{len(sample_queries)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Query:{Style.RESET_ALL} {query}")
            print(f"{Fore.YELLOW}{'─'*70}{Style.RESET_ALL}")
            
            try:
                response = system.process_query(query)
                print(f"{Fore.GREEN}Response:{Style.RESET_ALL}")
                print(response[:200] + "..." if len(response) > 200 else response)
                print(f"{Fore.GREEN}✅ Response generated successfully{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}❌ Error generating response: {e}{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}✅ Full response generation test completed{Style.RESET_ALL}\n")
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ Fatal error: {e}{Style.RESET_ALL}\n")


def test_data_availability():
    """
    Test that municipality data is accessible.
    """
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🧪 Testing Data Availability{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    from supervisor_multiagent_test import MUNICIPALITIES, load_municipality_data
    
    available = 0
    missing = 0
    
    for municipality in MUNICIPALITIES:
        data = load_municipality_data(municipality)
        if data is not None:
            print(f"{Fore.GREEN}✅ {municipality}: {len(data)} records{Style.RESET_ALL}")
            available += 1
        else:
            print(f"{Fore.RED}❌ {municipality}: No data found{Style.RESET_ALL}")
            missing += 1
    
    print(f"\n{Fore.CYAN}Data Availability Summary:{Style.RESET_ALL}")
    print(f"Available: {available}/{len(MUNICIPALITIES)}")
    print(f"Missing:   {missing}/{len(MUNICIPALITIES)}\n")


# ==============================================================================================
# Main Execution
# ==============================================================================================

def run_all_tests():
    """
    Run all test suites.
    """
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🚀 Multi-Agent System Test Suite{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    # Test 1: Data availability
    test_data_availability()
    
    # Test 2: Supervisor routing
    passed, failed = test_supervisor_routing()
    
    # Test 3: Full response generation (optional - costs API calls)
    run_full_test = input(f"\n{Fore.YELLOW}Run full response generation test? (costs API tokens) [y/N]: {Style.RESET_ALL}").strip().lower()
    if run_full_test == 'y':
        test_full_response_generation()
    else:
        print(f"{Fore.YELLOW}Skipping full response generation test{Style.RESET_ALL}")
    
    # Final summary
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🏁 All Tests Completed{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    if failed == 0:
        print(f"{Fore.GREEN}✨ All routing tests passed! System is ready.{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.YELLOW}⚠️  Some tests failed. Review supervisor routing logic.{Style.RESET_ALL}\n")


if __name__ == "__main__":
    run_all_tests()

