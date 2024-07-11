from fastapi import FastAPI

from src.auth.routers import users_auth_router

app = FastAPI(title="Shaare")

app.include_router(users_auth_router, prefix="/api")
