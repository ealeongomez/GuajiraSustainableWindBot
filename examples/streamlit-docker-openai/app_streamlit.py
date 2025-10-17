import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from dotenv import load_dotenv

# ==================================================
# Initial configuration
# ==================================================
load_dotenv()

# Sidebar with menu to choose OpenAI model
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("**LLM Provider:** OpenAI")
model_name = st.sidebar.selectbox(
    "Choose OpenAI Model:", 
    ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"]
)
temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Initialize the LLM
llm = ChatOpenAI(model=model_name, temperature=temperature)

# ==================================================
# Principal interfaz
# ==================================================
st.title("🤖 AI-Based Wind Forecasting System for La Guajira")
st.write(f"Using **OpenAI - {model_name}** (Temperature: {temperature})")

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
