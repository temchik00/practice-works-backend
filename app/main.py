import json

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth_router import router

from app.exceptions import GeneralException
from app.crud.exceptions import CrudError, ConstraintError, AlreadyExistsError
from app.services.exceptions import (ServiceError, UnauthorizedError,
                                     WrongCredentialsError)


app = FastAPI(
    title="practice-works"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


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
