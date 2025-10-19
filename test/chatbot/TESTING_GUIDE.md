# Guía de Testing - Sistema Text-to-Python

## 📋 Resumen de Tests Disponibles

Este directorio contiene múltiples niveles de tests para validar el sistema text-to-python multi-agente.

## 🧪 Tests Disponibles

### 1. **test_minimal.py** - Test Básico de Componentes

**Propósito:** Verifica que todas las dependencias y componentes básicos estén instalados y funcionando.

**Qué verifica:**
- ✅ Versión de Python
- ✅ Estructura del proyecto
- ✅ Archivos CSV de datos
- ✅ Archivo .env y API key
- ✅ Importación de librerías (pandas, langchain, colorama)
- ✅ Funcionamiento de colorama

**Ejecutar:**
```bash
cd /Users/guane/Documentos/Doctorate/GuajiraSustainableWindBot
./venv/bin/python test/chatbot/test_minimal.py
```

**Tiempo:** < 5 segundos  
**Costo:** $0  
**Prerequisitos:** Ninguno

---

### 2. **test_code_simple.py** - Test de Sistema sin API calls

**Propósito:** Valida el sistema completo sin hacer llamadas a la API de OpenAI.

**Qué verifica:**
- ✅ Carga de archivos CSV (3 municipios de prueba)
- ✅ Inicialización del LLM (sin ejecutar)
- ✅ Safe Python REPL (ejecución local de código)
- ✅ Cálculos estadísticos básicos
- ✅ Opcionalmente: 1 llamada simple a LLM

**Ejecutar:**
```bash
./venv/bin/python test/chatbot/test_code_simple.py
# Responde 'n' cuando pregunte sobre test LLM para evitar costo
```

**Tiempo:** < 10 segundos  
**Costo:** $0 (sin test LLM opcional)  
**Prerequisitos:** OPENAI_API_KEY en .env

---

### 3. **test_analysis_validation.py** - Validación de Análisis Real ⭐

**Propósito:** Ejecuta consultas reales con el sistema y valida que los resultados sean precisos.

**Qué hace:**
1. Carga el sistema multi-agente completo
2. Pre-calcula valores esperados de los datos
3. Ejecuta 3 consultas de ejemplo:
   - Promedio de viento en Riohacha
   - Temperatura máxima en Maicao
   - Número de registros en Albania
4. Compara las respuestas del LLM con los valores reales
5. Genera reporte de precisión

**Ejecutar:**
```bash
./venv/bin/python test/chatbot/test_analysis_validation.py
# Responde 'y' cuando pregunte si ejecutar las consultas
```

**Tiempo:** 30-60 segundos  
**Costo:** ~$0.10 (3 consultas × $0.035)  
**Prerequisitos:** OPENAI_API_KEY en .env

**Output esperado:**
```
✅ PASS: Average wind speed in Riohacha
✅ PASS: Maximum temperature in Maicao
✅ PASS: Number of records for Albania

Total: 3
Passed: 3
Warnings: 0
Failed: 0

✨ All tests passed! The system produces accurate results.
```

---

### 4. **test_code_agent.py** - Suite Completa de Tests

**Propósito:** Suite completa con múltiples categorías de tests.

**Qué verifica:**
- ✅ Disponibilidad de datos (13 municipios)
- ✅ Routing del supervisor (consultas simples, generales, comparaciones)
- ✅ Generación de código Python
- ✅ Ejecución de código en Safe REPL

**Ejecutar:**
```bash
./venv/bin/python test/chatbot/test_code_agent.py
# Responde selectivamente a cada tipo de test
```

**Tiempo:** Variable (1-3 minutos con todos los tests)  
**Costo:** ~$0.20-0.50 (según tests seleccionados)  
**Prerequisitos:** OPENAI_API_KEY en .env

---

### 5. **supervisor_code_agent_test.py** - Sistema Completo Interactivo

**Propósito:** Sistema completo en modo interactivo para pruebas manuales.

**Qué hace:**
- Inicia el chatbot completo text-to-python
- Permite hacer consultas en lenguaje natural
- Muestra el código generado
- Ejecuta el código y formatea respuestas

**Ejecutar:**
```bash
./venv/bin/python test/chatbot/supervisor_code_agent_test.py
```

**Ejemplos de consultas:**
```
¿Cuál es el promedio de viento en Riohacha?
¿Qué municipio tiene mayor temperatura?
Compara el viento entre Riohacha y Maicao
¿Cuál es la correlación entre temperatura y viento en Albania?
¿Qué es un modelo LSTM?  # Esta no genera código
```

**Tiempo:** Interactivo (5-10s por consulta)  
**Costo:** ~$0.035 por consulta  
**Salir:** Escribe 'exit'

---

## 🚀 Orden Recomendado de Ejecución

### Primera Vez (Validación Inicial):

```bash
# 1. Test básico de componentes (GRATIS)
./venv/bin/python test/chatbot/test_minimal.py

# 2. Test del sistema sin API (GRATIS)
./venv/bin/python test/chatbot/test_code_simple.py
# Responde 'n' al test LLM

# 3. Si ambos pasan, prueba el sistema completo (COSTO)
./venv/bin/python test/chatbot/test_analysis_validation.py
# Responde 'y' para ejecutar
```

### Desarrollo / Debugging:

```bash
# Si haces cambios al código, ejecuta primero:
./venv/bin/python test/chatbot/test_code_simple.py

# Luego valida con:
./venv/bin/python test/chatbot/test_analysis_validation.py
```

### Prueba Manual / Demo:

```bash
# Para demostrar el sistema:
./venv/bin/python test/chatbot/supervisor_code_agent_test.py
```

---

## 📊 Interpretación de Resultados

### ✅ Test PASSED
- El sistema funciona correctamente
- Los análisis son precisos
- Las respuestas contienen los valores correctos

### ⚠️ Test WARNED
- El sistema funciona pero hay pequeñas diferencias
- Puede ser redondeo o formato diferente
- Revisar manualmente si es aceptable

### ❌ Test FAILED
- El sistema tiene un problema
- Revisar los logs de error
- Verificar:
  1. OPENAI_API_KEY válida
  2. Archivos CSV presentes
  3. Dependencias instaladas

---

## 🔧 Troubleshooting

### Error: "OPENAI_API_KEY not found"
```bash
# Verificar que .env existe y tiene la key
cat .env | grep OPENAI_API_KEY
```

### Error: "Data not found"
```bash
# Verificar que los CSVs existen
ls -la data/raw/*.csv
```

### Error: "Import error"
```bash
# Re-instalar dependencias
./venv/bin/pip install -r requeriments.txt
```

### Exit code 136 en sandbox
```bash
# Ejecutar directamente con el Python del venv
./venv/bin/python test/chatbot/test_minimal.py

# O pedir permisos 'all' si usas el sandbox
```

---

## 📈 Métricas de Éxito

### Sistema Funcionando Correctamente:
- ✅ test_minimal.py: 100% imports exitosos
- ✅ test_code_simple.py: Todos los tests pasan
- ✅ test_analysis_validation.py: 3/3 tests PASSED
- ✅ Respuestas numéricamente precisas (<5% diferencia)

### Benchmarks Esperados:
- Tiempo de respuesta: 5-10 segundos por consulta
- Precisión numérica: >95%
- Tasa de éxito del routing: >90%
- Código generado ejecutable: >95%

---

## 💰 Costos Estimados

| Test | API Calls | Costo Aprox. | Tiempo |
|------|-----------|--------------|--------|
| test_minimal.py | 0 | $0 | 5s |
| test_code_simple.py | 0-1 | $0-0.005 | 10s |
| test_analysis_validation.py | 3 | $0.10 | 45s |
| test_code_agent.py (completo) | 6-12 | $0.20-0.50 | 2-3min |
| supervisor_code_agent_test.py | Por consulta | $0.035/query | 8s/query |

**Recomendación:** Ejecuta tests gratuitos frecuentemente, tests con costo ocasionalmente para validación.

---

## 📝 Autor

Eder Arley León Gómez  
Fecha: 2025-10-19

