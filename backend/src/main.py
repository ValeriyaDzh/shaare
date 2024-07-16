from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.auth.routers import users_auth_router
from src.files_upload.routers import files_upload_router

app = FastAPI(title="Shaare")

app.include_router(users_auth_router, prefix="/api")
app.include_router(files_upload_router, prefix="/api")

app.mount(
    "/uploaded_files",
    StaticFiles(directory="src/uploaded_files"),
    name="uploaded_files",
)
