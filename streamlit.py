import streamlit as st
from groq_helper import get_legal_response
from utils import generate_pdf
import speech_recognition as sr
import datetime
import pyaudio

# Set page config
st.set_page_config(page_title="Legal Bot", layout="wide")

# Title section
st.markdown("""
    <h1 style='text-align: center;'>⚖️ Legal Assistant Chatbot</h1>
    <p style='text-align: center;'>Type or speak your legal question. Get instant AI response and download a PDF!</p>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🧰 Options")
    st.markdown("Use voice or text input. Also try example prompts:")
    if st.button("🔄 Use Sample 1"):
        st.session_state["question"] = "What are my rights if I get fired unfairly?"
    if st.button("🔄 Use Sample 2"):
        st.session_state["question"] = "How can I file for divorce in India?"

    st.markdown("Made with ❤️ by YourBot")

# Voice input option
with st.expander("🎙️ Use Voice Input", expanded=False):
    st.info("Click below and speak your question...")
    if st.button("🎧 Start Listening"):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening for 4 seconds...")
            audio = r.listen(source, phrase_time_limit=4)
        try:
            voice_text = r.recognize_google(audio)
            st.session_state["question"] = voice_text
            st.success(f"Captured voice: '{voice_text}'")
        except Exception as e:
            st.error(f"Could not understand audio. Error: {e}")

# Question input
question = st.text_area("📝 Enter your legal question:", value=st.session_state.get("question", ""),
                        key="question_input")

# Submit & show result
if st.button("🔍 Get Answer"):
    if question.strip() == "":
        st.warning("Please enter or speak your question first.")
    else:
        with st.spinner("🧠 AI is analyzing your query..."):
            response = get_legal_response(question)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            filename = generate_pdf(question, response, filename=f"legal_response_{timestamp}.pdf")

        st.success("✅ Response Ready!")
        st.markdown("### 💬 Answer")
        st.markdown(response)

        # Download PDF
        with open(filename, "rb") as file:
            st.download_button("📄 Download as PDF", file, file_name=filename, mime="application/pdf")

# Optional: Show history
with st.expander("📜 Chat History", expanded=False):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if question and "response" in locals():
        st.session_state.chat_history.append((question, response))
    for q, r in reversed(st.session_state.chat_history[-5:]):
        st.markdown(f"**Q:** {q}")
        st.markdown(f"**A:** {r}")
        st.markdown("---")
