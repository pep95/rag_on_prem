import os
import pdb
import uuid
import time
import logging
from typing import List, Union
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, UpdateStatus
from sentence_transformers import SentenceTransformer
import re
from config import Settings
settings = Settings()
EMBEDDING_MODEL_PATH = settings.EMBEDDING_MODEL_PATH
VECTOR_DB_PATH = settings.VECTOR_DB_PATH
VECTORDB_COLLECTION_NAME = settings.VECTORDB_COLLECTION_NAME


logger = logging.getLogger(__name__)



class IngestionHandler:
    def __init__(self):
        self.__encoder = SentenceTransformer(EMBEDDING_MODEL_PATH)


        self.__qdrant_client = QdrantClient(path=VECTOR_DB_PATH)
        if settings.VECTORDB_COLLECTION_NAME not in [el.name for el in
                                                     self.__qdrant_client.get_collections().collections]:
            self.__collection = self.__qdrant_client.create_collection(
                collection_name=VECTORDB_COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=self.embedding_model.get_sentence_embedding_dimension(),
                    distance=models.Distance.COSINE,
                    on_disk=True))
        else:
            self.__collection = self.__qdrant_client.get_collection(collection_name=VECTORDB_COLLECTION_NAME)

    @property
    def embedding_model(self):
        return self.__encoder

    @property
    def persist_directory(self):
        return VECTOR_DB_PATH

    @property
    def collection(self):
        return self.__collection

    @property
    def vbd_client(self):
        return self.__qdrant_client


    def run_ingestion(self, texts_processed, text_not_preprocessed):
        start = time.time()

        # Update and store locally vectorstore
        logger.info(f"Appending to existing vectorstore at {VECTOR_DB_PATH}")

        #pdb.set_trace()
        if texts_processed:

            operation_info = self.__qdrant_client.upsert(collection_name=VECTORDB_COLLECTION_NAME,
                                                         wait=True,
                                                         points=[PointStruct(id=str(uuid.uuid4()),
                                                                             vector=self.__encoder.encode(
                                                                                 texts_processed[i]).tolist(),
                                                                             payload={"content": text_not_preprocessed[i]})
                                                                 for i in range(len(texts_processed))])

            if operation_info.status == UpdateStatus.COMPLETED:
                logger.info("Data inserted successfully!")
            else:
                logger.error("Failed to insert data")
        else:
            logger.error("No text to ingest")

        logger.info(f"Ingestion time: {round(time.time() - start, 2)}s\n")


    def search_context(self, query, num_target_source=5):
        query_embedding = self.embedding_model.encode([query])[0]

        document = self.vbd_client.search(collection_name=VECTORDB_COLLECTION_NAME,
                                          query_vector=query_embedding,
                                          limit=num_target_source)

        document = [doc.payload['content'] for doc in document]
        document = '\n\n'.join(document)
        context = re.sub('\s+', ' ', document)
        return context
