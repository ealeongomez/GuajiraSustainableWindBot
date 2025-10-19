#!/bin/bash
#
# Fix Dependencies Script
# =======================
# 
# Automatically fixes dependency issues detected by test_main.py
# 
# Author: Eder Arley León Gómez
# Date: 2025-10-19
#

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}🔧 Fixing Dependencies${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Navigate to project root
cd "$(dirname "$0")/../.."
PROJECT_ROOT=$(pwd)

echo -e "${YELLOW}Project root: ${PROJECT_ROOT}${NC}"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found${NC}"
    echo -e "${YELLOW}Creating new virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Virtual environment created${NC}"
    else
        echo -e "${RED}❌ Failed to create virtual environment${NC}"
        exit 1
    fi
fi

# Activate venv
echo -e "${CYAN}Activating virtual environment...${NC}"
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Virtual environment activated${NC}"
echo ""

# Upgrade pip
echo -e "${CYAN}Upgrading pip...${NC}"
pip install --upgrade pip -q

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${YELLOW}⚠️  requirements.txt not found${NC}"
    echo -e "${YELLOW}Installing core packages manually...${NC}"
    
    # Install core packages
    pip install python-telegram-bot -q
    pip install langchain langchain-openai langchain-experimental langsmith -q
    pip install pandas numpy matplotlib -q
    pip install python-dotenv pymongo colorama -q
    
    echo -e "${GREEN}✅ Core packages installed${NC}"
else
    echo -e "${CYAN}Installing packages from requirements.txt...${NC}"
    pip install -r requirements.txt -q
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ All packages installed from requirements.txt${NC}"
    else
        echo -e "${RED}❌ Error installing from requirements.txt${NC}"
        echo -e "${YELLOW}Trying manual installation...${NC}"
        
        pip install python-telegram-bot -q
        pip install langchain langchain-openai langchain-experimental langsmith -q
        pip install pandas numpy matplotlib -q
        pip install python-dotenv pymongo colorama -q
    fi
fi

echo ""

# Verify critical packages
echo -e "${CYAN}Verifying installation...${NC}"

check_package() {
    python -c "import $1" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}  ✅ $1${NC}"
        return 0
    else
        echo -e "${RED}  ❌ $1${NC}"
        return 1
    fi
}

ERRORS=0

check_package "telegram" || ERRORS=$((ERRORS+1))
check_package "langchain" || ERRORS=$((ERRORS+1))
check_package "langchain_openai" || ERRORS=$((ERRORS+1))
check_package "pandas" || ERRORS=$((ERRORS+1))
check_package "numpy" || ERRORS=$((ERRORS+1))
check_package "dotenv" || ERRORS=$((ERRORS+1))

echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✅ All dependencies installed!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${CYAN}Next steps:${NC}"
    echo -e "${CYAN}1. Run tests: cd test/chatbot && python test_main.py${NC}"
    echo -e "${CYAN}2. Launch bot: python main.py${NC}"
    echo ""
else
    echo -e "${YELLOW}========================================${NC}"
    echo -e "${YELLOW}⚠️  Some packages failed to install${NC}"
    echo -e "${YELLOW}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Try:${NC}"
    echo -e "${YELLOW}  pip install --upgrade pip${NC}"
    echo -e "${YELLOW}  pip install -r requirements.txt${NC}"
    echo ""
fi

# Show current environment
echo -e "${CYAN}Current environment:${NC}"
echo -e "  Python: $(which python)"
echo -e "  Pip: $(which pip)"
echo ""

