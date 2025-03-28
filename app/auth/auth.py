from fastapi import HTTPException, APIRouter, Request, Depends
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from db.database import get_db_conn
from db.dbmanager import DBManager
from .jwt_auth import create_access_token, create_refresh_token, verify_token
from config import (
    YANDEX_CLIENT_ID,
    YANDEX_SECRET,
    YANDEX_REDIRECT_URI
)

auth_router = APIRouter(prefix="/auth")

oauth = OAuth()
oauth.register(
    name='yandex',
    client_id=YANDEX_CLIENT_ID,
    client_secret=YANDEX_SECRET,
    authorize_url='https://oauth.yandex.ru/authorize',
    access_token='https://oauth.yandex.ru/token',
    api_base_url='https://login.yandex.ru/',
    client_kwargs={'scope': 'login:email login::info'}
)

@auth_router.get('/login')
async def yandex_login(request: Request):
    yandex = oauth.create_client('yandex')
    redirect_uri = YANDEX_REDIRECT_URI
    return yandex.authorize_redirect(request, redirect_uri)

@auth_router.get('/callback')
async def yandex_callback(request: Request, db: AsyncSession = Depends(get_db_conn)):
    db_manager = DBManager(session=db)
    yandex = oauth.create_client('yandex')
    token_data = await yandex.authorize_access_token(request)

    if not token_data:
        raise HTTPException(
            status_code=401,
            detail="No token data"
        )
    
    user_response = await yandex.get(
        'info', 
        token=token_data
    )

    user_info = user_response.json()

    if not user_info or 'error' in user_info:
        raise HTTPException(
            status_code=401,
            detail="No user info"
        )
    
    user = await db_manager.get_user_by_id(
        yandex_id = user_info['id']
    )

    if not user:
        user = await db_manager.create_user(
            yandex_id=user_info['id'], 
            email=user_info.get('default_email'), 
            name=user_info.get('display_name')
        )

    data = {
        "sub": str(user.id)
    }
    access_token = await create_access_token(
        data=data
    )
    refresh_token = await create_refresh_token(
        data=data
    )

    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    }

auth_router.post("/refresh_token")
async def refresh_token(request: Request, db: AsyncSession = Depends(get_db_conn)):
    refresh_token = request.refresh_token
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token not found")
    
    try:
        token_type, token = refresh_token.split()
        if token_type.lower() != 'bearer':
            raise HTTPException(
                status_code=401, 
                detail="The wrong type of token"
            )
    except ValueError:
        raise HTTPException(
            status_code=401, 
            detail="The wrong format of token"
        )

    try:
        db_manager = DBManager(session=db)

        # Проверяем refresh токен
        payload = await verify_token(refresh_token, "refresh")
        user_data = payload.get("sub")
        
        if not user_data:
            raise HTTPException(
                status_code=401,
                detail="No user data"
            )

        user = await db_manager.get_user_by_id(user_data['id'])
            
        if not user:
             raise HTTPException(
                status_code=404,
                detail="User not found"
            )
            
        new_data = {
            "sub": str(user.id)
        }
        new_access_token = await create_access_token(new_data)
        new_refresh_token = await create_refresh_token(new_data)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    
    except HTTPException:
        raise HTTPException(
            status_code=401, 
            detail="Invalid refresh token."
        )