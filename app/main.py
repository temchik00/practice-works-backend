import json

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router

from app.exceptions import GeneralException
from app.crud.exceptions import CrudError, ConstraintError, AlreadyExistsError
from app.dependencies.settings import get_fastapi_settings
from app.services.exceptions import (ServiceError, UnauthorizedError,
                                     WrongCredentialsError, NotFoundError)


settings = get_fastapi_settings()


app = FastAPI(
    title="practice-works",
    docs_url=f'{settings.base_path}/docs',
    redoc_url=f'{settings.base_path}/redoc',
    openapi_url=f'{settings.base_path}/openapi.json'
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=settings.base_path)
app.include_router(user_router, prefix=settings.base_path)


@app.exception_handler(AlreadyExistsError)
def already_exists_exception_handler(request, exc: AlreadyExistsError):
    return Response(
        json.dumps({"detail": exc.public_message}),
        status_code=status.HTTP_409_CONFLICT
    )


@app.exception_handler(ConstraintError)
def constraint_exception_handler(request, exc: ConstraintError):
    return Response(
        json.dumps({"detail": exc.public_message}),
        status_code=status.HTTP_400_BAD_REQUEST
    )


@app.exception_handler(CrudError)
def crud_exception_handler(request, exc: CrudError):
    return Response(
        json.dumps({"detail": exc.public_message}),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@app.exception_handler(NotFoundError)
def not_found_exception_handler(request, exc: NotFoundError):
    return Response(
        json.dumps({"detail": exc.public_message}),
        status_code=status.HTTP_404_NOT_FOUND
    )


@app.exception_handler(WrongCredentialsError)
def credentials_exception_handler(request, exc: WrongCredentialsError):
    return Response(
        json.dumps({"detail": exc.public_message}),
        status_code=status.HTTP_400_BAD_REQUEST
    )


@app.exception_handler(UnauthorizedError)
def unauthorized_exception_handler(request, exc: UnauthorizedError):
    return Response(
        json.dumps({"detail": exc.public_message}),
        status_code=status.HTTP_401_UNAUTHORIZED
    )


@app.exception_handler(ServiceError)
def service_exception_handler(request, exc: ServiceError):
    return Response(
        json.dumps({"detail": exc.public_message}),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@app.exception_handler(GeneralException)
def general_exception_handler(request, exc: GeneralException):
    return Response(
        json.dumps({"detail": exc.public_message}),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
