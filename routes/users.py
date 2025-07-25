from fastapi import APIRouter, Depends
from dependencies import SessionDep, security
from services.auth_service import get_current_user_by_token
from schemas.user import UserPublicResponse

router = APIRouter()


@router.get("/me", response_model=UserPublicResponse)
def get_user(
    session: SessionDep,
    token=Depends(security.oauth2_scheme),
):
    user = get_current_user_by_token(session, token)

    return {
        "message": "User Profile Retrieved",
        "data": user,
    }
