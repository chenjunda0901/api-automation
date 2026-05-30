from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
from app.database import get_db
from app.models.entities import ApiDefinition, TestCase
from app.schemas.api import (
    ApiDefinitionCreate, ApiDefinitionUpdate, ApiDefinitionResponse,
    TestCaseCreate, TestCaseUpdate, TestCaseResponse
)
from app.middleware.auth import get_current_user
from app.models.user import User
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/api/apis", tags=["接口管理"])


@router.get("/project/{project_id}", response_model=List[ApiDefinitionResponse])
async def list_apis(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目的接口列表"""
    result = await db.execute(
        select(ApiDefinition).where(ApiDefinition.project_id == project_id).order_by(ApiDefinition.updated_at.desc())
    )
    return result.scalars().all()


@router.post("", response_model=ApiDefinitionResponse)
async def create_api(
    api_data: ApiDefinitionCreate,
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建接口"""
    api = ApiDefinition(
        project_id=project_id,
        name=api_data.name,
        method=api_data.method,
        path=api_data.path,
        description=api_data.description,
        headers=[h.model_dump() for h in api_data.headers],
        params=[p.model_dump() for p in api_data.params],
        body=api_data.body,
        body_type=api_data.body_type,
        response=api_data.response
    )
    db.add(api)
    await db.commit()
    await db.refresh(api)
    return api


@router.get("/{api_id}", response_model=ApiDefinitionResponse)
async def get_api(
    api_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取接口详情"""
    result = await db.execute(select(ApiDefinition).where(ApiDefinition.id == api_id))
    api = result.scalar_one_or_none()
    if not api:
        raise NotFoundError("API not found")
    return api


@router.put("/{api_id}", response_model=ApiDefinitionResponse)
async def update_api(
    api_id: int,
    api_data: ApiDefinitionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新接口"""
    result = await db.execute(select(ApiDefinition).where(ApiDefinition.id == api_id))
    api = result.scalar_one_or_none()
    if not api:
        raise NotFoundError("API not found")

    update_data = api_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key in ["headers", "params"]:
            if isinstance(value, list):
                value = [v.model_dump() if hasattr(v, "model_dump") else v for v in value]
        setattr(api, key, value)

    await db.commit()
    await db.refresh(api)
    return api


@router.delete("/{api_id}")
async def delete_api(
    api_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除接口"""
    await db.execute(delete(ApiDefinition).where(ApiDefinition.id == api_id))
    await db.commit()
    return {"message": "API deleted"}


# 测试用例路由
router_cases = APIRouter(prefix="/api/cases", tags=["测试用例"])


@router_cases.get("/project/{project_id}", response_model=List[TestCaseResponse])
async def list_cases(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目的测试用例列表"""
    result = await db.execute(
        select(TestCase).where(TestCase.project_id == project_id).order_by(TestCase.updated_at.desc())
    )
    return result.scalars().all()


@router_cases.post("", response_model=TestCaseResponse)
async def create_case(
    case_data: TestCaseCreate,
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建测试用例"""
    case = TestCase(
        project_id=project_id,
        name=case_data.name,
        description=case_data.description,
        api_id=case_data.api_id,
        headers=[h.model_dump() for h in case_data.headers],
        params=[p.model_dump() for p in case_data.params],
        body=case_data.body,
        body_type=case_data.body_type,
        pre_script=case_data.pre_script,
        post_script=case_data.post_script,
        assertions=case_data.assertions
    )
    db.add(case)
    await db.commit()
    await db.refresh(case)
    return case


@router_cases.get("/{case_id}", response_model=TestCaseResponse)
async def get_case(
    case_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取测试用例详情"""
    result = await db.execute(select(TestCase).where(TestCase.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise NotFoundError("Test case not found")
    return case


@router_cases.put("/{case_id}", response_model=TestCaseResponse)
async def update_case(
    case_id: int,
    case_data: TestCaseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新测试用例"""
    result = await db.execute(select(TestCase).where(TestCase.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise NotFoundError("Test case not found")

    update_data = case_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key in ["headers", "params"]:
            if isinstance(value, list):
                value = [v.model_dump() if hasattr(v, "model_dump") else v for v in value]
        setattr(case, key, value)

    await db.commit()
    await db.refresh(case)
    return case


@router_cases.delete("/{case_id}")
async def delete_case(
    case_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除测试用例"""
    await db.execute(delete(TestCase).where(TestCase.id == case_id))
    await db.commit()
    return {"message": "Test case deleted"}