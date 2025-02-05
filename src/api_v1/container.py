from dishka import make_async_container

from src.api_v1.providers import ChatServiceProvider


container = make_async_container(
    ChatServiceProvider()
)
