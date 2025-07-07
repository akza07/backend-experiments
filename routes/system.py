from fastapi import APIRouter 
from database import flush_everything
from schemas.response import GenericResponse

router = APIRouter()

@router.post("/clear", response_model=GenericResponse)
def clear_database():
    flush_everything()
    return GenericResponse(message="Database flushed, Please reboot the server")
