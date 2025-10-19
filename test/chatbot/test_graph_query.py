"""
Test for graph generation capability
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style, init

init(autoreset=True)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
print(f"{Fore.CYAN}🧪 Graph Generation Test - Gráfica de Viento en Uribia{Style.RESET_ALL}")
print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

# Load system
print(f"{Fore.YELLOW}🤖 Cargando sistema multi-agente...{Style.RESET_ALL}")
try:
    from supervisor_code_agent_test import CodeMultiAgentSystem, OUTPUT_DIR
    system = CodeMultiAgentSystem()
    print(f"{Fore.GREEN}✅ Sistema cargado{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📁 Gráficas se guardarán en: {OUTPUT_DIR}{Style.RESET_ALL}\n")
except Exception as e:
    print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
    sys.exit(1)

# Execute query
query = "Quiero una gráfica de la velocidad del viento de Uribia"
print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
print(f"{Fore.CYAN}Query: {query}{Style.RESET_ALL}")
print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")

print(f"{Fore.YELLOW}💭 Ejecutando consulta con GPT-4...{Style.RESET_ALL}")
print(f"{Fore.YELLOW}(Esto generará código para crear una gráfica){Style.RESET_ALL}\n")

try:
    response = system.process_query(query)
    
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🤖 Respuesta del Sistema:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    print(response)
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    # Check if graph was created
    print(f"\n{Fore.YELLOW}🔍 Verificando archivos generados...{Style.RESET_ALL}\n")
    
    output_files = list(OUTPUT_DIR.glob("*.png"))
    if output_files:
        print(f"{Fore.GREEN}✅ Gráficas encontradas:{Style.RESET_ALL}")
        for f in output_files:
            file_size = f.stat().st_size / 1024  # KB
            print(f"   📊 {f.name} ({file_size:.1f} KB)")
        print(f"\n{Fore.GREEN}✅ ÉXITO - Sistema generó gráfica correctamente!{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.YELLOW}⚠️  No se encontraron archivos PNG en {OUTPUT_DIR}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   El código pudo ejecutarse pero no guardar archivo{Style.RESET_ALL}\n")
        
except Exception as e:
    print(f"\n{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
    import traceback
    print(traceback.format_exc())

