from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    """
    This class is used to set up the environment configurations.
    """

    # Environment variables
    ENV: str = os.environ.get('ENV')
    PREFIX: str = "/rag"

    # Resource paths useful for elaboration
    PATH_RES: str = os.path.join(os.getcwd(), "resources")
    STOP_WORD_PATH: str = os.path.join(PATH_RES, "stopwords-it.txt")
    MANAGED_EXTENSION = ['.pdf','.txt']

    #os.environ["MODEL_PATH"] = r"PATH TO .gguf MODEL"
    os.environ["VECTOR_DB_PATH"] = os.path.join(PATH_RES, "qdrant_db")
    os.environ["VECTORDB_COLLECTION_NAME"] = "test_rag"
    os.environ["EMBEDDING_MODEL_PATH"] = "nickprock/sentence-bert-base-italian-uncased"
    os.environ["PROMPT_PATH_WITHOUT_CONTEXT"] = os.path.join(PATH_RES, "PROMPT_WITHOUT_CONTEXT.txt")
    os.environ["PROMPT_PATH_WITH_CONTEXT1"] = os.path.join(PATH_RES, "PROMPT_WITH_CONTEXT_pt1.txt")
    os.environ["PROMPT_PATH_WITH_CONTEXT2"] = os.path.join(PATH_RES, "PROMPT_WITH_CONTEXT_pt2.txt")

    MODEL_PATH: str = os.environ.get("MODEL_PATH")
    VECTOR_DB_PATH: str = os.environ.get("VECTOR_DB_PATH")
    VECTORDB_COLLECTION_NAME: str = os.environ.get("VECTORDB_COLLECTION_NAME")
    EMBEDDING_MODEL_PATH: str = os.environ.get("EMBEDDING_MODEL_PATH")
    PROMPT_WITHOUT_CONTEXT: str = os.environ.get("PROMPT_PATH_WITHOUT_CONTEXT")
    PROMPT_PATH_WITH_CONTEXT1: str = os.environ.get("PROMPT_PATH_WITH_CONTEXT1")
    PROMPT_PATH_WITH_CONTEXT2: str = os.environ.get("PROMPT_PATH_WITH_CONTEXT2")

