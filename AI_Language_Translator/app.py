import streamlit as st
import requests

# ----------------FRONTEND SETUP-------------------
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌐",
    layout="centered"
)

# Title
st.title("🌐 AI Language Translator")
st.write("Translate text into your preferred language using LangChain and Groq.")

# Language selection
language = st.selectbox(
    "Select target language",
    [
        "Telugu",
        "Hindi",
        "French",
        "Spanish",
        "German",
        "Japanese",
        "English"
    ]
)

# Text input
text = st.text_area(
    "Enter text to translate",
    placeholder="Example: I love programming."
)

# Translate button
if st.button("Translate", use_container_width=True):

    # Validate input
    if not text.strip():
        st.warning("Please enter some text to translate.")

    else:
        # LangServe API URL
        url = "http://localhost:8000/chain/invoke"

        # Data sent to backend
        payload = {
            "input": {
                "language": language,
                "text": text
            }
        }

        try:
            with st.spinner("Translating..."):
                response = requests.post(url, json=payload)

            # Check for errors
            if response.status_code == 200:

                result = response.json()

                st.success("Translation completed!")

                st.subheader("Translated Text")

                # Display output
                st.write(result["output"])

            else:
                st.error(
                    f"Backend Error: {response.status_code}"
                )
                st.write(response.text)

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to the backend. "
                "Make sure FastAPI is running on port 8000."
            )
