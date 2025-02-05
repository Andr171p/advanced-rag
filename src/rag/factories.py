from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.embeddings import Embeddings
    from langchain_core.vectorstores import VectorStore
    from langchain_core.retrievers import BaseRetriever

from langchain.embeddings import HuggingFaceEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from elasticsearch import Elasticsearch
from langchain_community.retrievers import ElasticSearchBM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_gigachat.chat_models import GigaChat
from langchain_core.output_parsers.string import StrOutputParser

from src.misc.file_loaders import load_txt
from src.config import settings


def _get_embeddings(
    model_name: str = settings.embeddings.model_name,
    model_kwargs: dict = settings.embeddings.model_kwargs,
    encode_kwargs: dict = settings.embeddings.encode_kwargs
) -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    
    
def _get_elastic_client(
    url: str = settings.elastic.url,
    user: str = settings.elastic.user,
    password: str = settings.elastic.password
) -> Elasticsearch:
    return Elasticsearch(
        hosts=url, 
        basic_auth=(user, password)
    )


def _get_elastic_vector_store(
    url: str = settings.elastic.url,
    user: str = settings.elastic.user,
    password: str = settings.elastic.password,
    index_name: str = settings.elastic.vector_index_name,
    embeddings: "Embeddings" = _get_embeddings(),
) -> ElasticsearchStore:
    return ElasticsearchStore(
        es_url=url,
        index_name=index_name,
        embedding=embeddings,
        es_user=user,
        es_password=password
    )


def _get_vector_store_retriever(
    vector_store: "VectorStore" = _get_elastic_vector_store(),
    search_kwargs: dict = {"k": 2}
) -> "BaseRetriever":
    return vector_store.as_retriever(search_kwargs=search_kwargs)


def _get_elastic_bm25_retriever(
    client: Elasticsearch = _get_elastic_client(),
    index_name: str = settings.elastic.docs_index_name,
    search_kwargs: dict = {"k": 2}
) -> "BaseRetriever":
    return ElasticSearchBM25Retriever(
        client=client,
        index_name=index_name,
        search_kwargs=search_kwargs
    )


def get_ensemble_retriever() -> "BaseRetriever":
    vector_store_retriever = _get_vector_store_retriever()
    bm25_retriever = _get_elastic_bm25_retriever()
    return EnsembleRetriever(
        retrievers=[vector_store_retriever, bm25_retriever],
        weights=[0.6, 0.4]
    )
    
    
def get_chat_prompt(
    template_path: str = settings.static.prompt
) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_template(load_txt(template_path))


def get_gigachat_model(
    auth_key: str = settings.gigachat.auth_key,
    scope: str = settings.gigachat.scope,
    model_name: str = settings.gigachat.model_name,
) -> GigaChat:
    return GigaChat(
        credentials=auth_key,
        scope=scope,
        model=model_name,
        verify_ssl_certs=False,
        profanity_check=False
    )


def get_output_parser() -> StrOutputParser:
    return StrOutputParser()
