from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from dishka.integrations.fastapi import FromDishka, DishkaRoute

from src.schemas import ChatQuestion, ChatAnswer
from src.services import ChatService


chat_router = APIRouter(
    prefix="/api/v1",
    tags=["Chat"],
    route_class=DishkaRoute
)


@chat_router.post(path="/chat/", response_model=ChatAnswer)
async def answer_on_question(
    question: ChatQuestion,
    chat_service: FromDishka[ChatService]
) -> JSONResponse:
    answer = await chat_service.answer_on_question(question.question)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"answer": answer}
    )
