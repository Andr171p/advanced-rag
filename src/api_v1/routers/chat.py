from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from dishka.integrations.fastapi import FromDishka, DishkaRoute

from src.schemas import QuestionSchema, AnswerSchema
from src.services import ChatService


chat_router = APIRouter(
    prefix="/api/v1",
    tags=["Chat"],
    route_class=DishkaRoute
)


@chat_router.post(path="/chat/", response_model=AnswerSchema)
async def answer_on_question(
    question: QuestionSchema,
    chat_service: FromDishka[ChatService]
) -> JSONResponse:
    answer = await chat_service.answer_on_question(question.question)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"answer": answer}
    )
