import streamlit as st
from google import genai
from google.genai import types

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Keerthana Gemini AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ============================================================
# GOOGLE AI STUDIO API KEY
# ============================================================

# IMPORTANT:
# Replace the text below with your own Google AI Studio API key.

GOOGLE_API_KEY = "AQ.Ab8RN6KIvTkLEEOwGByj5pvyncvsEcNRfT82hd82K9Mlhx_0AQ"


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=GOOGLE_API_KEY)

# Current Gemini model used by the Google documentation
MODEL_NAME = MODEL_NAME = "gemini-3.1-flash-lite"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */
    .stApp {
        background: linear-gradient(
            135deg,
            #f5f7ff 0%,
            #eef2ff 50%,
            #f8f9ff 100%
        );
    }

    /* Header */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
        color: #4f46e5;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #555;
        margin-bottom: 25px;
    }

    /* Info card */
    .info-card {
        padding: 18px;
        border-radius: 15px;
        background: white;
        border: 1px solid #e4e7ec;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
    }

    /* Chat container */
    .chat-box {
        background: white;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0px 5px 20px rgba(0,0,0,0.06);
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #777;
        font-size: 13px;
        margin-top: 30px;
        padding: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">🤖 Keerthana Gemini AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Chat with Google Gemini using Google AI Studio API</div>',
    unsafe_allow_html=True
)


# ============================================================
# API KEY CHECK
# ============================================================

if GOOGLE_API_KEY == "PASTE_YOUR_GOOGLE_AI_STUDIO_API_KEY_HERE":

    st.error(
        "⚠️ Please add your Google AI Studio API key inside the "
        "GOOGLE_API_KEY variable in app.py."
    )

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Chat Settings")

    st.write("### 🤖 Model")
    st.info(MODEL_NAME)

    st.write("### 💬 Conversation")

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()

    st.write("---")

    st.write("### ✨ Features")

    st.write("✅ Google Gemini AI")
    st.write("✅ Streamlit interface")
    st.write("✅ Conversation history")
    st.write("✅ Beginner friendly")
    st.write("✅ Real-time responses")

    st.write("---")

    st.caption("Powered by Google Gemini API")


# ============================================================
# WELCOME MESSAGE
# ============================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div class="info-card">

        👋 <b>Welcome to Keerthana Gemini AI Chatbot!</b>

        <br><br>

        Ask me anything about:
        <br>
        💻 Programming &nbsp;&nbsp;
        📚 Education &nbsp;&nbsp;
        🤖 Artificial Intelligence
        <br>
        🐍 Python &nbsp;&nbsp;
        🌐 Web Development &nbsp;&nbsp;
        💡 General Questions

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DISPLAY PREVIOUS CHAT MESSAGES
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

user_prompt = st.chat_input(
    "💬 Type your message here..."
)


# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if user_prompt:

    # --------------------------------------------------------
    # Display user message
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(user_prompt)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )


    # --------------------------------------------------------
    # Generate Gemini response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("🤔 Gemini is thinking..."):

            try:

                # Create Gemini conversation history
                history = []

                for message in st.session_state.messages[:-1]:

                    if message["role"] == "user":

                        history.append(
                            types.Content(
                                role="user",
                                parts=[
                                    types.Part(
                                        text=message["content"]
                                    )
                                ]
                            )
                        )

                    elif message["role"] == "assistant":

                        history.append(
                            types.Content(
                                role="model",
                                parts=[
                                    types.Part(
                                        text=message["content"]
                                    )
                                ]
                            )
                        )


                # Create a Gemini chat with previous history
                chat = client.chats.create(
                    model=MODEL_NAME,
                    history=history
                )


                # Send current message
                response = chat.send_message(
                    message=user_prompt
                )


                # Get response text
                assistant_response = response.text


                # Display response
                st.markdown(assistant_response)


                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_response
                    }
                )


            except Exception as e:

                error_message = f"""
                ❌ **Something went wrong.**

                Please check:

                1. Your Google AI Studio API key
                2. Your internet connection
                3. Your Gemini API access
                4. Whether your API key is active

                **Error details:**
                `{str(e)}`
                """

                st.error(error_message)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🤖 Keerthana Gemini AI Chatbot
        <br>
        Built with Python + Streamlit + Google Gemini API
    </div>
    """,
    unsafe_allow_html=True
)