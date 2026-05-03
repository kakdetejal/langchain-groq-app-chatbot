import streamlit as st
from app.chains import get_chain

# Initialize chain once (important for performance)
chain = get_chain()

st.set_page_config(page_title="Groq AI Chatbot", page_icon="🤖")

st.title("🤖 Groq Tech AI Assistant (Alex)")
st.write("Ask any tech-related questions. Type 'exit' to stop session.")

# -----------------------------
# SESSION MEMORY SETUP
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # stores full chat history

# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# USER INPUT BOX
# -----------------------------
user_input = st.chat_input("Type your tech query here...")

if user_input:

    # Handle exit condition
    if user_input.lower() == "exit":
        st.warning("Session ended. Refresh to restart.")
        st.stop()

    # Store user message in memory
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Show user message in UI
    with st.chat_message("user"):
        st.markdown(user_input)

    # -----------------------------
    # CREATE CONTEXT FROM MEMORY
    # -----------------------------
    # Convert chat history into a simple prompt context
    conversation_history = ""

    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation_history += f"{role}: {msg['content']}\n"

    # -----------------------------
    # GET RESPONSE FROM LLM
    # -----------------------------
    response = chain.invoke({
        "input": f"{conversation_history}\nUser: {user_input}"
    })

    # -----------------------------
    # STORE ASSISTANT RESPONSE
    # -----------------------------
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(response)