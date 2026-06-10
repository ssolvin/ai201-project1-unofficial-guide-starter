import os
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ── Configuration ──────────────────────────────────────────────────────────────
DOCS_DIR = "documents"          # folder where your .txt files live
CHUNK_SIZE = 350           # characters
CHUNK_OVERLAP = 60         # characters


# ── Loading ────────────────────────────────────────────────────────────────────
def load_documents(docs_dir):
    """Load all .txt files from the docs directory."""
    documents = []
    for filename in os.listdir(docs_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(docs_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({
                "source": filename,
                "text": text
            })
            print(f"Loaded: {filename} ({len(text)} characters)")
    return documents


# ── Cleaning ───────────────────────────────────────────────────────────────────
def clean_document(text):
    """Remove noise while keeping substantive content."""

    # Remove HTML tags if any slipped through
    text = re.sub(r"<[^>]+>", "", text)

    # Remove HTML entities
    text = text.replace("&amp;", "&")
    text = text.replace("&nbsp;", " ")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&#39;", "'")

    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)

    # Collapse multiple blank lines into one
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


# ── Chunking ───────────────────────────────────────────────────────────────────
def chunk_documents(documents):
    """Split documents into chunks with source metadata attached."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],  # respects paragraph breaks first
    )

    all_chunks = []
    for doc in documents:
        chunks = splitter.split_text(doc["text"])

        for i, chunk in enumerate(chunks):
            chunk = chunk.strip()
            if len(chunk) < 80: # Modified this from a length of 0, because we want to skip chunks that may be too small which are chunks with less than 80 characters
                continue  # skip empty chunks

            all_chunks.append({
                "text": chunk,
                "source": doc["source"],
                "chunk_index": i
            })

    return all_chunks


# ── Inspection ─────────────────────────────────────────────────────────────────
def inspect_chunks(chunks, n=5):
    """Print n random chunks for manual inspection."""
    import random
    print("\n" + "="*60)
    print(f"CHUNK INSPECTION — showing {n} random chunks")
    print("="*60)

    samples = random.sample(chunks, min(n, len(chunks)))
    for i, chunk in enumerate(samples):
        print(f"\n--- Chunk {i+1} ---")
        print(f"Source: {chunk['source']} | Index: {chunk['chunk_index']}")
        print(f"Length: {len(chunk['text'])} characters")
        print(f"Text:\n{chunk['text']}")

    print("\n" + "="*60)
    print(f"TOTAL CHUNKS: {len(chunks)}")
    print("="*60)


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Step 1: Loading documents...")
    documents = load_documents(DOCS_DIR)
    print(f"\nLoaded {len(documents)} documents.")

    print("\nStep 2: Cleaning documents...")
    for doc in documents:
        doc["text"] = clean_document(doc["text"])
    print("Cleaning complete.")

    # Print one full document to verify cleaning worked
    print("\n--- Sample cleaned document (first loaded) ---")
    print(documents[0]["text"][:1000])
    print("...[truncated]")

    print("\nStep 3: Chunking documents...")
    chunks = chunk_documents(documents)

    print("\nStep 4: Inspecting chunks...")
    inspect_chunks(chunks, n=5)

    print("\nDone. Review the chunks above before moving to embedding.")

    # ── NEW: Pass chunks directly into your new vector store ──
    print("\nStep 5: Seeding Vector Database...")
    from retriever import embed_and_store
    embed_and_store(chunks)

    print("\nDone. Ingestion and Vector Storage are complete!")