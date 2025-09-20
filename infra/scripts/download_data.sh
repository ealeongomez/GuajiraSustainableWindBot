#!/bin/bash
# ============================================================================
# Script: download_data.sh
# Descripción: Lanza la descarga de datos climáticos vía API
# Autor: Eder Arley León Gómez
# ============================================================================

API_URL="http://127.0.0.1:8000"

# 1. Verificar que la API esté corriendo
if ! curl -s "$API_URL/health" > /dev/null; then
  echo "❌ La API no está disponible en $API_URL"
  echo "👉 Primero ejecuta: ./infra/scripts/run_api.sh"
  exit 1
fi

# 2. Actualización incremental horaria (última hora de todos los municipios)
echo "⏳ Ejecutando actualización horaria de todos los municipios..."
curl -s -X POST "$API_URL/update/hourly" \
     -H "Content-Type: application/json" \
     -d '{"wind_only": false}' | jq .

# 3. (Opcional) Descarga completa de 5 años
# echo "📥 Ejecutando descarga histórica de 5 años..."
# curl -s -X POST "$API_URL/download/full" \
#      -H "Content-Type: application/json" \
#      -d '{"wind_only": false}' | jq .
