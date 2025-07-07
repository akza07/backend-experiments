from fastapi import FastAPI
from config import get_config
from database import create_db_and_tables
from routes import users, auth, system
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title=get_config().app_name,
    description="Contains sample code and experiments with different libraries",
    version="1.0.0",
)


@app.get("/health", tags=["Health"])
def check_health():
    app_name: str = get_config().app_name
    return f"{app_name} is up and running."


# Auth
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)
# Users
app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

app.include_router(
    system.router,
    prefix="/system",
    tags=["System"]
)
