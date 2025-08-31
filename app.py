import streamlit as st
import requests
import os

# Load environment variables (from .env file)
from dotenv import load_dotenv
load_dotenv()

BACKEND_API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Mini RAG App", page_icon="📄")

st.title("📄 AI Engineer Assessment: Mini RAG App")
st.subheader("Answer questions about your documents using an LLM")

# Sidebar for document ingestion
with st.sidebar:
    st.header("Document Ingestion")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file and st.button("Ingest Document"):
        with st.spinner("Ingesting document..."):
            # Save file to a temp location
            temp_file_path = f"temp_doc_{uploaded_file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Send path to the backend for ingestion
            response = requests.post(f"{BACKEND_API_URL}/ingest", json={"document_path": temp_file_path})

            if response.status_code == 200:
                st.success("Document ingested successfully!")
            else:
                st.error(f"Error ingesting document: {response.text}")

            os.remove(temp_file_path) # Clean up the temp file

# querying
st.markdown("---")
query = st.text_area("Enter your question:", height=100)

if st.button("Get Answer"):
    if query:
        with st.spinner("Getting answer..."):
            response = requests.post(f"{BACKEND_API_URL}/query", json={"question": query})

            if response.status_code == 200:
                answer = response.json().get("answer")
                if answer:
                    st.markdown("### Answer")
                    st.success(answer)
                else:
                    st.error("No answer found.")
            else:
                st.error(f"Error: {response.text}")
    else:
        st.warning("Please enter a question.")