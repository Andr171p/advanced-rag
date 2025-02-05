import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR: Path = Path(__file__).resolve().parent.parent

ENV_PATH: Path = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


class EmbeddingsSettings(BaseSettings):
    model_name: str = "ai-forever/sbert_large_nlu_ru"
    model_kwargs: dict = {"device": "cpu"}
    encode_kwargs: dict = {'normalize_embeddings': False}


class ElasticSettings(BaseSettings):
    url: str = "http://localhost:9200"
    user: str = "elastic"
    password: str = "password"
    
    vector_index_name: str = "tyuiu_index"
    docs_index_name: str = "docs-tyuiu-index"
    
    
class StaticSettings(BaseSettings):
    prompt: Path = BASE_DIR / "static" / "prompt" / "Сотрудник приёмной комиссии.txt"


class GigaChatSettings(BaseSettings):
    auth_key: str = os.getenv("GIGACHAT_AUTH_KEY")
    scope: str = os.getenv("GIGACHAT_SCOPE")
    model_name: str = os.getenv("GIGACHAT_MODEL_NAME")


class Settings(BaseSettings):
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    elastic: ElasticSettings = ElasticSettings()
    static: StaticSettings = StaticSettings()
    gigachat: GigaChatSettings = GigaChatSettings()
    
    
settings = Settings()
