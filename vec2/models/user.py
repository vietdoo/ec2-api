from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
# from vec2.postgres import Base
from vec2.kit.db.models.base import Model


class User(Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
