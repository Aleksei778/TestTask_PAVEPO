from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, relationship

from ..utils import moscow_time

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    yandex_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=moscow_time)
    updated_at = Column(DateTime(timezone=True), default=moscow_time)

    audio_files = relationship('AudioFile', back_populates='user')

class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    changed_filename = Column(String, nullable=True)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), default=moscow_time)

    user = relationship('User', back_populates='audio_files')