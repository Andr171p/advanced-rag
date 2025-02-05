from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from dishka.integrations.fastapi import FromDishka, DishkaRoute

from src.schemas import QuestionSchema
from src.services import ChatService


chat_router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
    route_class=DishkaRoute
)


@chat_router.post(path="/answer/", response_model=...)
async def answer_on_question(
    question: QuestionSchema,
    chat_service: FromDishka[ChatService]
) -> JSONResponse:
    answer = await chat_service.answer_on_question(question.text)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"answer": answer}
    )
