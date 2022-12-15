from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from typing import List, Union
from datetime import datetime, timedelta
import src.dao.user_dao as user_dao
import src.config.config as config
#JWT設定
SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

#パスワードのハッシュ化設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#OAuth2.0をパスワードフローで使用する設定
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "general": "download",
        "admin": "manage user",
    }
)

class Token(BaseModel):
    """アクセストークン情報"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """復号後のJWTのペイロード"""
    user_name: Union[str, None] = None
    scopes: List[str] = []

def verify_password(plain_password, hashed_password):
    """パスワード検証。平文パスワードとハッシュ化パスワード比較。

    Args:
        plain_password: パスワード（平文）
        hashed_password: パスワード（ハッシュ済） 

    Returns:
        True:パスワードが一致している
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """パスワードをハッシュ化する。

    Args:
        password: パスワード（平文）

    Returns:
        パスワード（ハッシュ化）
    """
    return pwd_context.hash(password)

def get_user(user_name: str):
    """DBからユーザ情報を取得する。

    Args:
        username: ユーザ名。ユーザ検索のキー。

    Returns:
        対象ユーザのレコード。
    """   
    user = user_dao.selectByName(user_name)
    if user != None:
        return user
    return None

def authenticate_user(user_name: str, password: str):
    """ユーザのパスワード認証を行い、ユーザ情報を返却する。

    Args:
        username: ユーザ名
        password: パスワード

    Returns:
        ユーザ情報
    """
    user = get_user(user_name)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict):
    """アクセストークンを生成する。

    Args:
        data (dict): JWTのペイロード部

    Returns:
        アクセストークン
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    """アクセストークンを検証し、ログインユーザ情報を取得する。

    Args:
        security_scoprs: スコープ
        token: アクセストークン

    Returns:
        アクセストークンに紐づくログインユーザ情報
    """
    
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="再度ログインしてください。",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # JWTからユーザ名とスコープ取得
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, user_name=user_id)
    except JWTError:
        raise credentials_exception
    except ValidationError as e:
        raise credentials_exception
    
    # ユーザ存在確認
    user = get_user(user_name=token_data.user_name)
    if user is None:
        raise credentials_exception
    
    # スコープ所持確認
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user