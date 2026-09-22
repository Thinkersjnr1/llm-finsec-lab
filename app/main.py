from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .auth import router as auth_router
from .accounts import router as accounts_router
from .transfers import router as transfers_router
from .ai import router as ai_router

app = FastAPI(
    title="LLM-FinSec Lab",
    description="Deliberately vulnerable fintech application for authorized security testing",
    version="1.0.0"
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    for error in exc.errors():
        sanitized_error = {
            "loc": error.get("loc"),
            "msg": error.get("msg"),
            "type": error.get("type")
        }

        errors.append(sanitized_error)

    return JSONResponse(
        status_code=422,
        content={"detail": errors}
    )


app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(transfers_router)
app.include_router(ai_router)

@app.get("/")
def root():
    return {
        "application": "LLM-FinSec Lab",
        "status": "running",
        "environment": "local-lab"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
