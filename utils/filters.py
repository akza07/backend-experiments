from typing import Literal

from pydantic import BaseModel, Field

class PageFilter(BaseModel):
    page:int = Field(1)
    size:int = Field(25)
    order_by: Literal["created_at","updated_at"] = "created_at"
    search:str = ""
