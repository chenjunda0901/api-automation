from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List, Optional
import re

from app.database import get_db
from app.models.entities import MockRule
from app.schemas.mock import MockRuleCreate, MockRuleUpdate, MockRuleResponse
from app.middleware.auth import get_current_user
from app.models.user import User
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/api/mock", tags=["Mock服务"])


@router.get("/project/{project_id}", response_model=List[MockRuleResponse])
async def list_mock_rules(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目的 Mock 规则列表"""
    result = await db.execute(
        select(MockRule).where(MockRule.project_id == project_id).order_by(MockRule.priority.desc())
    )
    return result.scalars().all()


@router.post("", response_model=MockRuleResponse)
async def create_mock_rule(
    rule_data: MockRuleCreate,
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建 Mock 规则"""
    rule = MockRule(
        project_id=project_id,
        name=rule_data.name,
        method=rule_data.method,
        path=rule_data.path,
        match_type=rule_data.match_type,
        response_status=rule_data.response_status,
        response_body=rule_data.response_body,
        response_headers=rule_data.response_headers,
        delay_ms=rule_data.delay_ms,
        enabled=rule_data.enabled,
        priority=rule_data.priority
    )
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.get("/{rule_id}", response_model=MockRuleResponse)
async def get_mock_rule(
    rule_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取 Mock 规则详情"""
    result = await db.execute(select(MockRule).where(MockRule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
        raise NotFoundError("Mock rule not found")
    return rule


@router.put("/{rule_id}", response_model=MockRuleResponse)
async def update_mock_rule(
    rule_id: int,
    rule_data: MockRuleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新 Mock 规则"""
    result = await db.execute(select(MockRule).where(MockRule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
        raise NotFoundError("Mock rule not found")

    for key, value in rule_data.model_dump(exclude_unset=True).items():
        setattr(rule, key, value)

    await db.commit()
    await db.refresh(rule)
    return rule


@router.delete("/{rule_id}")
async def delete_mock_rule(
    rule_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除 Mock 规则"""
    await db.execute(delete(MockRule).where(MockRule.id == rule_id))
    await db.commit()
    return {"message": "Mock rule deleted"}


@router.post("/match")
async def match_mock_rule(
    project_id: int,
    method: str,
    path: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """匹配 Mock 规则（内部使用）"""
    result = await db.execute(
        select(MockRule).where(
            MockRule.project_id == project_id,
            MockRule.enabled == True,
            MockRule.method == method.upper()
        ).order_by(MockRule.priority.desc())
    )
    rules = result.scalars().all()
    
    for rule in rules:
        matched = False
        if rule.match_type == "exact":
            matched = rule.path == path
        elif rule.match_type == "prefix":
            matched = path.startswith(rule.path)
        elif rule.match_type == "regex":
            try:
                matched = bool(re.match(rule.path, path))
            except re.error:
                pass
        
        if matched:
            return {
                "matched": True,
                "rule_id": rule.id,
                "status": rule.response_status,
                "body": rule.response_body,
                "headers": rule.response_headers,
                "delay_ms": rule.delay_ms
            }
    
    return {"matched": False}