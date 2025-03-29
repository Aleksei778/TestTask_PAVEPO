from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy import desc
from typing import Optional

from .models import User, AudioFile
from schemas.user import UserCreate
from schemas.audiofile import AudioFileCreate

class DBManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserCreate):
        user = User(
            yandex_id=user.yandex_id,
            email=user.email,
            name=user.name,
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user
    
    async def get_user_by_id(self, id: int):
        query = select(User).where(User.id == id)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str):
        query = select(User).where(User.id == email)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()
    
    async def get_user_by_yandex_id(self, yandex_id: str):
        query = select(User).where(User.id == yandex_id)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def get_users(self, skip: int = 0, limit: int = 10):
        query = select(User).offset(skip).limit(limit)
        result = await self.session.execute(query)

        return result.scalars.all()
    
    async def delete_user(self, user_id: int):
        query = delete(User).where(User.id == user_id)
        result = await self.session.execute(query)
        await self.session.commit()
        
        return result.rowcount > 0
    
    async def update_user(self, user_id: int, user: UserUpdate):
        update_data = user.model_dump(exclude_unset=True)
        query = update(User).where(User.id == user_id).values(**update_data)
        await self.session.execute(query)
        await self.session.commit()

        return self.get_user_by_id(user_id=user_id)
    
    async def create_audiofile(self, file: AudioFileCreate):
        new_file = AudioFile(
            user_id=file.user_id,
            original_filename=file.original_filename,
            file_path=file.file_path,
            changed_filename=file.change_filename
        )

        self.session.add(new_file)
        await self.session.commit()
        await self.session.refresh(new_file)

        return new_file

    async def get_audiofile_by_id(self, file_id: int):
        query = select(AudioFile).where(AudioFile.id == file_id)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()
    
    async def get_user_audiofiles(self, user_id: int, skip: int = 0, limit: int = 10):
        query = select(AudioFile).where(AudioFile.user_id == user_id).offset(skip).limit(limit)
        result = await self.session.execute(query)

        return result.scalars.all()
    
    async def delete_audiofile(self, file_id: int):
        query = delete(AudioFile).where(AudioFile.id == file_id)
        result = await self.session.execute(query)
        await self.session.commit()
        
        return result.rowcount > 0
    
    async def update_user(self, file_id: int, file: AudioFileUpdate):
        update_data = file.model_dump(exclude_unset=True)
        query = update(AudioFile).where(AudioFile.id == AudioFile).values(**update_data)
        await self.session.execute(query)
        await self.session.commit()

        return self.get_audiofile_by_id(file_id=file_id)


