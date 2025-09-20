#!/bin/bash
# ============================================================================
# Script: download_data.sh
# Descripción: Arranca la API de clima en el puerto 8000,
#              liberando el puerto si ya está ocupado.
# Autor: Eder Arley León Gómez
# ============================================================================

# 1. Activar entorno virtual
source ../../venv/bin/activate

# 2. Variables de entorno
export DATA_DIR="./data/raw"
export STATE_DIR="./data/state"
export ENABLE_SCHEDULER="true"

# 3. Verificar si el puerto 8000 está en uso
PID=$(lsof -ti:8000)
if [ -n "$PID" ]; then
  echo "⚠️  El puerto 8000 está en uso por el proceso $PID. Matando proceso..."
  kill -9 $PID
  echo "✅ Puerto 8000 liberado."
fi

# 4. Crear carpetas de datos si no existen
mkdir -p $DATA_DIR $STATE_DIR

# 5. Ejecutar la API en el puerto 8000
echo "🚀 Iniciando API en http://127.0.0.1:8000"
exec uvicorn src.data_ingestion.data_API:app --host 0.0.0.0 --port 8000 --reload
