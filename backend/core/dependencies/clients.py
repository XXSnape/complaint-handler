import aiohttp
from fastapi import Request


def get_client_session(
    request: Request,
) -> aiohttp.ClientSession:
    return request.app.state.client_session
