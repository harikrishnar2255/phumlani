import os
import random
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖", layout="centered")

# --- CUSTOM CSS FOR BLUE, GREEN & GREY THEME ---
st.markdown(
    """
    <style>
    /* Main background & page styling */
    .stApp {
        background-color: #0f172a; /* Dark Slate Grey Background */
        color: #f8fafc;
    }
    
    /* Title and subtext styling */
    h1 {
        color: #38bdf8 !important; /* Vibrant Blue */
        text-align: center;
        font-weight: 700;
    }
    p {
        color: #94a3b8 !important; /* Cool Grey */
    }

    /* Input Box styling */
    div[data-baseweb="input"] {
        background-color: #1e293b !important;
        border: 2px solid #10b981 !important; /* Emerald Green Border */
        border-radius: 12px !important;
        color: #ffffff !important;
    }

    /* Custom classes for randomized message backgrounds */
    .bg-gradient-1 {
        background: linear-gradient(135deg, #1e3a8a 0%, #065f46 100%); /* Deep Blue to Forest Green */
    }
    .bg-gradient-2 {
        background: linear-gradient(135deg, #0f766e 0%, #334155 100%); /* Teal Green to Dark Grey */
    }
    .bg-gradient-3 {
        background: linear-gradient(135deg, #1d4ed8 0%, #475569 100%); /* Bright Blue to Slate Grey */
    }
    .bg-gradient-4 {
        background: linear-gradient(135deg, #059669 0%, #0284c7 100%); /* Emerald Green to Sky Blue */
    }

    /* Chat bubble container styling */
    .custom-chat-box {
        padding: 14px 18px;
        border-radius: 15px;
        margin-bottom: 12px;
        color: #ffffff;
        font-size: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🤖 Custom Groq Chatbot")
st.write("Powered by `openai/gpt-oss-120b` with Blue, Green & Grey styling")

# Initialize Groq client using environment variable 'x'
api_key = os.getenv("x")

if not api_key:
    st.error("API key not found! Please ensure variable 'x' is set in your .env file.")
else:
    client = Groq(api_key=api_key)

    # Initialize chat history and message styling map in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "styles" not in st.session_state:
        st.session_state.styles = []

    # Available randomized gradient classes
    gradients = [
        "bg-gradient-1",
        "bg-gradient-2",
        "bg-gradient-3",
        "bg-gradient-4",
    ]

    # Display prior chat messages with stored random gradient styles
    for idx, message in enumerate(st.session_state.messages):
        role_label = "👤 You" if message["role"] == "user" else "🤖 AI"
        gradient_class = st.session_state.styles[idx]

        st.markdown(
            f"""
            <div class="custom-chat-box {gradient_class}">
                <strong>{role_label}:</strong><br>{message['content']}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Accept user input
    if prompt := st.chat_input("Ask something..."):
        # Select a random color gradient for user message
        user_style = random.choice(gradients)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.styles.append(user_style)

        st.markdown(
            f"""
            <div class="custom-chat-box {user_style}">
                <strong>👤 You:</strong><br>{prompt}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Generate assistant response
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            assistant_message = response.choices[0].message.content

            # Select a random color gradient for assistant message
            assistant_style = random.choice(gradients)
            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_message}
            )
            st.session_state.styles.append(assistant_style)

            st.markdown(
                f"""
                <div class="custom-chat-box {assistant_style}">
                    <strong>🤖 AI:</strong><br>{assistant_message}
                </div>
                """,
                unsafe_allow_html=True,
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")