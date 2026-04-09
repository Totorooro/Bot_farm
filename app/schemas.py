import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import DomainType, EnvType


class UserCreate(BaseModel):
    """Pydantic схема для валидации входных данных"""

    login: str
    password: str
    project_id: uuid.UUID
    env: EnvType
    domain: DomainType

class UserResponse(BaseModel):
    """Pydantic схема для валидации выходных данных"""

    id: uuid.UUID
    created_at: datetime
    login: str
    project_id: uuid.UUID
    env: EnvType
    domain: DomainType
    locktime: datetime | None

    model_config = ConfigDict(from_attributes=True)