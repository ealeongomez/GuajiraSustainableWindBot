# Code Agent Module - Text-to-Python Multi-Agent System

## 📋 Descripción

Módulo modular y reutilizable para el sistema multi-agente con capacidad text-to-python.

## 🏗️ Estructura del Módulo

```
src/code_agent/
├── __init__.py              # Package initialization and exports
├── config.py                # Configuration and LLM initialization
├── data_manager.py          # Data loading and caching
├── safe_repl.py             # Safe Python code execution
├── supervisor.py            # Query routing agent
├── municipality_agent.py    # Municipality-specific analysis agent
├── general_agent.py         # General knowledge agent
├── system.py                # System orchestrator
└── README.md                # This file
```

## 🚀 Uso Básico

### Importación Simple

```python
from src.code_agent import CodeMultiAgentSystem

# Inicializar sistema
system = CodeMultiAgentSystem(verbose=True)

# Procesar consulta
response = system.process_query("¿Cuál es el promedio de viento en Riohacha?")
print(response)
```

### Uso Avanzado

```python
from src.code_agent import (
    DataManager,
    SafePythonREPL,
    SupervisorAgent,
    CodeMunicipalityAgent,
    GeneralAgent
)
from src.code_agent.config import get_supervisor_llm, get_agent_llm

# Inicializar componentes individuales
data_manager = DataManager(verbose=True)
supervisor = SupervisorAgent(get_supervisor_llm())

# Enrutar consulta manualmente
routing = supervisor.route_query("¿Cuál es el viento en Maicao?")
print(routing)  # {'type': 'data_query', 'municipalities': ['maicao'], 'needs_code': True}
```

## 📦 Componentes

### 1. DataManager (`data_manager.py`)

Gestiona la carga y caché de datos de municipios.

**Características:**
- Carga todos los municipios al inicializar
- Cache en memoria para acceso rápido
- Conversión automática de fechas a datetime
- Estadísticas por municipio

**Ejemplo:**
```python
from src.code_agent import DataManager

dm = DataManager()
df = dm.get_data('riohacha')
stats = dm.get_statistics('riohacha')
```

### 2. SafePythonREPL (`safe_repl.py`)

Entorno seguro de ejecución de código Python.

**Características:**
- Builtins limitados (seguridad)
- DataFrames pre-cargados
- Acceso a pandas y matplotlib
- Captura de stdout

**Ejemplo:**
```python
from src.code_agent import SafePythonREPL, DataManager

dm = DataManager()
repl = SafePythonREPL(dm)

code = "print(df_riohacha['wind_speed_10m'].mean())"
result = repl.run(code)
print(result)  # "15.39"
```

### 3. SupervisorAgent (`supervisor.py`)

Analiza consultas y decide el enrutamiento.

**Características:**
- Clasificación de tipo de consulta
- Detección de municipios mencionados
- Determina si necesita código

**Ejemplo:**
```python
from src.code_agent import SupervisorAgent
from src.code_agent.config import get_supervisor_llm

supervisor = SupervisorAgent(get_supervisor_llm())
routing = supervisor.route_query("Compara Riohacha y Maicao")
# {'type': 'comparison', 'municipalities': ['riohacha', 'maicao'], 'needs_code': True}
```

### 4. CodeMunicipalityAgent (`municipality_agent.py`)

Agente especializado para análisis de datos de un municipio.

**Características:**
- Generación de código Python
- Ejecución en Safe REPL
- Formateo conversacional de respuestas
- Soporte para gráficas

**Ejemplo:**
```python
from src.code_agent import CodeMunicipalityAgent, DataManager
from src.code_agent.config import get_agent_llm

dm = DataManager()
agent = CodeMunicipalityAgent('riohacha', get_agent_llm(), dm)
response = agent.answer("¿Cuál es el promedio de viento?")
```

### 5. GeneralAgent (`general_agent.py`)

Agente para preguntas conceptuales sin código.

**Características:**
- Respuestas sobre energía eólica
- Explicación de conceptos LSTM
- Información de La Guajira

**Ejemplo:**
```python
from src.code_agent import GeneralAgent
from src.code_agent.config import get_agent_llm

agent = GeneralAgent(get_agent_llm())
response = agent.answer("¿Qué es un modelo LSTM?")
```

### 6. CodeMultiAgentSystem (`system.py`)

Orquestador principal del sistema multi-agente.

**Características:**
- Inicialización automática de todos los componentes
- Routing inteligente de consultas
- Manejo de consultas multi-municipio
- Modo verbose configurable

**Ejemplo:**
```python
from src.code_agent import CodeMultiAgentSystem

# Con verbose
system = CodeMultiAgentSystem(verbose=True)
response = system.process_query("Promedio de viento en Albania")

# Sin verbose (silencioso)
system = CodeMultiAgentSystem(verbose=False)
response = system.process_query("Promedio de viento en Albania", verbose=False)
```

## ⚙️ Configuración

El archivo `config.py` contiene:

```python
# Paths
PROJECT_ROOT    # Raíz del proyecto
DATA_DIR        # data/raw/
MODELS_DIR      # models/LSTM/
OUTPUT_DIR      # test/chatbot/output/

# Municipalities
MUNICIPALITIES  # Lista de 13 municipios

# LLM Functions
get_supervisor_llm()  # GPT-4 para supervisor
get_agent_llm()       # GPT-4 para agentes
```

## 🔒 Seguridad

El `SafePythonREPL` implementa:

- ✅ Builtins limitados (sin eval, exec, import, etc.)
- ✅ Solo módulos permitidos (pandas, matplotlib)
- ✅ DataFrames pre-cargados (sin I/O de archivos)
- ✅ No acceso a red
- ✅ Ejecución en scope controlado

## 📊 Flujo de Datos

```
Usuario
   ↓
CodeMultiAgentSystem.process_query()
   ↓
SupervisorAgent.route_query()
   ↓
   ├─→ GeneralAgent.answer()           (preguntas conceptuales)
   │
   └─→ CodeMunicipalityAgent.answer()  (análisis de datos)
        ↓
        1. Genera código Python
        2. Ejecuta en SafePythonREPL
        3. Formatea respuesta
        ↓
   Respuesta al usuario
```

## 🧪 Testing

```bash
# Test completo del sistema
python test/chatbot/test_single_query.py

# Test interactivo
python test/chatbot/supervisor_code_agent_test.py
```

## 📝 Ejemplos Completos

### Ejemplo 1: Análisis Simple

```python
from src.code_agent import CodeMultiAgentSystem

system = CodeMultiAgentSystem()
queries = [
    "¿Cuál es el promedio de viento en Riohacha?",
    "¿Cuál es la temperatura máxima en Maicao?",
    "¿Cuántos registros hay de Albania?"
]

for query in queries:
    response = system.process_query(query, verbose=False)
    print(f"Q: {query}")
    print(f"A: {response}\n")
```

### Ejemplo 2: Comparación Multi-Municipio

```python
from src.code_agent import CodeMultiAgentSystem

system = CodeMultiAgentSystem(verbose=True)
response = system.process_query(
    "Compara el viento promedio entre Riohacha y Maicao"
)
print(response)
```

### Ejemplo 3: Generación de Gráfica

```python
from src.code_agent import CodeMultiAgentSystem

system = CodeMultiAgentSystem()
response = system.process_query(
    "Quiero una gráfica de la velocidad del viento de Uribia"
)
print(response)
# La gráfica se guarda en OUTPUT_DIR
```

## 🔧 Extensión del Módulo

### Agregar Nuevo Agente

1. Crear archivo en `src/code_agent/my_agent.py`
2. Implementar clase con método `answer(query: str) -> str`
3. Agregar a `__init__.py`
4. Actualizar `system.py` para enrutamiento

### Modificar Prompt del Supervisor

Editar `supervisor.py`, método `__init__`:

```python
self.prompt = ChatPromptTemplate.from_template(
    """Tu nuevo prompt aquí..."""
)
```

### Cambiar Modelo LLM

Editar `config.py`:

```python
def get_agent_llm():
    return ChatOpenAI(
        model="gpt-3.5-turbo",  # Cambiar modelo
        temperature=0.2,         # Ajustar temperatura
        ...
    )
```

## 📈 Performance

- **Carga inicial:** ~3 segundos (13 municipios)
- **Consulta simple:** ~5-8 segundos (con GPT-4)
- **Consulta con gráfica:** ~8-12 segundos
- **Memoria:** ~50MB (DataFrames en cache)

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY not found"
```bash
# Verificar .env
cat .env | grep OPENAI_API_KEY
```

### Error: "Module 'code_agent' not found"
```python
# Asegurarse de estar en project root
import sys
sys.path.insert(0, '/path/to/project')
```

### Error: "Data not found"
```bash
# Verificar archivos CSV
ls -la data/raw/open_meteo_*.csv
```

## 👨‍💻 Autor

Eder Arley León Gómez  
Fecha: 2025-10-19

## 📝 Changelog

### v1.0.0 (2025-10-19)
- Módulo inicial
- 6 componentes principales
- Soporte para text-to-python
- Generación de gráficas
- Safe Python REPL

