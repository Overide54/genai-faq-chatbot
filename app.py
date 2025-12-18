import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

load_dotenv()

st.set_page_config(page_title="GenAI FAQ Chatbot", page_icon="🤖")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ GROQ_API_KEY not found. Please check environment variables.")
    st.stop()

client = Groq(api_key=api_key)

faq_context = """
Company working hours are from 9 AM to 6 PM.
Employees are entitled to 20 paid leaves per year.
Password reset can be done via the IT self-service portal.
Employees must apply leave at least one day in advance.
For system issues, contact IT support via internal ticketing system.
"""

st.title("🤖 GenAI FAQ Chatbot")
st.write("Ask any HR or IT related question")

user_question = st.text_input("Enter your question")

if st.button("Get Answer") and user_question:
    with st.spinner("Thinking... 🤖"):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful HR and IT support assistant. "
                            "Answer only from the provided FAQ context. "
                            "If the answer is not present, say "
                            "'Please contact HR or IT support for this query.'"
                        )
                    },
                    {
                        "role": "system",
                        "content": f"FAQ Context:\n{faq_context}"
                    },
                    {
                        "role": "user",
                        "content": user_question
                    }
                ],
                temperature=0.2
            )

            st.success(response.choices[0].message.content)

        except Exception as e:
            st.error(f"LLM Error: {e}")
