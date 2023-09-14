from .data import DataRefresher
from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from .model import DashboardResponse

from contextlib import asynccontextmanager

class Application:
    def __init__(self) -> None:
        self.data_refresher = DataRefresher()
        self.app = FastAPI(
            title="Kostenbesparingsapp",
            version="0.1.0",
            lifespan=self.lifespan
        )

        self.router = APIRouter(tags=["Default API Routes"])
        self.router.add_api_route(
            path="/data",
            endpoint=self.get_data,
            methods=["GET"],
            summary="Root"
        )

        self.router.add_api_route(
            path="/favicon.ico",
            endpoint=self.favicon,
            methods=["GET"],
            include_in_schema=False
        )

        self.app.include_router(self.router)

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        await self.data_refresher.run()
        yield
        await self.data_refresher.stop()

    async def get_data(self) -> DashboardResponse:
        return self.data_refresher.get_data()
    
    async def favicon(self):
        return FileResponse("data/favicon.png")
