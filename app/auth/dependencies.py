from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db_conn
from db.models import User
from .jwt_auth import verify_token

security = HTTPBearer()

async def get_current_user(
        credentials: HTTPBearer = Depends(security),
        db: AsyncSession = Depends(get_db_conn)
):
    db_manager = DBManager(session=db)

    try:
        if not credentials or not credentials.credentials:
            raise HTTPException(
                status_code=401,
                detail="No auth data"
            )
        
        payload = await verify_token(token=credentials.credentials)

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="No user data"
            )
        
    except:
        raise HTTPException(
                status_code=401,
                detail="Could not validate creds"
            )
    
    user = await db_manager.get_user_from_db(user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="No such user"
        )
    
    return user