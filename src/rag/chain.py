from typing import TYPE_CHECKING, Callable, List

from langchain_core.runnables import RunnablePassthrough

if TYPE_CHECKING:
    from langchain_core.documents import Document
    from langchain_core.retrievers import BaseRetriever
    from langchain_core.prompts.chat import BaseChatPromptTemplate
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.output_parsers.transform import BaseTransformOutputParser
    from langchain_core.runnables.base import Runnable


class RAGChainFactory:
    def __init__(
        self,
        retriever: "BaseRetriever",
        prompt: "BaseChatPromptTemplate",
        model: "BaseChatModel",
        parser: "BaseTransformOutputParser",
    ) -> None:
        self._retriever = retriever
        self._prompt = prompt
        self._model = model
        self._parser = parser
        
    def create_rag_chain(
        self, 
        parse_document_context_func: Callable[[List["Document"]], str]
    ) -> "Runnable":
        chain = (
            {
                "context": self._retriever | parse_document_context_func,
                "question": RunnablePassthrough()
            } |
            self._prompt |
            self._model |
            self._parser
        )
        return chain
