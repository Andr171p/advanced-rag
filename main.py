import asyncio

from src.services.chat import ChatService


question = "За какие достижения дают дополнительные баллы?"


async def main() -> None:
    chat_service = ChatService()
    answer = await chat_service.answer_on_question(question)
    print(answer)
    
    
asyncio.run(main())
