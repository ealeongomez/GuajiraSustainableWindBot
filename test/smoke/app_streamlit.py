import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage, AIMessage
from dotenv import load_dotenv
import requests

# ==================================================
# Initial configuration
# ==================================================
load_dotenv()

# Función para obtener solo modelos LLM de Ollama (sin embeddings)
def get_ollama_llms():
    try:
        response = requests.get("http://localhost:11434/api/tags").json()
        modelos = [m["name"] for m in response["models"]]
        # Filtrar embeddings
        llms = [m for m in modelos if "embed" not in m.lower()]
        return llms
    except Exception:
        return ["ollama_no_disponible"]

# Sidebar with menu to choose model
st.sidebar.title("⚙️ Configuration")
provider = st.sidebar.selectbox("Choose the LLM provider:", ["OpenAI", "Ollama"])

if provider == "OpenAI":
    model_name = st.sidebar.selectbox("Modelo OpenAI:", ["gpt-3.5-turbo", "gpt-4"])
    llm = ChatOpenAI(model=model_name, temperature=0.7)
else:
    ollama_models = get_ollama_llms()
    model_name = st.sidebar.selectbox("Modelo Ollama:", ollama_models)
    llm = ChatOllama(model=model_name)

# ==================================================
# Principal interfaz
# ==================================================
st.title("🤖 Chatbot for sustainable energy planning in La Guajira")
st.write(f"Using **{provider} - {model_name}**")

# Initialize history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    else:
        st.chat_message("assistant").write(msg.content)

# User input
if prompt := st.chat_input("Write your message..."):
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    response = llm(st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=response.content))
    st.chat_message("assistant").write(response.content)
