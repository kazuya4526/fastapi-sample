from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

# DB接続情報
USERNAME = config(key="USER_NAME", cast=str)
PASSWORD =  config(key="PASSWORD", cast=str)
HOST = config(key="HOST", cast=str)
PORT = config(key="PORT", cast=str)
DATABASE = config(key="DATABASE", cast=str)

# S3情報
AWS_ACCESS_KEY_ID = config(key="AWS_ACCESS_KEY_ID", cast=str)
AWS_SECRET_ACCESS_KEY = config(key="AWS_SECRET_ACCESS_KEY", cast=str)
REGION_NAME = config(key="REGION_NAME", cast=str)

# OAUTH設定
SECRET_KEY = config(key="SECRET_KEY", cast=str)
ALGORITHM = config(key="ALGORITHM", cast=str)
ACCESS_TOKEN_EXPIRE_MINUTES = config(key="ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)