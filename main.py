from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from routes import UserRoute, WalletRoute, TokenRoute
from database import init_db
from middlewares import AuthentictionMiddleware, RateLimitterMiddleware



#* INIT DB
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

#* APP
app = FastAPI(lifespan=lifespan)

#* Routers
app.include_router(UserRoute)
app.include_router(WalletRoute)
app.include_router(TokenRoute)



#* MIDDLEWARES
app.add_middleware(AuthentictionMiddleware)
app.add_middleware(RateLimitterMiddleware)