import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter




def load_and_split_documents(data_dir: str="data", chunk_size: int=500, chunk_overlap: int=50):
    """
    Load and split documents from the specified directory.

    Args:
        data_dir (str): The directory containing the documents to load.
    """
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory '{data_dir}' does not exist.")

    # Load documents from the specified directory
    print(f"Loading documents from directory: {data_dir}")
    loader = PyPDFDirectoryLoader(data_dir)
    documents = loader.load()

    if not documents:
        raise ValueError(f"No documents found in the directory '{data_dir}'.")
        return []
    print(f"Loaded {len(documents)} documents successfully.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")

    return chunks

if __name__ == "__main__":
    DATA_PATH = "data"  # Specify the path to your data directory
    # Create the data directory if it does not exist.
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        print(f"Created directory '{DATA_PATH}'. Please place your PDF files in this directory and run the script again.")
    else:
        sample_chunks = load_and_split_documents(data_dir=DATA_PATH)

        if sample_chunks:
            print("\n--- TEST SAMPLE CHUNK ---")
            print(f"SourceFile: {sample_chunks[0].metadata.get('source')}")
            print(f"Page   : {sample_chunks[0].metadata.get('page') + 1}") #type: ignore
            print(f"Content   :\n{sample_chunks[0].page_content}")
