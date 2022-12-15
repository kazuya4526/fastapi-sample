from typing import List
from sqlalchemy.sql import func
from datetime import datetime

from src.config.db_config import get_session
from src.model.entities import DownloadUser

def selectByName(user_name: str):
    
    db = next(get_session())
    
    user: DownloadUser = db.query(DownloadUser).where(
        DownloadUser.user_id == user_name
    ).first()

    return user

def register(user_name: str, hashed_password: str, role_code: str):
    
    db = next(get_session())
    
    user = DownloadUser(
        user_id = user_name,
        password = hashed_password,
        role_code = role_code
    )
    
    db.add(user)
    
    db.commit()