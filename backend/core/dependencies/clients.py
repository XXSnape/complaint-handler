import aiohttp
from fastapi import Request


def get_client_session(
    request: Request,
) -> aiohttp.ClientSession:
    """
    Получает сессию aiohttp из состояния приложения.
    """
    return request.app.state.client_session
