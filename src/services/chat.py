from src.rag.provider import get_rag_chain


class ChatService:
    def __init__(self) -> None:
        self._rag_chain = get_rag_chain()
    
    async def answer_on_question(self, question: str) -> str:
        answer = await self._rag_chain.ainvoke(question)
        return answer
    