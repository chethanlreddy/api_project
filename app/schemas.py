import email
from email.mime import base
from inspect import classify_class_attrs
from lib2to3.pgen2.token import BACKQUOTE
from operator import le
from os import access
from turtle import pos
from click import option
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class postBase(BaseModel):
    title: str
    content: str
    published: bool = True


class postCreate(postBase):
    pass


class userOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class post(postBase):
    id: int
    created_at: datetime
    owner_id: int
    owner : userOut

    class Config:
        orm_mode = True


class postOut(BaseModel):
    post : post
    votes : int

    class Config:
        orm_mode = True

class userCreate(BaseModel):
    email: EmailStr
    password: str


class userLogin(BaseModel):
    email: EmailStr
    password: str


class token(BaseModel):
    access_token: str
    token_type: str


class tokenData(BaseModel):
    id: Optional[str] = None


class vote(BaseModel):
    post_id : int
    dir : conint(le=1)