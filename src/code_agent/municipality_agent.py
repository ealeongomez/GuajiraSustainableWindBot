"""
Municipality Agent - Code-enabled agent for municipality-specific queries
"""

import traceback
from colorama import Fore, Style

from .safe_repl import SafePythonREPL
from .security import SecurityValidator


class CodeMunicipalityAgent:
    """Municipality agent with Python code execution capability."""
    
    def __init__(self, municipality: str, llm, data_manager):
        """
        Initialize Municipality Agent.
        
        Args:
            municipality: Name of the municipality
            llm: Language model instance
            data_manager: DataManager instance
        """
        self.municipality = municipality
        self.llm = llm
        self.data_manager = data_manager
        self.python_repl = SafePythonREPL(data_manager)
        self.security_validator = SecurityValidator(verbose=False)
        
    def answer(self, query: str) -> str:
        """
        Answer query using Python code generation and execution.
        
        Args:
            query: User's question
            
        Returns:
            Formatted response string
        """
        municipality_display = self.municipality.replace("_", " ").title()
        df = self.data_manager.get_data(self.municipality)
        
        if df is None:
            return f"No hay datos disponibles para {municipality_display}."
        
        # Create prompt for code generation
        prompt = f"""Eres un experto analista de datos para {municipality_display}, La Guajira.

IMPORTANTE: Tienes un DataFrame PRE-CARGADO llamado 'df_{self.municipality}' que contiene ÚNICAMENTE datos de {municipality_display}.
NO necesitas importar pandas, NO necesitas filtrar por municipio - el DataFrame ya contiene solo datos de {municipality_display}.

El DataFrame 'df_{self.municipality}' tiene las siguientes columnas:
- datetime: fecha y hora (pandas datetime)
- wind_speed_10m: velocidad del viento a 10m (m/s) - float
- wind_direction_10m: dirección del viento (grados) - float
- temperature_2m: temperatura a 2m (°C) - float
- relative_humidity_2m: humedad relativa (%) - float
- precipitation: precipitación (mm) - float
- hour: hora del día (0-23) - int
- date: fecha - string
- municipio: siempre "{self.municipality}" - string

Datos disponibles:
- Total de registros: {len(df):,}
- Rango de fechas: {df['datetime'].min()} a {df['datetime'].max()}
- Todos los registros son de {municipality_display}

Tu tarea:
1. Genera código Python SIMPLE para responder la consulta
2. USA DIRECTAMENTE df_{self.municipality} - NO filtres por municipio
3. El código DEBE usar print() para mostrar los resultados
4. NO uses imports (pandas ya está disponible como 'pd', matplotlib.pyplot como 'plt')
5. Sé preciso con los cálculos

Para GRÁFICAS:
- Usa plt.figure() para crear la figura
- Crea la gráfica con plt.plot() o similar
- SIEMPRE guarda con: plt.savefig(OUTPUT_DIR / 'nombre_archivo.png')
- Usa plt.close() al final
- Imprime la ruta donde se guardó

Ejemplos de código correcto:

# Para estadísticas simples:
promedio = df_{self.municipality}['wind_speed_10m'].mean()
print(f"Velocidad promedio: {{promedio:.2f}} m/s")

# Para gráficas:
plt.figure(figsize=(12, 6))
plt.plot(df_{self.municipality}['datetime'], df_{self.municipality}['wind_speed_10m'])
plt.title('Velocidad del Viento en {municipality_display}')
plt.xlabel('Fecha')
plt.ylabel('Velocidad (m/s)')
plt.grid(True)
output_file = OUTPUT_DIR / '{self.municipality}_wind_speed.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.close()
print(f"Gráfica guardada en: {{output_file}}")

Consulta del usuario: {query}

Genera SOLO el código Python (sin imports, sin explicaciones, solo el código ejecutable):"""

        try:
            # Generate code
            code = self.llm.invoke(prompt).content.strip()
            
            # Remove markdown code blocks if present
            if code.startswith("```python"):
                code = code.split("```python", 1)[1]
            if code.startswith("```"):
                code = code.split("```", 1)[1]
            if "```" in code:
                code = code.split("```")[0]
            code = code.strip()
            
            # Sanitize code for security
            sanitized_code = self.security_validator.sanitize_code(code)
            
            if not sanitized_code:
                return f"⚠️ El código generado contiene operaciones no permitidas por seguridad. Por favor, reformula tu pregunta de manera más específica sobre {municipality_display}."
            
            # Execute code
            print(f"{Fore.CYAN}🐍 Ejecutando código:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{sanitized_code}{Style.RESET_ALL}\n")
            
            result = self.python_repl.run(sanitized_code)
            
            # Format result conversationally
            format_prompt = f"""Basado en estos resultados de análisis de datos para {municipality_display}:

{result}

Genera una respuesta conversacional en español que:
1. Responda directamente la pregunta del usuario
2. Incluya los números y estadísticas del resultado
3. Sea clara y concisa
4. Use lenguaje natural

Pregunta original: {query}

Respuesta conversacional:"""
            
            formatted_response = self.llm.invoke(format_prompt).content.strip()
            
            return formatted_response
            
        except Exception as e:
            error_trace = traceback.format_exc()
            return f"Error al analizar datos de {municipality_display}: {str(e)}\n\nDetalles técnicos:\n{error_trace}"

