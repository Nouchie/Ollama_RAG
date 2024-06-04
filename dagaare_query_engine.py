import os
from llama_index.readers.file import PDFReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import StorageContext, VectorStoreIndex

def create_dagaare_dictionary_engine():
    try:
        pdf_path = os.path.join("data", "Dagaare_dictionary.pdf")
        if not os.path.isfile(pdf_path):
            print(f"PDF file not found: {pdf_path}")
            return None

        Dagaare_dictionary_pdf = PDFReader().load_data(file=pdf_path)
        if not Dagaare_dictionary_pdf:
            print(f"No data loaded from the PDF: {pdf_path}")
            return None

        embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

        index = VectorStoreIndex.from_documents(Dagaare_dictionary_pdf, embed_model=embed_model, show_progress=True)
        index.storage_context.persist(persist_dir="Dagaare")

        Dagaare_dictionary_engine = index.as_query_engine()

        return Dagaare_dictionary_engine

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Instantiate the query engine
Dagaare_dictionary_engine = create_dagaare_dictionary_engine()
