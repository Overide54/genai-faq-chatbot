import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Page config MUST come after importing streamlit
st.set_page_config(page_title="GenAI FAQ Chatbot", page_icon="🤖")

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# FAQ context
faq_context = """
Company working hours are from 9 AM to 6 PM.
Employees are entitled to 20 paid leaves per year.
Password reset can be done via the IT self-service portal.
Employees must apply leave at least one day in advance.
For system issues, contact IT support via internal ticketing system.
"""

# UI
st.title("🤖 GenAI FAQ Chatbot")
st.write("Ask any HR or IT related question")

user_question = st.text_input("Enter your question")

if st.button("Get Answer") and user_question:
    with st.spinner("Thinking... 🤖"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful company HR and IT support assistant. "
                            "Answer ONLY based on the provided FAQ context. "
                            "If the answer is not in the context, say "
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

            answer = response.choices[0].message.content
            st.success(answer)

        except Exception as e:
            st.error(f"Error: {e}")

