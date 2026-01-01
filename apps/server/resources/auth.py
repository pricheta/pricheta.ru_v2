from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from apps.server.auth_service.auth_service import AuthService
from apps.server.deps import get_auth_service
from apps.server.models import AuthResponse

router = APIRouter()
TAGS = ["auth"]


@router.post("/")
def auth(
    request: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    user = auth_service.users_db.get_user(request.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Authorisation failed",
        )

    verified = auth_service.verify_password(
        plain_password=request.password,
        hashed_password=user.password,
    )
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authorisation failed",
        )

    access_token = auth_service.create_access_token(user)
    return AuthResponse(access_token=access_token)
