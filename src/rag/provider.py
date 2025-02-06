from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_core.runnables.base import Runnable

from src.rag.chain import RAGChainFactory
from src.rag.helpers import parse_documents_content
from src.rag.utils import (
    ensemble_retriever,
    prompt,
    model,
    parser
)


def get_rag_chain() -> "Runnable":
    rag_chain_factory = RAGChainFactory(
        retriever=ensemble_retriever,
        prompt=prompt,
        model=model,
        parser=parser
    )
    rag_chain = rag_chain_factory.create_rag_chain(parse_documents_content)
    return rag_chain
