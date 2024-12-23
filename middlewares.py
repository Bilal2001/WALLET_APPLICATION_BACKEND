from collections import defaultdict
import time
from typing import Dict
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import os
from dotenv import load_dotenv
import jwt

#* Lead ENV File
load_dotenv()
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
RATELIMIT_PER_MINUTE = os.environ["RATELIMIT_PER_MINUTE"]

class AuthentictionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/docs", "/openapi.json", "/token/new-token"]:
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Authorization header missing or invalid"})
            
        token = auth_header.split(" ")[1]  # Extract token part
        try:
            # Decode and validate the JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload  # Store the decoded payload for use in endpoints
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token has expired"})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})
        
        # Proceed to the next request handler
        return await call_next(request)
    
class RateLimitterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_count: Dict[str, int] = defaultdict(int)
        self.rate_limit_time: Dict[str, float] = defaultdict(float)
        
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/docs", "/openapi.json", "/token/new-token"]:
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]  # Extract token part
        current_time = time.time()
        
        print(self.rate_limit_count, self.rate_limit_time)
        
        if token not in self.rate_limit_count:
            self.rate_limit_count[token] = 0
            self.rate_limit_time[token] = current_time
        
        elif self.rate_limit_count[token] == 10:
            if (current_time - self.rate_limit_time[token]) >= 60:
                del self.rate_limit_time[token]
                del self.rate_limit_count[token]
            return JSONResponse(status_code=429, content="Rate limit exceeded")

        self.rate_limit_time[token] = current_time
        self.rate_limit_count[token] += 1

        return await call_next(request)