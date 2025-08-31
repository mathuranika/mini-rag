import os
import argparse
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.retrievers import CohereRagRetriever



load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

PINECONE_INDEX_NAME = "mini-rag"
EMBEDDINGS_DIMENSIONS = 768

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def upsert_document(document_path: str, index_name: str):
    """
    Loads a document, splits it into chunks, and upserts the embeddings
    to the specified Pinecone index.
    """
    print(f"Loading document from {document_path}...")
    loader = PyPDFLoader(document_path)
    documents = loader.load()

    print("Splitting document into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    docs = text_splitter.split_documents(documents)

    print("Creating embeddings and upserting to Pinecone...")
    vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    vector_store.add_documents(docs)

    print("Document ingestion complete.")
    
def query_rag(question: str, index_name: str) -> str:
    """
    Queries the Pinecone index using RAG to generate an answer with citations.
    """
    # Connect to the Pinecone index
    vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)

    # Initialize the Google Gemini LLM
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    # Set up the retriever with the vector store
    retriever = vector_store.as_retriever()

    # Define a prompt template for the LLM
    template = """
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use inline citations to cite sources [1], [2], etc.

    Question: {question}
    Context: {context}
    Answer:
    """
    prompt = ChatPromptTemplate.from_template(template)

    # Set up a simpler chain
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    response = rag_chain.invoke(question)

    return response

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a RAG pipeline command.")
    parser.add_argument("--mode", type=str, required=True, choices=["ingest", "query"], help="The mode to run the script in (ingest or query).")
    parser.add_argument("--path", type=str, help="The path to the document to ingest.")
    parser.add_argument("--question", type=str, help="The question to ask the RAG pipeline.")

    args = parser.parse_args()

    if args.mode == "ingest":
        if not args.path:
            print("Error: --path is required for 'ingest' mode.")
        else:
            upsert_document(args.path, PINECONE_INDEX_NAME)
    elif args.mode == "query":
        if not args.question:
            print("Error: --question is required for 'query' mode.")
        else:
            answer = query_rag(args.question, PINECONE_INDEX_NAME)
            print(f"Answer: {answer}")