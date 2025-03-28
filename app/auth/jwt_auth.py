from jose import jwt, JWTError
from datetime import timedelta, datetime
from fastapi import HTTPException

from config import (
    JWT_ACCESS_SECRET_FOR_AUTH, 
    JWT_ALGORITHM, 
    JWT_REFRESH_SECRET_FOR_AUTH
)

ACCESS_TOKEN_EXPIRES_MINUTES = 10
REFRESH_TOKEN_EXPIRES_DAYS = 7

async def create_access_token(self, data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({
        "exp": expire, 
        "type": "access"
    })
        
    try:
        encoded_jwt = jwt.encode(
            to_encode,
            JWT_ACCESS_SECRET_FOR_AUTH,
            algorithm=self.algorithm
        )
        return encoded_jwt
    except Exception as e:
        raise Exception(f"Error creating access token: {str(e)}")
    
async def create_refresh_token(self, data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRES_DAYS)
    to_encode.update({
        "exp": expire, 
        "type": "refresh"
    })
        
    try:
        encoded_jwt = jwt.encode(
            to_encode,
            JWT_REFRESH_SECRET_FOR_AUTH,
            algorithm=self.algorithm
        )
        return encoded_jwt
    except Exception as e:
        raise Exception(f"Error creating refresh token: {str(e)}")

async def verify_token(token: str, token_type: str = "access"):
    try:
        secret = (
                JWT_ACCESS_SECRET_FOR_AUTH
                if token_type == "access"
                else JWT_REFRESH_SECRET_FOR_AUTH
            )
        
        payload = jwt.decode(
                token,
                secret,
                algorithms=[JWT_ALGORITHM]
            )

        if payload.get("type") != token_type:
                print("not type")
                raise Exception("Invalid token type")
        
        exp = payload.get("exp")
        if not exp or datetime.fromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=401, 
                detail="Token has expired"
            )
        
    except JWTError as jwt_e:
        raise HTTPException(
            status_code=401, 
            detail=str(jwt_e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=401, 
            detail=str(e)
        )