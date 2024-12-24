from fastapi import FastAPI
from routes import UserRoute, WalletRoute, TokenRoute
from middlewares import AuthentictionMiddleware


#* APP
app = FastAPI()

#* Routers
app.include_router(UserRoute)
app.include_router(WalletRoute)
app.include_router(TokenRoute)



#* MIDDLEWARES
app.add_middleware(AuthentictionMiddleware)