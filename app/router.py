from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas import UserCreate, UserResponse
from app.service import (
    create_user_service,
    free_users_service,
    get_users_service,
    lock_user_service,
)

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(session: AsyncSession = Depends(get_session)):
    """GET-запрос на получение всех существующих пользователей"""

    return await get_users_service(session)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    """POST-запрос на добавление пользователя"""

    return await create_user_service(session, user)

@router.post("/lock", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def lock_user(session: AsyncSession = Depends(get_session)):
    """POST-запрос на блокирование пользователя"""

    return await lock_user_service(session)

@router.delete("/lock", status_code=status.HTTP_200_OK)
async def free_users(session: AsyncSession = Depends(get_session)):
    """DELETE-запрос на снятие блокировки у всех пользователей"""
    
    return await free_users_service(session)