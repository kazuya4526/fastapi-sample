from datetime import datetime
from pydantic import BaseModel
from typing import Union

class CommonResponse(BaseModel):
    message: str

class UserInfo(BaseModel):
    user_id: int
    user_name: str
    password: str

class FileInfo(BaseModel):
    file_name: str
    owner: str
    content_length: int
    last_modified: datetime
    