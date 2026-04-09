from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import User
from app.schemas import UserCreate


async def get_users_service(session: AsyncSession):
    """Получение всех существующих пользователей"""

    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


async def create_user_service(session: AsyncSession, user: UserCreate):
    """Создание пользователя"""

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    db_user = User(**user.model_dump())  
    db_user.password = hashed_password
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def lock_user_service(session: AsyncSession):
    """Получить пользователя для нужд ботофермы"""

    now = datetime.utcnow()
    new_locktime = now + timedelta(minutes=settings.LOCK_TIMEOUT_MINUTES)

    query = select(User).where(
            or_(
                User.locktime.is_(None),
                User.locktime <= now,
            ))
    
    result = await session.execute(query)
    db_item = result.scalars().first()

    if not db_item:
        raise HTTPException(status_code=404, detail="No free users available")
    
    db_item.locktime = new_locktime

    await session.commit()
    await session.refresh(db_item)
    return db_item


async def free_users_service(session: AsyncSession):
    """Снятие блокировки у всех пользователей"""
    
    query = update(User).values(locktime=None)
    await session.execute(query)    
    await session.commit()