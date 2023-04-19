from .db_session import SqlAlchemyBase
from sqlalchemy import (
        Column, 
        Integer, 
        String, 
    )


class User(SqlAlchemyBase):
    __tablename__ = 'bot_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=True)
    api_token = Column(String, nullable=True)
