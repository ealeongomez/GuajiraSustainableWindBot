"""
Quick test: Single query validation
Updated to use src/code_agent module
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style, init
import pandas as pd

init(autoreset=True)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
print(f"{Fore.CYAN}🧪 Single Query Test - Velocidad Promedio de Riohacha{Style.RESET_ALL}")
print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

# Calculate expected value
print(f"{Fore.YELLOW}📊 Calculando valor esperado...{Style.RESET_ALL}")
DATA_DIR = project_root / "data" / "raw"
df = pd.read_csv(DATA_DIR / "open_meteo_riohacha.csv")
expected_value = df['wind_speed_10m'].mean()
print(f"{Fore.CYAN}Valor esperado: {expected_value:.2f} m/s{Style.RESET_ALL}")
print(f"{Fore.CYAN}Total registros: {len(df):,}{Style.RESET_ALL}\n")

# Load system
print(f"{Fore.YELLOW}🤖 Cargando sistema multi-agente...{Style.RESET_ALL}")
try:
    from src.code_agent import CodeMultiAgentSystem
    system = CodeMultiAgentSystem(verbose=True)
    print(f"{Fore.GREEN}✅ Sistema cargado{Style.RESET_ALL}\n")
except Exception as e:
    print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
    sys.exit(1)

# Execute query
query = "¿Cuál es la velocidad promedio del viento en Riohacha?"
print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
print(f"{Fore.CYAN}Query: {query}{Style.RESET_ALL}")
print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

print(f"{Fore.YELLOW}💭 Ejecutando consulta con GPT-4...{Style.RESET_ALL}")
print(f"{Fore.YELLOW}(Esto tomará 5-10 segundos y costará ~$0.035){Style.RESET_ALL}\n")

try:
    response = system.process_query(query, verbose=True)
    
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🤖 Respuesta del Sistema:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    print(response)
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    # Validate
    print(f"\n{Fore.YELLOW}📊 Validación:{Style.RESET_ALL}\n")
    print(f"Valor esperado: {Fore.CYAN}{expected_value:.2f} m/s{Style.RESET_ALL}")
    
    # Try to extract number from response
    import re
    numbers = re.findall(r'\d+\.?\d*', response)
    
    if numbers:
        extracted = float(numbers[0])
        print(f"Valor en respuesta: {Fore.CYAN}{extracted:.2f} m/s{Style.RESET_ALL}")
        diff = abs(extracted - expected_value)
        print(f"Diferencia: {Fore.CYAN}{diff:.2f} m/s{Style.RESET_ALL}")
        
        # Check tolerance (5%)
        tolerance = 0.05 * expected_value
        if diff <= tolerance:
            print(f"\n{Fore.GREEN}✅ VALIDACIÓN EXITOSA - El sistema respondió correctamente!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}   La respuesta está dentro del margen de tolerancia (5%){Style.RESET_ALL}\n")
        else:
            print(f"\n{Fore.YELLOW}⚠️  Diferencia mayor al 5% esperado{Style.RESET_ALL}\n")
    else:
        print(f"\n{Fore.YELLOW}⚠️  No se pudo extraer un valor numérico de la respuesta{Style.RESET_ALL}\n")
        
except Exception as e:
    print(f"\n{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
    import traceback
    print(traceback.format_exc())
