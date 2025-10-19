"""
==============================================================================
Project: GuajiraSustainableWindBot
File: test_main.py
Description:
    Comprehensive test suite for main.py to ensure all components
    are working correctly before deployment.

Tests:
    1. Environment variables validation
    2. Import integrity
    3. Handler functionality
    4. CodeMultiAgentSystem initialization
    5. Configuration validation
    6. Integration checks

Usage:
    python test_main.py

Author: Eder Arley León Gómez
Created on: 2025-10-19
==============================================================================
"""

# ==============================================================================================
# Libraries 
# ==============================================================================================

import os
import sys
import warnings
from pathlib import Path
from dotenv import load_dotenv

# Try to import colorama, if not available use plain text
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    # Create dummy classes for when colorama is not available
    class DummyColor:
        def __getattr__(self, name):
            return ''
    Fore = DummyColor()
    Style = DummyColor()

# Project root is current directory (since test_main.py is in root)
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Disable warnings
warnings.filterwarnings("ignore")

# Load environment variables
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# ==============================================================================================
# Test Functions
# ==============================================================================================

def print_header(text):
    """Print a formatted header"""
    if HAS_COLOR:
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    else:
        print(f"\n{'='*80}")
        print(f"{text}")
        print(f"{'='*80}\n")


def print_test(test_name):
    """Print test name"""
    if HAS_COLOR:
        print(f"{Fore.YELLOW}🧪 Testing: {test_name}{Style.RESET_ALL}")
    else:
        print(f"🧪 Testing: {test_name}")


def print_success(message):
    """Print success message"""
    if HAS_COLOR:
        print(f"{Fore.GREEN}   ✅ {message}{Style.RESET_ALL}")
    else:
        print(f"   ✅ {message}")


def print_error(message):
    """Print error message"""
    if HAS_COLOR:
        print(f"{Fore.RED}   ❌ {message}{Style.RESET_ALL}")
    else:
        print(f"   ❌ {message}")


def print_warning(message):
    """Print warning message"""
    if HAS_COLOR:
        print(f"{Fore.YELLOW}   ⚠️  {message}{Style.RESET_ALL}")
    else:
        print(f"   ⚠️  {message}")


def test_environment_variables():
    """Test 1: Validate environment variables"""
    print_header("Test 1: Environment Variables")
    
    errors = []
    warnings_list = []
    
    # Required variables
    print_test("Required Environment Variables")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print_success(f"OPENAI_API_KEY found ({openai_key[:10]}...)")
    else:
        errors.append("OPENAI_API_KEY not found")
        print_error("OPENAI_API_KEY not found in .env")
    
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if telegram_token:
        print_success(f"TELEGRAM_BOT_TOKEN found ({telegram_token[:10]}...)")
    else:
        errors.append("TELEGRAM_BOT_TOKEN not found")
        print_error("TELEGRAM_BOT_TOKEN not found in .env")
    
    # Optional variables
    print_test("Optional Environment Variables")
    
    mongodb_uri = os.getenv("MONGODB_URI")
    if mongodb_uri:
        print_success(f"MONGODB_URI configured")
    else:
        warnings_list.append("MONGODB_URI not configured")
        print_warning("MONGODB_URI not configured (conversations won't persist)")
    
    langchain_key = os.getenv("LANGCHAIN_API_KEY")
    if langchain_key:
        print_success(f"LANGCHAIN_API_KEY configured")
    else:
        warnings_list.append("LANGCHAIN_API_KEY not configured")
        print_warning("LANGCHAIN_API_KEY not configured (no tracing)")
    
    return len(errors) == 0, errors, warnings_list


def test_imports():
    """Test 2: Validate all imports"""
    print_header("Test 2: Import Integrity")
    
    errors = []
    
    # Test main.py imports
    print_test("Main Telegram Libraries")
    try:
        from telegram import Update
        from telegram.ext import Application, CommandHandler, MessageHandler, filters
        print_success("Telegram libraries imported successfully")
    except ImportError as e:
        errors.append(f"Telegram import error: {e}")
        print_error(f"Failed to import Telegram libraries: {e}")
    
    # Test config import
    print_test("Telegram Bot Config")
    try:
        from src.telegram_bot.config import TELEGRAM_BOT_TOKEN
        print_success("Config imported successfully")
    except ImportError as e:
        errors.append(f"Config import error: {e}")
        print_error(f"Failed to import config: {e}")
    
    # Test handlers import
    print_test("Code Agent Handlers")
    try:
        from src.telegram_bot.code_agent_handlers import (
            start_command_code,
            help_command_code,
            clear_command_code,
            handle_message_code,
            error_handler_code
        )
        print_success("All handlers imported successfully")
        
        # Validate handlers are callable
        handlers = [
            start_command_code,
            help_command_code,
            clear_command_code,
            handle_message_code,
            error_handler_code
        ]
        for handler in handlers:
            if not callable(handler):
                errors.append(f"{handler.__name__} is not callable")
                print_error(f"{handler.__name__} is not callable")
            else:
                print_success(f"  - {handler.__name__} is callable")
                
    except ImportError as e:
        errors.append(f"Handlers import error: {e}")
        print_error(f"Failed to import handlers: {e}")
    
    return len(errors) == 0, errors


def test_code_agent_system():
    """Test 3: Validate CodeMultiAgentSystem"""
    print_header("Test 3: CodeMultiAgentSystem Initialization")
    
    errors = []
    
    print_test("CodeMultiAgentSystem Import")
    try:
        from src.code_agent import CodeMultiAgentSystem
        print_success("CodeMultiAgentSystem imported successfully")
    except ImportError as e:
        errors.append(f"CodeMultiAgentSystem import error: {e}")
        print_error(f"Failed to import CodeMultiAgentSystem: {e}")
        return False, errors
    
    print_test("CodeMultiAgentSystem Initialization")
    try:
        system = CodeMultiAgentSystem(verbose=False)
        print_success("CodeMultiAgentSystem initialized successfully")
        
        # Test system has required attributes
        print_test("System Components")
        if hasattr(system, 'supervisor'):
            print_success("  - Supervisor agent found")
        else:
            errors.append("Supervisor agent not found")
            print_error("  - Supervisor agent not found")
        
        if hasattr(system, 'municipality_agents'):
            print_success(f"  - {len(system.municipality_agents)} municipality agents found")
            if len(system.municipality_agents) != 13:
                errors.append(f"Expected 13 municipality agents, found {len(system.municipality_agents)}")
                print_warning(f"  - Expected 13 municipality agents, found {len(system.municipality_agents)}")
        else:
            errors.append("Municipality agents not found")
            print_error("  - Municipality agents not found")
        
        if hasattr(system, 'general_agent'):
            print_success("  - General agent found")
        else:
            errors.append("General agent not found")
            print_error("  - General agent not found")
            
    except Exception as e:
        errors.append(f"CodeMultiAgentSystem initialization error: {e}")
        print_error(f"Failed to initialize CodeMultiAgentSystem: {e}")
    
    return len(errors) == 0, errors


def test_data_files():
    """Test 4: Validate data files"""
    print_header("Test 4: Data Files Validation")
    
    errors = []
    warnings_list = []
    
    print_test("Municipality Data Files")
    
    data_dir = project_root / "data" / "raw"
    if not data_dir.exists():
        errors.append("data/raw directory not found")
        print_error("data/raw directory not found")
        return False, errors, warnings_list
    
    municipalities = [
        "albania", "barrancas", "distraccion", "el_molino", "fonseca",
        "hatonuevo", "la_jagua_del_pilar", "maicao", "manaure", "mingueo",
        "riohacha", "san_juan_del_cesar", "uribia"
    ]
    
    found_count = 0
    for municipality in municipalities:
        csv_file = data_dir / f"open_meteo_{municipality}.csv"
        if csv_file.exists():
            print_success(f"  - {municipality}.csv found")
            found_count += 1
        else:
            warnings_list.append(f"{municipality}.csv not found")
            print_warning(f"  - {municipality}.csv not found")
    
    print_success(f"Found {found_count}/{len(municipalities)} municipality data files")
    
    if found_count == 0:
        errors.append("No municipality data files found")
        print_error("No municipality data files found - system won't work")
    
    return len(errors) == 0, errors, warnings_list


def test_output_directory():
    """Test 5: Validate output directory"""
    print_header("Test 5: Output Directory")
    
    errors = []
    
    print_test("Graph Output Directory")
    
    output_dir = project_root / "test" / "chatbot" / "output"
    if output_dir.exists():
        print_success(f"Output directory exists: {output_dir}")
    else:
        print_warning(f"Output directory doesn't exist: {output_dir}")
        print_warning("Creating output directory...")
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            print_success("Output directory created successfully")
        except Exception as e:
            errors.append(f"Failed to create output directory: {e}")
            print_error(f"Failed to create output directory: {e}")
    
    return len(errors) == 0, errors


def test_mongodb_connection():
    """Test 6: Test MongoDB connection (optional)"""
    print_header("Test 6: MongoDB Connection (Optional)")
    
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        print_warning("MONGODB_URI not configured - skipping test")
        return True, []
    
    errors = []
    
    print_test("MongoDB Manager Import")
    try:
        from src.telegram_bot.mongodb_manager import get_mongodb_manager
        print_success("MongoDB manager imported successfully")
        
        print_test("MongoDB Connection")
        mongodb = get_mongodb_manager()
        if mongodb:
            print_success("MongoDB manager initialized successfully")
            
            # Test connection
            try:
                stats = mongodb.get_statistics()
                print_success(f"MongoDB connected - Total conversations: {stats.get('total_conversations', 0)}")
            except Exception as e:
                print_warning(f"MongoDB connected but query failed: {e}")
        else:
            print_warning("MongoDB manager returned None (might be disabled)")
            
    except Exception as e:
        errors.append(f"MongoDB test error: {e}")
        print_warning(f"MongoDB test failed: {e}")
        print_warning("Bot will work without MongoDB (no persistence)")
    
    return True, errors  # Don't fail on MongoDB errors


def test_simple_query():
    """Test 7: Test a simple query"""
    print_header("Test 7: Simple Query Test")
    
    errors = []
    
    print_test("Initializing CodeMultiAgentSystem")
    try:
        from src.code_agent import CodeMultiAgentSystem
        system = CodeMultiAgentSystem(verbose=False)
        print_success("System initialized")
        
        print_test("Processing test query")
        test_query = "¿Qué es la energía eólica?"
        print(f"   Query: '{test_query}'")
        
        try:
            response = system.process_query(test_query, verbose=False)
            if response and len(response) > 0:
                print_success(f"Response received ({len(response)} characters)")
                if HAS_COLOR:
                    print(f"\n{Fore.BLUE}   Response preview:{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}   {response[:200]}...{Style.RESET_ALL}\n")
                else:
                    print(f"\n   Response preview:")
                    print(f"   {response[:200]}...\n")
            else:
                errors.append("Empty response received")
                print_error("Empty response received")
        except Exception as e:
            errors.append(f"Query processing error: {e}")
            print_error(f"Query processing failed: {e}")
            
    except Exception as e:
        errors.append(f"System initialization error: {e}")
        print_error(f"System initialization failed: {e}")
    
    return len(errors) == 0, errors


# ==============================================================================================
# Main Test Runner
# ==============================================================================================

def run_all_tests():
    """Run all tests and generate report"""
    if HAS_COLOR:
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🧪 Testing main.py - Complete System Validation{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    else:
        print(f"\n{'='*80}")
        print(f"🧪 Testing main.py - Complete System Validation")
        print(f"{'='*80}\n")
    
    total_tests = 7
    passed_tests = 0
    all_errors = []
    all_warnings = []
    
    # Test 1: Environment Variables
    success, errors, warnings = test_environment_variables()
    if success:
        passed_tests += 1
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 2: Imports
    success, errors = test_imports()
    if success:
        passed_tests += 1
    all_errors.extend(errors)
    
    # Test 3: CodeMultiAgentSystem
    success, errors = test_code_agent_system()
    if success:
        passed_tests += 1
    all_errors.extend(errors)
    
    # Test 4: Data Files
    success, errors, warnings = test_data_files()
    if success:
        passed_tests += 1
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    
    # Test 5: Output Directory
    success, errors = test_output_directory()
    if success:
        passed_tests += 1
    all_errors.extend(errors)
    
    # Test 6: MongoDB (optional)
    success, errors = test_mongodb_connection()
    if success:
        passed_tests += 1
    all_errors.extend(errors)
    
    # Test 7: Simple Query
    success, errors = test_simple_query()
    if success:
        passed_tests += 1
    all_errors.extend(errors)
    
    # Generate final report
    print_header("Test Summary")
    
    if HAS_COLOR:
        print(f"{Fore.CYAN}Tests Passed: {passed_tests}/{total_tests}{Style.RESET_ALL}\n")
    else:
        print(f"Tests Passed: {passed_tests}/{total_tests}\n")
    
    if all_errors:
        if HAS_COLOR:
            print(f"{Fore.RED}Errors Found: {len(all_errors)}{Style.RESET_ALL}")
        else:
            print(f"Errors Found: {len(all_errors)}")
        for error in all_errors:
            if HAS_COLOR:
                print(f"{Fore.RED}  ❌ {error}{Style.RESET_ALL}")
            else:
                print(f"  ❌ {error}")
        print()
    
    if all_warnings:
        if HAS_COLOR:
            print(f"{Fore.YELLOW}Warnings: {len(all_warnings)}{Style.RESET_ALL}")
        else:
            print(f"Warnings: {len(all_warnings)}")
        for warning in all_warnings:
            if HAS_COLOR:
                print(f"{Fore.YELLOW}  ⚠️  {warning}{Style.RESET_ALL}")
            else:
                print(f"  ⚠️  {warning}")
        print()
    
    # Final verdict
    if passed_tests == total_tests and len(all_errors) == 0:
        if HAS_COLOR:
            print(f"{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}✅ ALL TESTS PASSED! main.py is ready for deployment.{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'='*80}{Style.RESET_ALL}\n")
            print(f"{Fore.CYAN}You can now run:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}  python main.py{Style.RESET_ALL}\n")
        else:
            print(f"{'='*80}")
            print(f"✅ ALL TESTS PASSED! main.py is ready for deployment.")
            print(f"{'='*80}\n")
            print(f"You can now run:")
            print(f"  python main.py\n")
        return True
    elif len(all_errors) == 0:
        if HAS_COLOR:
            print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}⚠️  TESTS PASSED WITH WARNINGS{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}\n")
            print(f"{Fore.YELLOW}main.py will work but some features may be limited.{Style.RESET_ALL}\n")
        else:
            print(f"{'='*80}")
            print(f"⚠️  TESTS PASSED WITH WARNINGS")
            print(f"{'='*80}\n")
            print(f"main.py will work but some features may be limited.\n")
        return True
    else:
        if HAS_COLOR:
            print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}")
            print(f"{Fore.RED}❌ TESTS FAILED! Please fix errors before running main.py{Style.RESET_ALL}")
            print(f"{Fore.RED}{'='*80}{Style.RESET_ALL}\n")
        else:
            print(f"{'='*80}")
            print(f"❌ TESTS FAILED! Please fix errors before running main.py")
            print(f"{'='*80}\n")
        return False


# ==============================================================================================
# Entry Point
# ==============================================================================================

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

