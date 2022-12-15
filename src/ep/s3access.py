import datetime
from typing import List
from fastapi import Depends, APIRouter, Security
from fastapi.responses import FileResponse
import boto3
import boto3.s3
from src.model.response_models import FileInfo

from src.model.entities import DownloadUser
from src.config.auth_config import get_current_user
import src.config.config as config

#ルーティング定義
router = APIRouter(
    prefix="/s3",
    tags=["s3"]
)

# 取得
@router.get('/', response_model=List[FileInfo])
async def get_file_list(current_user: DownloadUser = Security(get_current_user, scopes=["general"])):
    
    # s3操作オブジェクトを取得
    s3 = boto3.resource(
        's3',
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.REGION_NAME
    )
    
    # バケット一覧を表示
    for bucket in s3.buckets.all():
        print(bucket.name)
    
    # バケット情報を取得
    bucket = s3.Bucket('python-access-test-202212070919')
    
    resp: List[FileInfo] = []
    # バケット内のファイル一覧を表示
    for obj in bucket.objects.all():
        resp.append(FileInfo(file_name=obj.key, owner=obj.owner["DisplayName"], content_length=obj.size, last_modified=obj.last_modified))
    
    return resp
