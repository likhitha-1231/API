
import streamlit as st
from groq import Groq

# Your Groq API key
GROQ_API_KEY = "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"

# Create Groq client
client = Groq(api_key=GROQ_API_KEY)

# Page settings
st.set_page_config(
    page_title="Groq AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 Groq AI Chatbot")
st.write("Chat with Groq AI")

# Get available Groq models
try:
    models = client.models.list()

    available_models = [model.id for model in models.data]

    preferred_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "qwen/qwen3-32b"
    ]

    selected_model = None

    for model in preferred_models:
        if model in available_models:
            selected_model = model
            break

    if selected_model is None and available_models:
        selected_model = available_models[0]

except Exception as e:
    st.error("Unable to get Groq models.")
    st.code(str(e))
    st.stop()

# Show selected model
st.caption(f"Using model: {selected_model}")

# Create conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_message = st.chat_input("Type your message...")

if user_message:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_message)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=st.session_state.messages,
                    temperature=0.7
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

                # Save AI response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error("Groq API Error")
                st.code(str(e))

# Clear conversation
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()
