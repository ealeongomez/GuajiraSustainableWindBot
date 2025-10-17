# Ejemplo: Streamlit ChatBot con Docker y OpenAI

Este ejemplo muestra cómo dockerizar una aplicación de Streamlit que usa LangChain con OpenAI para crear un chatbot de pronóstico de viento.

## 📋 Contenido

- `app_streamlit.py`: Aplicación Streamlit con interfaz de chat
- `Dockerfile`: Configuración de Docker para la aplicación
- `requirements.txt`: Dependencias de Python
- `.dockerignore`: Archivos a excluir del build
- `.env.example`: Plantilla para variables de entorno

## 🏗️ Arquitectura

La aplicación usa:
- **Streamlit**: Framework para la interfaz web
- **LangChain**: Para integración con modelos LLM
- **OpenAI**: Proveedor de modelos (GPT-3.5-turbo, GPT-4, GPT-4-turbo)

## 📦 Pre-requisitos

Antes de iniciar, asegúrate de tener instalado:
- **Docker Desktop** (para Mac/Windows) o **Docker Engine** (para Linux)
- **OpenAI API Key** - Obtén una en [OpenAI Platform](https://platform.openai.com/api-keys)

### Verificar instalación de Docker

```bash
# Verificar que Docker está instalado
docker --version
# Output esperado: Docker version 24.x.x, build ...

# Verificar que Docker daemon está corriendo
docker ps
# Si funciona, verás una lista de contenedores (puede estar vacía)
```

**⚠️ Si obtienes un error**: Inicia Docker Desktop desde tu aplicación y espera a que el ícono de Docker en la barra superior esté activo.

## 🚀 Inicialización de Docker - Paso a Paso

### Paso 1: Navegar al directorio del ejemplo

```bash
cd examples/streamlit-docker-openai
```

### Paso 2: Construir la imagen Docker

```bash
docker build -t wind-forecast-app .
```

**¿Qué hace esto?**
- Lee el `Dockerfile` y construye una imagen
- Descarga Python 3.11-slim como base
- Instala todas las dependencias de `requirements.txt`
- Copia el código de la aplicación
- Etiqueta la imagen como `wind-forecast-app`

**Tiempo estimado**: 2-5 minutos (primera vez)

### Paso 3: Ejecutar el contenedor

Tienes dos opciones para pasar tu API key:

#### Opción A: API Key directamente en el comando

```bash
docker run -d --name streamlit-docker-openai -p 8501:8501 \
  -e OPENAI_API_KEY=sk-tu-api-key-aqui wind-forecast-app
```

#### Opción B: Usando archivo .env (Recomendado)

```bash
# 1. Crear archivo .env
echo "OPENAI_API_KEY=sk-tu-api-key-aqui" > .env

# 2. Ejecutar con el archivo .env
docker run -d --name streamlit-docker-openai -p 8501:8501 \
  --env-file .env wind-forecast-app
```

**¿Qué hace esto?**
- `-d`: Ejecuta el contenedor en segundo plano (detached mode)
- `--name streamlit-docker-openai`: Asigna un nombre personalizado al contenedor
- `-p 8501:8501`: Mapea el puerto 8501 del contenedor al puerto 8501 de tu máquina
- `-e` o `--env-file`: Pasa variables de entorno al contenedor
- `wind-forecast-app`: Nombre de la imagen a ejecutar

### Paso 4: Acceder a la aplicación

Abre tu navegador en: **http://localhost:8501**

Deberías ver la interfaz de Streamlit con el chatbot listo para usar.

## 🛠️ Comandos de Gestión de Docker

### Detener el contenedor

```bash
# Usando el nombre del contenedor
docker stop streamlit-docker-openai

# O usando el ID
docker ps                        # Ver ID del contenedor
docker stop <container_id>
```

### Ver logs

```bash
# Ver logs completos
docker logs streamlit-docker-openai

# Seguir logs en tiempo real
docker logs -f streamlit-docker-openai

# Ver últimas 50 líneas
docker logs --tail 50 streamlit-docker-openai
```

### Reiniciar el contenedor

```bash
# Reiniciar contenedor existente
docker restart streamlit-docker-openai

# Iniciar contenedor detenido
docker start streamlit-docker-openai
```

### Ver contenedores e imágenes

```bash
# Ver contenedores corriendo
docker ps

# Ver todos los contenedores (incluso detenidos)
docker ps -a

# Ver imágenes Docker
docker images

# Ver uso de espacio
docker system df
```

### Limpiar recursos Docker

```bash
# Detener y eliminar el contenedor
docker rm -f streamlit-docker-openai

# Eliminar solo si está detenido
docker rm streamlit-docker-openai

# Eliminar imagen
docker rmi wind-forecast-app

# Eliminar todos los contenedores detenidos
docker container prune

# Eliminar imágenes sin usar
docker image prune

# Limpieza completa (¡cuidado!)
docker system prune -a
```

### Reconstruir la imagen (después de cambios en el código)

```bash
# Reconstruir con caché
docker build -t wind-forecast-app .

# Reconstruir sin caché (fuerza descarga de todo)
docker build --no-cache -t wind-forecast-app .
```

## 🔍 Troubleshooting

### Error: "Cannot connect to Docker daemon"

**Problema**: Docker no está corriendo.

**Solución**:
```bash
# Mac: Abre Docker Desktop desde Applications
# Verifica que el ícono de Docker aparezca en la barra superior
# Espera a que el ícono deje de estar animado

# Linux: Inicia el servicio
sudo systemctl start docker
```

### Error: "port is already allocated"

**Problema**: El puerto 8501 ya está en uso.

**Solución 1**: Detén la aplicación que está usando el puerto.
```bash
# Mac/Linux: Encontrar proceso usando el puerto
lsof -i :8501
kill -9 <PID>
```

**Solución 2**: Usa un puerto diferente.
```bash
docker run -p 8502:8501 --env-file .env wind-forecast-app
# Accede en: http://localhost:8502
```

### Error: "invalid API key"

**Problema**: La API key de OpenAI no es válida.

**Solución**:
- Verifica que tu API key sea correcta en [OpenAI Platform](https://platform.openai.com/api-keys)
- Asegúrate de que comience con `sk-`
- Revisa que no haya espacios extras en el archivo `.env`

### La imagen es muy grande

**Solución**: La imagen usa `python:3.11-slim` que ya es optimizada. Si necesitas reducir más:
```bash
# Usar alpine (más pequeño pero puede tener problemas de compatibilidad)
# Modificar la primera línea del Dockerfile:
FROM python:3.11-alpine
```

## 🚀 Uso Rápido (Resumen)

### Opción 1: Con Docker (Recomendado para producción)

```bash
# 1. Construir la imagen
docker build -t wind-forecast-app .

# 2. Ejecutar con tu API key
docker run -p 8501:8501 -e OPENAI_API_KEY=tu-api-key wind-forecast-app

# 3. Abrir en el navegador
# http://localhost:8501
```

### Opción 2: Sin Docker (Desarrollo local)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu OPENAI_API_KEY

# 3. Ejecutar la aplicación
streamlit run app_streamlit.py
```

## ⚙️ Características

- **Selección de Modelo**: Elige entre diferentes modelos de OpenAI (GPT-3.5, GPT-4, GPT-4-turbo)
- **Control de Temperatura**: Ajusta la creatividad de las respuestas (0.0-1.0)
- **Historial de Chat**: Mantiene el contexto de la conversación
- **Interfaz Moderna**: UI limpia y responsiva con Streamlit

## 🐳 Detalles del Dockerfile

```dockerfile
FROM python:3.11-slim          # Imagen base ligera
WORKDIR /app                   # Directorio de trabajo
COPY requirements.txt .        # Copiar dependencias
RUN pip install --no-cache-dir # Instalar sin cache
COPY app_streamlit.py .        # Copiar código
EXPOSE 8501                    # Puerto de Streamlit
CMD ["streamlit", "run", ...]  # Comando de inicio
```

## 🔧 Configuración

### Variables de Entorno

- `OPENAI_API_KEY`: (Requerido) Tu API key de OpenAI

### Puertos

- **8501**: Puerto por defecto de Streamlit

### Modelos Disponibles

- `gpt-3.5-turbo`: Rápido y económico, ideal para la mayoría de tareas
- `gpt-4`: Mayor capacidad de razonamiento y precisión
- `gpt-4-turbo-preview`: Versión mejorada de GPT-4 con ventana de contexto mayor

## 📝 Notas

- El contenedor ejecuta Streamlit en modo servidor (`--server.address=0.0.0.0`)
- Incluye healthcheck para monitoreo en producción
- La imagen usa Python 3.11 slim para optimizar tamaño
- `.dockerignore` excluye archivos innecesarios del build

## 🎯 Casos de Uso

Este ejemplo es útil para:
- Desplegar chatbots con LLM en producción
- Prototipar interfaces conversacionales rápidamente
- Aprender integración de Streamlit + Docker + LangChain + OpenAI
- Testing de aplicaciones antes de desplegar en la nube
- Baseline para comparar con modelos locales (Ollama, etc.)

## 💡 Próximos Pasos

Para extender este ejemplo puedes:
- Agregar memoria persistente con bases de datos
- Implementar RAG (Retrieval Augmented Generation)
- Integrar con tus modelos de pronóstico de viento
- Añadir autenticación de usuarios
- Implementar streaming de respuestas

## 📚 Referencias

- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain OpenAI Integration](https://python.langchain.com/docs/integrations/platforms/openai)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

