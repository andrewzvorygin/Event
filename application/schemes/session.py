from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel


class RefreshSession(BaseModel):
    user_id: int
    refresh_session: UUID = uuid4()
    access_token: str | None
    expires_in: int
    time_created: datetime

    class Config:
        orm_mode = True
