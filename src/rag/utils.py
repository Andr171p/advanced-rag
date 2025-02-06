from langchain.embeddings import HuggingFaceEmbeddings
from langchain_elasticsearch import ElasticsearchStore
from elasticsearch import Elasticsearch
from langchain_community.retrievers import ElasticSearchBM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_gigachat.chat_models import GigaChat
from langchain_core.output_parsers.string import StrOutputParser

from src.rag.helpers import get_gigachat_auth_key
from src.misc.file_loaders import load_txt
from src.config import settings


embeddings = HuggingFaceEmbeddings(
    model_name=settings.embeddings.model_name,
    model_kwargs=settings.embeddings.model_kwargs,
    encode_kwargs=settings.embeddings.encode_kwargs
)


elastic_client = Elasticsearch(
    hosts=settings.elastic.url,
    basic_auth=(settings.elastic.user, settings.elastic.password)
)


vector_store = ElasticsearchStore(
    es_url=settings.elastic.url,
    index_name=settings.elastic.vector_index_name,
    embedding=embeddings,
    es_user=settings.elastic.user,
    es_password=settings.elastic.password
)


vector_store_retriever = vector_store.as_retriever(search_kwargs={"k": 2})


bm25_retriever = ElasticSearchBM25Retriever(
    client=elastic_client,
    index_name=settings.elastic.docs_index_name,
    search_kwargs={"k": 2}
)


ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_store_retriever, bm25_retriever],
    weights=[0.6, 0.4]
)


prompt = ChatPromptTemplate.from_template(load_txt(settings.static.prompt))


model = GigaChat(
    credentials=get_gigachat_auth_key(
        client_id=settings.gigachat.client_id, 
        client_secret=settings.gigachat.client_secret
    ),
    scope=settings.gigachat.scope,
    model=settings.gigachat.model_name,
    verify_ssl_certs=False,
    profanity_check=False
)


parser = StrOutputParser()
