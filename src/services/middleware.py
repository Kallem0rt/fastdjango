from starlette.middleware.base import BaseHTTPMiddleware


class PrefixMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Проверяем, что запрос направлен в Django-приложение
        if request.url.path.startswith("/admin"):
            # Добавляем префикс к пути запроса
            request.scope['path'] = "/django" + request.scope['path']
        if request.url.path.startswith("/static"):
            pass
        return await call_next(request)
