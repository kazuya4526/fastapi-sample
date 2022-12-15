from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter

import src.config.auth_config as authconfig
import src.dao.user_dao as userdao
from src.model.response_models import CommonResponse


#router登録
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

#認証EP
@router.post("/token", response_model=authconfig.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """認証EP

    Args:
        form_data (OAuth2PasswordRequestForm, optional): ユーザ情報（ユーザ名, パスワード）

    Raises:
        HTTPException: 認証エラー

    Returns:
        _type_: アクセストークン
    """
    user = authconfig.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザ名またはパスワードが誤っています。",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.role_code == "0":
        scope = ["general"]
    elif user.role_code =="1":
        scope = ["admin"]
    else:
        scope = ""
        
    access_token = authconfig.create_access_token(
        data={
            "sub": user.user_id,
            "scopes": scope
        }
    )
    return {"access_token": access_token, "token_type": "bearer"}

#ユーザ新規登録EP
@router.post("/register", response_model=CommonResponse)
async def signup(form_data: OAuth2PasswordRequestForm = Depends()):
    user = userdao.selectByName(form_data.username)
    if user != None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザは既に登録されています。",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    hashed_password = authconfig.get_password_hash(form_data.password)
    userdao.register(form_data.username, hashed_password, "0")
    return {"message": "正常"}