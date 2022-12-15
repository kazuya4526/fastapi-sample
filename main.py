from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from src.ep.auth import router as auth_router
from src.ep.s3access import router as s3access_router

###############################################################################
#=============================Config==========================================#
###############################################################################

# FastAPIインスタンス生成
app = FastAPI()

# CORS設定
origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routing設定
app.include_router(auth_router)
app.include_router(s3access_router)