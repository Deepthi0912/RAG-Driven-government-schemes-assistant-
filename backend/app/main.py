from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.categories import router as category_router
from app.api.schemes import router as scheme_router
from app.api.documents import router as document_router
from app.api.qa import router as qa_router
from app.api.history import router as history_router
from app.api.feedback import router as feedback_router
from app.api.saved_schemes import router as saved_schemes_router


app = FastAPI(
    title="SchemeWise API",
    description="Government Scheme Discovery Platform",
    version="1.0.0"
)


# Existing API routes
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(scheme_router)
app.include_router(document_router)
app.include_router(history_router)
app.include_router(qa_router)
app.include_router(feedback_router)

# Saved schemes API
app.include_router(saved_schemes_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to SchemeWise API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }