#!/bin/bash
#
# Test Runner Script for WindBot ChatBot
# ========================================
# 
# Quick launcher for different test scenarios
# 
# Author: Eder Arley León Gómez
# Created: 2025-10-19
#

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Banner
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}🌬️  WindBot Test Runner${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Menu
show_menu() {
    echo -e "${YELLOW}Select a test to run:${NC}"
    echo ""
    echo "  ${GREEN}🧪 Pre-Deployment:${NC}"
    echo "    1) Test main.py (Complete Validation) ⭐ RUN FIRST"
    echo ""
    echo "  ${GREEN}🚀 Production Bot:${NC}"
    echo "    2) Main Production Bot (main.py)"
    echo ""
    echo "  ${GREEN}Basic Chatbots:${NC}"
    echo "    3) Console Basic Chatbot"
    echo "    4) Telegram Basic Chatbot"
    echo ""
    echo "  ${GREEN}Code Agent Systems (Text-to-Python):${NC}"
    echo "    5) Console Code Agent System"
    echo "    6) Telegram Code Agent System (Test Version)"
    echo ""
    echo "  ${GREEN}Unit Tests:${NC}"
    echo "    7) Code Agent Tests"
    echo "    8) Security Tests"
    echo "    9) Multi-Agent Routing Tests"
    echo "   10) History Loading Tests"
    echo ""
    echo "  ${GREEN}Utilities:${NC}"
    echo "   11) Query MongoDB Conversations"
    echo "   12) Verify History in Context"
    echo ""
    echo "    0) Exit"
    echo ""
}

# Check environment
check_env() {
    if [ ! -f "../../.env" ]; then
        echo -e "${RED}❌ Error: .env file not found${NC}"
        echo -e "${YELLOW}Please create .env in project root${NC}"
        exit 1
    fi
    
    if ! grep -q "OPENAI_API_KEY" "../../.env"; then
        echo -e "${RED}❌ Error: OPENAI_API_KEY not found in .env${NC}"
        exit 1
    fi
}

# Run test
run_test() {
    local test_file=$1
    local test_name=$2
    
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}Running: ${test_name}${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
    
    if [ -f "$test_file" ]; then
        python "$test_file"
    else
        echo -e "${RED}❌ Error: $test_file not found${NC}"
    fi
}

# Main loop
main() {
    check_env
    
    while true; do
        show_menu
        read -p "Enter your choice [0-12]: " choice
        
        case $choice in
            1)
                echo ""
                echo -e "${CYAN}========================================${NC}"
                echo -e "${CYAN}Running: test_main.py (Complete Validation)${NC}"
                echo -e "${CYAN}========================================${NC}"
                echo ""
                cd ../.. && python test_main.py
                cd "$SCRIPT_DIR"
                ;;
            2)
                echo ""
                echo -e "${CYAN}========================================${NC}"
                echo -e "${CYAN}Running: Main Production Bot${NC}"
                echo -e "${CYAN}========================================${NC}"
                echo ""
                cd ../.. && python main.py
                cd "$SCRIPT_DIR"
                ;;
            3)
                run_test "console_chatbot_test.py" "Console Basic Chatbot"
                ;;
            4)
                run_test "telegram_chatbot.py" "Telegram Basic Chatbot"
                ;;
            5)
                run_test "supervisor_code_agent_test.py" "Console Code Agent System"
                ;;
            6)
                run_test "telegram_code_agent_test.py" "Telegram Code Agent System (Test)"
                ;;
            7)
                run_test "test_code_agent.py" "Code Agent Tests"
                ;;
            8)
                echo ""
                echo -e "${CYAN}Running Security Tests...${NC}"
                echo ""
                python test_security.py
                echo ""
                python test_security_integration.py
                ;;
            9)
                run_test "test_multiagent_routing.py" "Multi-Agent Routing Tests"
                ;;
            10)
                run_test "test_history_loading.py" "History Loading Tests"
                ;;
            11)
                run_test "query_conversations.py" "Query MongoDB Conversations"
                ;;
            12)
                run_test "verify_history_in_context.py" "Verify History in Context"
                ;;
            0)
                echo ""
                echo -e "${GREEN}👋 Goodbye!${NC}"
                echo ""
                exit 0
                ;;
            *)
                echo ""
                echo -e "${RED}❌ Invalid option. Please try again.${NC}"
                echo ""
                ;;
        esac
        
        echo ""
        echo -e "${YELLOW}Press Enter to continue...${NC}"
        read
        clear
    done
}

# Run main
main

