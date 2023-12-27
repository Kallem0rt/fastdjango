import os
from pathlib import Path

import uvicorn
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles

from src.services.include_routers import IncludeRouter
from src.services.logger import get_logger
from src.services.middleware import PrefixMiddleware

BASE_DIR = Path(__file__).resolve().parent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{BASE_DIR.name}.settings")

# Загрузка переменных окружения из файла .env
load_dotenv()

fast_api = IncludeRouter()
app = fast_api()
fast_api.inspect_routes(fast_api.app)
fast_api.app.add_middleware(PrefixMiddleware)

# Подключение Django ASGI приложения

django_asgi_app = get_asgi_application()
app.mount("/django", django_asgi_app)
#
app.mount("/static", StaticFiles(directory=BASE_DIR / BASE_DIR.name / "static"), name="static")

# Подключаем шаблоны Jinja2

logger = get_logger()

logger.info(f"Include router")

if __name__ == "__main__":
    uvicorn.run(
        fast_api.app,
        log_config=None,
        host="0.0.0.0",
        port=8080,
        log_level="info",
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
