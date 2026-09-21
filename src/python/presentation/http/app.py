from fastapi import FastAPI

from .routers.loan import router as loan_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="DDD Learning Challenges",
        version="0.1.0",
    )
    app.include_router(loan_router)
    return app


app = create_app()
