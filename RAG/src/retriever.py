import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from ingestion import load_and_split_documents

VECTORDB_DIR = "vectorstore"

def get_embedding_model():
    """
    Downloads/loads the HuggingFace sentence-transformer embedding model.
    Runs locally on CPU (~90MB model size).
    """
    print("--> Loading HuggingFace Embedding model (all-MiniLM-L6-v2)...")
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )

def get_vector_store(data_dir: str="data", force_rebuild: bool=False):
    """
    Load or create a Chroma vector store from documents in the specified directory.

    Args:
        data_dir (str): The directory containing the documents to load.
        force_rebuild (bool): If True, forces rebuilding the vector store even if it exists.

    Returns:
        Chroma: The loaded or newly created Chroma vector store.
    """
    embedding_fn = get_embedding_model()

    if os.path.exists(VECTORDB_DIR) and os.listdir(VECTORDB_DIR) and not force_rebuild:
        print(f"--> Existing Vector Store found at '{VECTORDB_DIR}'. Loading database...")
        vector_db = Chroma(
            persist_directory=VECTORDB_DIR,
            embedding_function=embedding_fn
        )
    else:
        print("--> Creating a new Vector Store from documents in 'data/'...")
        chunks = load_and_split_documents(data_dir=data_dir)
        if not chunks:
            raise ValueError("No text chunks found to embed into Vector Store.")
        print(f"--> Embedding {len(chunks)} chunks and saving to '{VECTORDB_DIR}'...")
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_fn,
            persist_directory=VECTORDB_DIR
        )
        print("--> Vector Store created and persisted successfully!")
    return vector_db

def search_documents(query: str, k: int = 3):
    """
    Search for k documents in the vector store that are most similar to the given query.
    """
    vector_db = get_vector_store()
    print(f"\n--> Searching Top-{k} relevant chunks for query: '{query}'...")

    results = vector_db.similarity_search_with_score(query, k=k)
    return results

if __name__ == "__main__":
    test_query = "What is Explainable Generative AI?"

    # Retrieve Top-3 relevant chunks with scores
    matched_results = search_documents(query=test_query, k=3)

    print("\n" + "="*70)
    print(f"RETRIEVAL RESULTS FOR QUERY: '{test_query}'")
    print("="*70)

    for i, item in enumerate(matched_results, 1):
        # Unpack tuple safely
        if isinstance(item, tuple) and len(item) == 2:
            doc, score = item
        else:
            doc, score = item, None

        source_file = os.path.basename(doc.metadata.get('source', 'N/A'))
        page_num = doc.metadata.get('page', 0) + 1

        score_str = f"{score:.4f}" if score is not None else "N/A"
        print(f"\n[Result #{i}] | Distance Score: {score_str}")
        print(f"📄 Source: {source_file} (Page {page_num})")
        print("Content Snippet:")
        print("-" * 50)
        print(doc.page_content.strip())
        print("-" * 50)
