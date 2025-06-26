import os
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Chat with Daddy!", page_icon="🧔", layout="centered")

# Styling
st.markdown(
    """
    <style>
    .avatar {
        width: 100px;
        border-radius: 50%;
        margin-bottom: 10px;
    }
    .message-box {
        background-color: #f0f8ff;
        padding: 1em;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    .dad-message {
        background-color: #d1e7dd;
        color: #0f5132;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Dad avatar
st.image("https://lh3.googleusercontent.com/a/ACg8ocJ8H57tq5ydcX4yj6jb0qQ5qc5bws0FRAbVwb6mqr4EX6RA4w4vUg=s504-c-no", caption="Dad", use_container_width=False, width=100)

# Custom personality system message
PERSONALITY = (
    "You are a cool, funny dad chatting with your 9 and 11-year-old kids. "
    "You love joking around and being silly, but you’re also kind and caring. "
    "When the kids ask for something expensive, dangerous, or unreasonable, "
    "you say 'no' in a very sarcastic and funny way, like: 'Oh sure, let me just call the money tree.' "
    "Keep your language simple, clear, and age-appropriate. You like dad jokes, bad puns, and playful sarcasm."
)

st.title("👨‍👧‍👦 Chat with Dad")
st.write("Talk to your dad – he’s powered by Gemini!")

# Set up Gemini
api_key = os.environ['GOOGLE_API_KEY']
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

# Persistent chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.model_chat = model.start_chat(history=[])
    st.session_state.model_chat.send_message(PERSONALITY)
    st.session_state.model_chat.send_message("Hi kids! I'm your dad. Let's chat!")

# Input form to isolate submission
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", key="user_input")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.chat_history.append(("kid", user_input))
    try:
        response = st.session_state.model_chat.send_message(user_input)
        dad_reply = response.text.strip()
    except Exception as e:
        dad_reply = "Oops! Dad's having a tech issue. Try again later."

    st.session_state.chat_history.append(("dad", dad_reply))

# Show chat
for speaker, message in st.session_state.chat_history:
    if speaker == "kid":
        st.markdown(f"<div class='message-box'><strong>You:</strong> {message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='message-box dad-message'><strong>Dad:</strong> {message}</div>", unsafe_allow_html=True)
