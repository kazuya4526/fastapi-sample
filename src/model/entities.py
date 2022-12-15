from src.config.db_config import Base
from sqlalchemy.schema import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP, CHAR, INTEGER, VARCHAR, DATE

class DownloadUser(Base):
    __tablename__ = "download_user"
    user_id = Column(VARCHAR, primary_key=True)
    password = Column(VARCHAR)
    role_code = Column(CHAR)