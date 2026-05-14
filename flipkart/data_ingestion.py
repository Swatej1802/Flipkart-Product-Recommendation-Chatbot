from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

from flipkart.data_converter import DataConverter
from flipkart.config import Config


class DataIngestor:

    def __init__(self):

        # Local embedding model
        self.embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # AstraDB Vector Store
        self.vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="flipkart_reviews",
            api_endpoint=Config.ASTRA_DB_API_ENDPOINT,
            token=Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace=Config.ASTRA_DB_KEYSPACE
        )

    # load_existing=True
    # If vectors already exist, just load them

    def ingest(self, load_existing=True):

        print("Loading vector store...")

        if load_existing:
            return self.vstore

        print("Converting CSV data into documents...")

        docs = DataConverter(
            "data/flipkart_product_review.csv"
        ).convert()

        print("Uploading documents to AstraDB...")

        self.vstore.add_documents(docs)

        print("Data ingestion completed successfully.")

        return self.vstore


if __name__ == "__main__":

    ingestor = DataIngestor()

    ingestor.ingest(load_existing=False)