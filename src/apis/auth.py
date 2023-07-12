import datetime
from fastapi import APIRouter
from prisma.models import User
from pydantic import BaseModel
from typing import Optional, Union
from src.models.scalar import Gender, Role
from src.prisma import prisma
from src.utils.auth import (
    encryptPassword,
    signJWT,
    validatePassword,
)

router = APIRouter()


class SignIn(BaseModel):
    email: str
    password: str


class SignInOut(BaseModel):
    token: str
    user: User


class SignUp(BaseModel):
    email: str
    password: str
    role: Role
    name: Optional[str] = None
    nickname: Optional[str] = None
    birthday: Optional[datetime.date] = None
    gender: Optional[Gender] = None
    phone: Optional[str] = None


@router.post("/auth/sign-in", tags=["auth"])
async def sign_in(signIn: SignIn):
    user = await prisma.user.find_first(
        where={
            "email": signIn.email,
        }
    )

    if user and user.password:
        validated = validatePassword(signIn.password, user.password)
        del user.password

        if validated:
            token = signJWT(user.id)
            return SignInOut(token=token, user=user)

    return None


@router.post("/auth/sign-up", tags=["auth"])
async def sign_up(user: SignUp):
    password = encryptPassword(user.password)
    created = await prisma.user.create(
        {
            "email": user.email,
            "password": password,
            "name": user.name,
            "nickname": user.nickname,
            "birthDay": user.birthday,
            "gender": user.gender,
            "phone": user.phone,
        }  # type: ignore
    )

    return created


@router.get("/auth/", tags=["auth"])
async def auth():
    users = await prisma.user.find_many()

    for user in users:
        del user.password

    return users
