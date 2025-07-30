from typing import Callable
from fastapi import Request, Response
from ...core.exception import RequestException


__all__ = (
    'InternalUserAgentRestriction',
)


class InternalUserAgentRestriction:

    def __init__(self):
        import re
        self.UA_REGEX = re.compile(r"^DealerTower-[A-Za-z0-9_-]+/\d+\.\d+(?:\.\d+)*$")

    async def __call__(self, request: Request, call_next: Callable) -> Response:
        ua = request.headers.get('user-agent') or ''
        if not self.UA_REGEX.match(ua):
            raise RequestException(
                controller='dtpyfw.middlewares.user_agent.InternalUserAgentRestriction',
                message='Wrong credential.',
                status_code=403,
            )
