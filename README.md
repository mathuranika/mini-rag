# **Mini RAG App**

This is a Retrieval-Augmented Generation (RAG) application built as a solution for the AI Engineer Assessment. The application allows a user to upload a PDF document and then ask questions to a Large Language Model (LLM) that is grounded in the content of that document.

## **Architecture**

The application is structured with a clear separation of concerns between the frontend and a scalable backend API.

1. **Frontend (Streamlit)**: A user-friendly interface for document upload and querying. It sends API requests to the backend.  
2. **Backend (FastAPI)**: A Python web API that handles all the core logic, including document ingestion and RAG querying.  
3. **Vector Database (Pinecone)**: A hosted, cloud-based vector database that stores the numerical representations (embeddings) of the document chunks.  
4. **Embedding Model (Google Gemini)**: The GoogleGenerativeAIEmbeddings model is used to convert both the document chunks and the user's query into vectors.  
5. **Re-ranker (Cohere)**: The Cohere Rerank model is used to re-order the retrieved documents for improved relevance before they are passed to the LLM.  
6. **LLM (Google Gemini)**: The gemini-1.5-flash model generates the final answer based on the user's query and the relevant context.

## **Quick Start**

### **1\. Prerequisites**

* Python 3.10 or higher  
* Access to Google AI Studio to get your GOOGLE\_API\_KEY  
* A free account on Pinecone to get your API key and environment  
* A free account on Cohere to get your API key for re-ranking

### **2\. Setup**

1. Clone the repository and navigate into the project directory:  
   git clone \<your-repo-url\>  
   cd miniRAG

2. Create and activate a virtual environment:  
   python3 \-m venv venv  
   \# Mac/Linux:  
   source venv/bin/activate  
   \# Windows:  
   .\\venv\\Scripts\\activate

3. Install the required packages:  
   pip install \-r requirements.txt

4. Create a .env file in the root directory and add your API keys:  
   GOOGLE\_API\_KEY=your-google-api-key-here  
   PINECONE\_API\_KEY=your-pinecone-api-key-here  
   PINECONE\_ENVIRONMENT=your-pinecone-environment-here  
   COHERE\_API\_KEY=your-cohere-api-key-here

### **3\. Running the Application**

1. Start the Backend API:  
   Open a terminal, navigate to the miniRAG/backend directory, and run the API server.  
   cd backend  
   python \-m uvicorn api:app \--reload

2. Start the Frontend:  
   Open a second terminal, navigate back to the root miniRAG directory, and run the Streamlit app.  
   cd ..  
   streamlit run app.py

The application will open in your web browser. You can then upload a PDF and start asking questions.

## **Submission Checklist**

### **Evaluation**

I performed a minimal evaluation using a gold set of 5 Q\&A pairs on a test PDF. The success rate was high, with the model providing accurate answers grounded in the document content. The citations were correctly linked to the source material. The primary evaluation metric was the factual accuracy of the generated answers.

### **Chunking Strategy**

* **Chunk Size:** 1000 tokens  
* **Chunk Overlap:** 100 tokens

This strategy was chosen to balance chunk size with the need for sufficient overlap to maintain context between chunks.

### **Retriever & Reranker Settings**

The PineconeVectorStore.as\_retriever() with the GoogleGenerativeAIEmbeddings model was used for initial retrieval. The CohereRagRetriever was then used for re-ranking to improve the relevance of the retrieved documents before passing them to the LLM.

### **Remarks**

* **Trade-off: LLM for Citation:** A significant trade-off was using a general-purpose LLM (gemini-1.5-flash) to generate citations. While this approach works, a model specifically fine-tuned for this task or a more robust citation extraction method would improve accuracy and reliability.  
* **Provider Limits:** The free tier of Pinecone has limitations on the number of indexes and vectors that can be stored, which can impact the scale of the application. For a larger-scale project, a paid tier or alternative would be required.  
* **API Latency:** The sequential nature of the RAG chain (retrieve \-\> re-rank \-\> generate) can introduce latency. A more optimized, asynchronous pipeline could be implemented to improve response times for the user.

## **My Resume**

\[https://docs.google.com/document/d/1smIdmogt1pPw-W0T_ZVp9pufbAAoITHa/edit?usp=sharing&ouid=102107465474449019933&rtpof=true&sd=true\]