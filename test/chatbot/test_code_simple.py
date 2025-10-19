"""
==============================================================================
Simple test for text-to-python system - Step by step validation
==============================================================================
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style, init
import pandas as pd

# Initialize colorama
init(autoreset=True)

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
print(f"{Fore.CYAN}🧪 Simple Test Suite - Text-to-Python System{Style.RESET_ALL}")
print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

# ============================================================================
# Test 1: Check Environment
# ============================================================================
print(f"{Fore.YELLOW}Test 1: Verificando entorno...{Style.RESET_ALL}")

if os.getenv("OPENAI_API_KEY"):
    print(f"{Fore.GREEN}✅ OPENAI_API_KEY encontrada{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}❌ OPENAI_API_KEY no encontrada{Style.RESET_ALL}")
    sys.exit(1)

print(f"{Fore.GREEN}✅ Python version: {sys.version.split()[0]}{Style.RESET_ALL}")
print()

# ============================================================================
# Test 2: Check Data Files
# ============================================================================
print(f"{Fore.YELLOW}Test 2: Verificando archivos de datos...{Style.RESET_ALL}")

DATA_DIR = project_root / "data" / "raw"
MUNICIPALITIES = ["riohacha", "maicao", "albania"]

data_found = 0
for municipality in MUNICIPALITIES:
    csv_file = DATA_DIR / f"open_meteo_{municipality}.csv"
    if csv_file.exists():
        try:
            df = pd.read_csv(csv_file, nrows=5)  # Just read 5 rows for testing
            print(f"{Fore.GREEN}✅ {municipality}: {csv_file.name} ({len(df.columns)} columnas){Style.RESET_ALL}")
            data_found += 1
        except Exception as e:
            print(f"{Fore.RED}❌ {municipality}: Error leyendo CSV - {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ {municipality}: Archivo no encontrado{Style.RESET_ALL}")

print(f"\n{Fore.CYAN}Archivos encontrados: {data_found}/{len(MUNICIPALITIES)}{Style.RESET_ALL}\n")

if data_found == 0:
    print(f"{Fore.RED}❌ No se encontraron datos. Verifica que los archivos CSV estén en {DATA_DIR}{Style.RESET_ALL}")
    sys.exit(1)

# ============================================================================
# Test 3: Import Main Components
# ============================================================================
print(f"{Fore.YELLOW}Test 3: Importando componentes del sistema...{Style.RESET_ALL}")

try:
    from langchain_openai import ChatOpenAI
    print(f"{Fore.GREEN}✅ ChatOpenAI importado{Style.RESET_ALL}")
except ImportError as e:
    print(f"{Fore.RED}❌ Error importando ChatOpenAI: {e}{Style.RESET_ALL}")
    sys.exit(1)

try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    print(f"{Fore.GREEN}✅ LangChain core components importados{Style.RESET_ALL}")
except ImportError as e:
    print(f"{Fore.RED}❌ Error importando LangChain core: {e}{Style.RESET_ALL}")
    sys.exit(1)

print()

# ============================================================================
# Test 4: Initialize LLM
# ============================================================================
print(f"{Fore.YELLOW}Test 4: Inicializando LLM...{Style.RESET_ALL}")

try:
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        max_retries=2,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    print(f"{Fore.GREEN}✅ LLM GPT-4 inicializado correctamente{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}❌ Error inicializando LLM: {e}{Style.RESET_ALL}")
    sys.exit(1)

print()

# ============================================================================
# Test 5: Test Safe Python REPL
# ============================================================================
print(f"{Fore.YELLOW}Test 5: Probando Safe Python REPL...{Style.RESET_ALL}")

try:
    # Load one dataframe
    csv_file = DATA_DIR / "open_meteo_riohacha.csv"
    df_riohacha = pd.read_csv(csv_file)
    print(f"{Fore.GREEN}✅ DataFrame cargado: {len(df_riohacha)} registros{Style.RESET_ALL}")
    
    # Test simple calculation
    mean_wind = df_riohacha['wind_speed_10m'].mean()
    print(f"{Fore.GREEN}✅ Cálculo de prueba: Viento promedio = {mean_wind:.2f} m/s{Style.RESET_ALL}")
    
    # Test code execution via exec
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    exec("print(f'Test: {df_riohacha[\"wind_speed_10m\"].mean():.2f}')", {'df_riohacha': df_riohacha})
    
    sys.stdout = old_stdout
    result = captured_output.getvalue().strip()
    print(f"{Fore.GREEN}✅ Ejecución de código: {result}{Style.RESET_ALL}")
    
except Exception as e:
    sys.stdout = old_stdout
    print(f"{Fore.RED}❌ Error en Safe REPL: {e}{Style.RESET_ALL}")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)

print()

# ============================================================================
# Test 6: Test Simple LLM Call (Optional)
# ============================================================================
print(f"{Fore.YELLOW}Test 6: Prueba de llamada LLM (opcional)...{Style.RESET_ALL}")

test_llm = input(f"{Fore.CYAN}¿Ejecutar prueba de LLM? (consume tokens) [y/N]: {Style.RESET_ALL}").strip().lower()

if test_llm == 'y':
    try:
        prompt = ChatPromptTemplate.from_template("Responde en UNA palabra: ¿Cuál es la capital de Colombia?")
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({})
        print(f"{Fore.GREEN}✅ LLM respuesta: {response}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error en llamada LLM: {e}{Style.RESET_ALL}")
        import traceback
        print(traceback.format_exc())
else:
    print(f"{Fore.YELLOW}⏭️  Prueba de LLM omitida{Style.RESET_ALL}")

print()

# ============================================================================
# Summary
# ============================================================================
print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
print(f"{Fore.CYAN}📊 Resumen de Tests{Style.RESET_ALL}")
print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
print(f"{Fore.GREEN}✅ Todos los tests básicos pasaron correctamente{Style.RESET_ALL}")
print(f"{Fore.GREEN}✅ El sistema está listo para usar{Style.RESET_ALL}")
print()
print(f"{Fore.YELLOW}Para probar el sistema completo:{Style.RESET_ALL}")
print(f"  python test/chatbot/supervisor_code_agent_test.py")
print()

