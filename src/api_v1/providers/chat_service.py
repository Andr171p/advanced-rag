from dishka import Provider, Scope, provide

from src.services import ChatService


class ChatServiceProvider(Provider):
    @provide(scope=Scope.APP)
    def get_chat_service(self) -> ChatService:
        return ChatService()
