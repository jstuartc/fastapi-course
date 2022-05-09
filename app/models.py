from typing import Text
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import relationship
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = 'True', nullable = False)
    created_at = Column(TIMESTAMP(timezone= True), nullable = False, server_default = func.now())
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable= False)

    owner = relationship("User") 

class User(Base):
    __tablename__ = "users"

    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    id = Column(Integer, primary_key = True, nullable = False)
    created_at = Column(TIMESTAMP(timezone= True), nullable = False, server_default = func.now())

class Votes(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), primary_key = True)
    post_id = Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"), primary_key = True)