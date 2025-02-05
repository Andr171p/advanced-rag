from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.runnables.base import Runnable

from src.rag.chain_factory import RAGChainFactory
from src.rag.helpers import parse_documents_content
from src.rag.factories import (
    get_ensemble_retriever,
    get_chat_prompt,
    get_gigachat_model,
    get_output_parser
)


def get_rag_chain() -> "Runnable":
    rag_chain_factory = RAGChainFactory(
        retriever=get_ensemble_retriever(),
        prompt=get_chat_prompt(),
        model=get_gigachat_model(),
        parser=get_output_parser()
    )
    rag_chain = rag_chain_factory.create_rag_chain(parse_documents_content)
    return rag_chain
