import os
import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

# Load environment configs
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize database components and local embedding encoder
client = chromadb.PersistentClient(path="./chroma_db")
# Ensure your collection name matches exactly what you configured in ingest.py
collection = client.get_or_create_collection(
    name="uci_cs_unofficial_guide", 
    metadata={"hnsw:space": "cosine"}
)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key=GROQ_API_KEY)

def ask(question: str):
    # 1. Vectorize query and extract top-k elements
    query_vector = embedding_model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=5  # Set to 5 as planned to offset catalog matching issues
    )
    
    # 2. Extract and format context string along with metadata origins
    retrieved_chunks = results["documents"][0] if results["documents"] else []
    # print(f"DEBUG CHUNKS FOUND: {retrieved_chunks}") # DEBUG PRINT REMOVE THIS LATER OR COMMENT OUT
    metadatas = results["metadatas"][0] if results["metadatas"] else []
    
    context_str = "\n\n".join([f"--- Snippet ---\n{text}" for text in retrieved_chunks])
    
    # Programmatic source logging guarantees the LLM can't mess it up
    unique_sources = sorted(list(set([meta["source"] for meta in metadatas if "source" in meta])))
    
    # 3. Formulate the strict grounding prompt
    system_instruction = (
        "You are an academic advisor helping students navigate UCI computer science courses. "
        "Answer the user's question using ONLY the provided text snippets below. Do not use your own external "
        "general knowledge, and do not assume or extrapolate facts. If the provided snippets do not contain "
        "the explicit facts required to completely answer the question, state exactly: "
        "'I don't have enough information on that.' Your response must be objective and directly grounded in the context."
    )
    
    user_content = f"Context Material:\n{context_str}\n\nUser Question: {question}"
    
    # 4. Request generation through Groq API
    completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_content}
        ],
        temperature=0.0  # Force maximum determinism to mitigate hallucinations
    )
    
    answer = completion.choices[0].message.content
    return {"answer": answer, "sources": unique_sources}