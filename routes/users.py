from fastapi import APIRouter, Depends
from dependencies import SessionDep, security
from utils.helpers import get_current_user
from schemas.user import UserPublicResponse

router = APIRouter()


@router.get("/me", response_model=UserPublicResponse)
def get_user(
    session: SessionDep,
    token=Depends(security.oauth2_scheme),
):
    user = get_current_user(session, token)

    return {
        "message": "User Profile fetched",
        "data": user,
    }
