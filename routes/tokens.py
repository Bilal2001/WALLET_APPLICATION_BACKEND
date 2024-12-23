from fastapi import APIRouter
from fastapi.responses import JSONResponse
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "VERY_SECRET_KEY"
ALGORITHM = "HS256"

app = APIRouter(prefix="/token", tags=["token"])

@app.get("/new-token")
async def create_jwt_token():
    payload = {}
    payload["exp"] = datetime.now() + timedelta(hours=1)  # Token expires in 1 hour
    return JSONResponse(status_code=200, content={"token" : jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)})