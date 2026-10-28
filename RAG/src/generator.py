import os
import sys
import warnings
warnings.filterwarnings("ignore")

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_llm_model(model_name: str = None, temperature: float = 0.2):
    """
    Initializes Google Gemini with REST transport to prevent gRPC connection hangs on Windows.
    """
    model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables or .env file.")

    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=temperature,
        request_timeout=60.0,  # 60 seconds timeout
        max_retries=2          # Limit retries to avoid hanging indefinitely on network drops
    )

def build_rag_prompt(query: str, retrieved_docs: list) -> str:
    """
    Constructs an augmented RAG prompt using retrieved context chunks.
    """
    context_blocks = []
    for i, item in enumerate(retrieved_docs, 1):
        doc = item[0] if isinstance(item, tuple) else item
        source_file = os.path.basename(doc.metadata.get('source', 'N/A'))
        page_num = doc.metadata.get('page', 0) + 1

        context_blocks.append(
            f"[Document #{i} - Source: {source_file}, Page {page_num}]:\n{doc.page_content.strip()}"
        )

    context_str = "\n\n---\n\n".join(context_blocks)

    prompt = f"""You are a helpful and precise AI Research Assistant. Your task is to answer the user's question based ONLY on the provided document contexts below.

CRITICAL INSTRUCTIONS:
1. Answer the question using ONLY information explicitly mentioned in the context.
2. If the answer cannot be found in the provided context, state clearly: "The provided document does not contain enough information to answer this question."
3. Always cite your sources in your answer using the source file and page number provided in the context (e.g., [Explainable_GenerativeAI_GenXAI.pdf, Page 1]).

RETRIEVED CONTEXTS:
{context_str}

USER QUESTION:
{query}

ANSWER:"""

    return prompt

def generate_answer(query: str, retrieved_docs: list) -> str:
    """
    Standard generation mode returning full string output.
    """
    if not retrieved_docs:
        return "No context was provided by the retriever."

    full_prompt = build_rag_prompt(query, retrieved_docs)
    llm = get_llm_model()

    print("--> Sending Prompt to Gemini LLM (REST mode)...")
    response = llm.invoke(full_prompt)

    content = response.content
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, str):
                text_parts.append(part)
            elif isinstance(part, dict) and 'text' in part:
                text_parts.append(part['text'])
        return "\n".join(text_parts) if text_parts else str(content)

    return str(content)

def generate_answer_stream(query: str, retrieved_docs: list):
    """
    Real-time streaming output with explicit fallback to standard invoke.
    """
    if not retrieved_docs:
        print("No context was provided by the retriever.")
        return

    full_prompt = build_rag_prompt(query, retrieved_docs)
    llm = get_llm_model()

    print("--> Sending Prompt to Gemini LLM...")
    print("\n" + "="*70)
    print("🤖 RAG SYSTEM RESPONSE:")
    print("="*70)
    sys.stdout.flush()

    try:
        ans = generate_answer(query, retrieved_docs)
        print(ans)
    except Exception as e:
        print(f"\n❌ Error encountered while communicating with Gemini API: {e}")

    print("\n" + "="*70 + "\n")
    sys.stdout.flush()

if __name__ == "__main__":
    print("Generator module (Gemini REST) initialized successfully.")
