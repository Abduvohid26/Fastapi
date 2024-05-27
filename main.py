from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
from product_routes import product_router
from fastapi_jwt_auth import AuthJWT
from schema import SettingsModel
from os import getenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
orgins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=orgins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(product_router)

@AuthJWT.load_config
def get_config():
    return SettingsModel()

@app.get('/')
async def home():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(getenv('PORT', 8000)))
