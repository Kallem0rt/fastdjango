import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.services.logger import get_logger

logger = get_logger()

BASE_DIR = Path(__file__).resolve().parent


class IncludeRouter:
    def __init__(self):
        self.app = FastAPI()

    def import_routers_from_module(self, module_name):

        module = __import__(f"{BASE_DIR.parent.name}.{module_name}", fromlist=['dummy'])
        if isinstance(module.router, APIRouter):
            self.app.include_router(module.router)

    @staticmethod
    def inspect_routes(router: APIRouter, prefix: str = ""):
        for route in router.routes:
            full_path = prefix + route.path
            logger.info(f"Route: {full_path}, Methods: {route.methods}")

    def __call__(self):
        # Найдите все файлы в пакете
        package_path = os.path.join(BASE_DIR.parent, 'routers')
        files = [f[:-3] for f in os.listdir(package_path) if f.endswith(".py") and not f.startswith("__")]
        # Импортируйте и добавьте роутеры
        for file in files:
            module_name = f"routers.{file}"
            logger.info(f"Importing router {file}")
            self.import_routers_from_module(module_name)
        return self.app
