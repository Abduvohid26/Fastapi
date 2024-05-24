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
    username_or_email: str
    password: str


class SettingsModel(BaseModel):
    authjwt_secret_key: str = "a4555d491306130ada7f5036187736d331a30a8addb5df2bd3a559a3cc41b3f3"
    authjwt_access_token_expires: int = 60 * 60  # 60 minutes
    authjwt_refresh_token_expires: int = 604800  # 7 days
    

class OrderModel(BaseModel):
    id: Optional[int] = None
    qty: int
    order_status: Optional[str] = 'PENDING'
    user_id: Optional[int] = None
    product_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "qty": 2,
            }
        }

class OrderStatus(BaseModel):
    order_status: Optional[str] = 'PENDING'

    class Config:
        json_schema_extra = {
            "example": {
                "order_status": "PENDING",
            }
        }



class ProductModel(BaseModel):
    id: Optional[int] = None
    name: str  
    price: int

    class Config:
        json_schema_extra = {
            "example": {
                "name": "test",
                "price": 20000,
            }
        }