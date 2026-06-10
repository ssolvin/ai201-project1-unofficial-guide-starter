import os
import chromadb
from chromadb.utils import embedding_functions

# ── Configuration ──────────────────────────────────────────────────────────────
CHROMA_DATA_PATH = "./chroma_db"
COLLECTION_NAME = "uci_cs_unofficial_guide"

# Initialize Persistent ChromaDB Client
# This saves the index to disk under the ./chroma_db directory
client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

# Set up the local embedding function using all-MiniLM-L6-v2
# ChromaDB handles downloading and executing this model locally via huggingface
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Get or create the collection, configuring it to use Cosine Distance
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_func,
    metadata={"hnsw:space": "cosine"}  # Lower score = closer/more relevant match
)


# ── Core Functions ─────────────────────────────────────────────────────────────
def embed_and_store(chunks):
    """
    Takes a list of processed chunks from ingest.py and stores them in ChromaDB.
    
    Args:
        chunks (list[dict]): List of dicts containing 'text', 'source', and 'chunk_index'
    """
    if not chunks:
        print("No chunks provided to store.")
        return

    print(f"Adding {len(chunks)} chunks to ChromaDB collection '{COLLECTION_NAME}'...")

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        # Build a unique ID for each snippet using source and index
        unique_id = f"{chunk['source'].replace('.txt', '')}_{chunk['chunk_index']}"
        ids.append(unique_id)
        documents.append(chunk["text"])
        
        # Store source metadata so the LLM can programmatically cite it later
        metadatas.append({
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"]
        })

    # ChromaDB natively handles batches; add everything to the store
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    print("Successfully embedded and stored all chunks.")


def retrieve(query, top_k=5):
    """
    Queries the vector database using semantic similarity search.
    
    Args:
        query (str): The user's text question.
        top_k (int): Number of top documents to return.
        
    Returns:
        list[dict]: Ranked matching text segments with metadata and distance scores.
    """
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    # Reformat ChromaDB's deeply nested output into a clean, easy-to-read list of dicts
    formatted_results = []
    
    # Check if we actually got results back
    if results and results["documents"] and len(results["documents"][0]) > 0:
        for i in range(len(results["documents"][0])):
            formatted_results.append({
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "chunk_index": results["metadatas"][0][i]["chunk_index"],
                "distance": results["distances"][0][i]  # Cosine distance
            })
            
    return formatted_results


# ── Quick Test Execution ───────────────────────────────────────────────────────
if __name__ == "__main__":
    # This block allows you to test retrieval independently directly from the terminal
    print(f"Testing connection to collection: '{COLLECTION_NAME}'")
    total_items = collection.count()
    print(f"Current total vector count in database: {total_items}")
    
    if total_items > 0:
        test_query = "What is the prerequisite for ICS 45C?"
        print(f"\nRunning test query: '{test_query}'")
        matches = retrieve(test_query, top_k=5)
        
        for idx, match in enumerate(matches):
            print(f"\n[{idx + 1}] Distance: {match['distance']:.4f} | Source: {match['source']}")
            print(f"    Text: {match['text']}")