from pydantic import BaseModel
from typing import Optional


class SigupModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = False

    class Config:
        json_schema_extra = {
            "example": {
                "username": "test",
                "email": "test@gmail.com",
                "password": "123",
                "is_staff": False,
                "is_active": False,
            }
        }
    
class LoginModel(BaseModel):
    username: str
    password: str


class SettingsModel(BaseModel):
    authjwt_secret_key: str = "a4555d491306130ada7f5036187736d331a30a8addb5df2bd3a559a3cc41b3f3"
    authjwt_access_token_expires: int = 300  # 5 minutes
    authjwt_refresh_token_expires: int = 604800  # 7 days
    