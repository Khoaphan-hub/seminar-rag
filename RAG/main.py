import os
import sys

# Append src/ directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from retriever import search_documents, get_vector_store
from generator import generate_answer_stream

def ask_rag_system(question: str, top_k: int = 5):
    """
    Executes a single RAG query pipeline with context inspection.
    """
    print("\n" + "="*70)
    print(f"❓ USER QUESTION: {question}")
    print("="*70)

    # 1. RETRIEVAL
    retrieved_results = search_documents(query=question, k=top_k)
    print(f"--> Found {len(retrieved_results)} relevant document chunks:")

    # INSPECT RETRIEVED SOURCES
    for idx, item in enumerate(retrieved_results, 1):
        doc, score = item if isinstance(item, tuple) else (item, None)
        src = os.path.basename(doc.metadata.get('source', 'N/A'))
        pg = doc.metadata.get('page', 0) + 1
        score_info = f" | Distance: {score:.4f}" if score is not None else ""
        print(f"   [{idx}] Source: {src} (Page {pg}){score_info}")

    print("-" * 70)

    # 2. GENERATION (STREAMING)
    generate_answer_stream(query=question, retrieved_docs=retrieved_results)

def start_interactive_cli():
    """
    Runs an interactive CLI chat loop for continuous querying.
    """
    print("="*70)
    print("🚀 RAG SYSTEM INTERACTIVE CHATBOT (CS420 - Topic S07: GenXAI)")
    print("Pre-loading Vector Store into memory...")

    # Warm up / Load VectorDB once at startup
    get_vector_store()

    print("System Ready! Type 'exit' or 'quit' anytime to end the session.")
    print("="*70)

    while True:
        try:
            user_query = input("\n❓ Enter your question: ").strip()

            # Check exit triggers
            if user_query.lower() in ['exit', 'quit', 'q']:
                print("\n--> Exiting RAG System. Goodbye!")
                break

            # Ignore empty inputs
            if not user_query:
                print("--> Question cannot be empty. Please enter a valid question.")
                continue

            # Process query
            ask_rag_system(user_query, top_k=5)

        except KeyboardInterrupt:
            print("\n\n--> Session terminated by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error encountered while processing request: {e}")

if __name__ == "__main__":
    start_interactive_cli()
