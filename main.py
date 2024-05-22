from fastapi import FastAPI
from auth_routes import auth_router
from fastapi_jwt_auth import AuthJWT
from schema import SettingsModel
app = FastAPI()

app.include_router(auth_router)

@AuthJWT.load_config
def get_config():
    return SettingsModel()

@app.get('/')
async def home():
    return {"message": "Hello World"}

