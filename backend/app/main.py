from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.database import init_db
from app.core.exceptions import BizError
from app.routers import (
    auth_router,
    projects_router,
    apis_router,
    router_cases,
    scenes_router,
    reports_router,
    run_router,
    mock_router,
    import_export_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    os.makedirs("./data", exist_ok=True)
    await init_db()
    await seed_demo_data()
    yield
    # 关闭时清理


app = FastAPI(
    title="API Pilot",
    description="企业级接口自动化测试平台",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理
@app.exception_handler(BizError)
async def biz_error_handler(request: Request, exc: BizError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message}
    )


@app.exception_handler(Exception)
async def general_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"code": "INTERNAL_ERROR", "message": str(exc)}
    )


# 注册路由
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(apis_router)
app.include_router(router_cases)
app.include_router(scenes_router)
app.include_router(reports_router)
app.include_router(run_router)
app.include_router(mock_router)
app.include_router(import_export_router)


# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# 根路径
@app.get("/")
async def root():
    return {
        "name": "API Pilot",
        "version": "1.0.0",
        "description": "企业级接口自动化测试平台"
    }


async def seed_demo_data():
    """创建演示账号"""
    from app.database import AsyncSessionLocal
    from app.models.user import User
    from app.middleware.auth import get_password_hash
    from sqlalchemy import select

    async with AsyncSessionLocal() as db:
        # 检查是否已有 admin 用户
        result = await db.execute(select(User).where(User.username == "admin"))
        if result.scalar_one_or_none():
            return

        # 创建 admin 用户
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_superuser=True
        )
        db.add(admin)

        # 创建 demo 用户
        demo = User(
            username="demo",
            email="demo@example.com",
            hashed_password=get_password_hash("demo123"),
            is_active=True,
            is_superuser=False
        )
        db.add(demo)

        await db.commit()