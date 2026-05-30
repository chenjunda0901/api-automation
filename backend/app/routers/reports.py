from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.entities import TestReport, ReportStep
from app.schemas.report import TestReportResponse, ReportStepResponse
from app.middleware.auth import get_current_user
from app.models.user import User
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/api/reports", tags=["测试报告"])


@router.get("/scene/{scene_id}", response_model=List[TestReportResponse])
async def list_reports(
    scene_id: int,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取场景的报告列表"""
    result = await db.execute(
        select(TestReport)
        .where(TestReport.scene_id == scene_id)
        .order_by(TestReport.started_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/{report_id}", response_model=TestReportResponse)
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取报告详情"""
    result = await db.execute(select(TestReport).where(TestReport.id == report_id))
    report = result.scalar_one_or_none()
    if not report:
        raise NotFoundError("Report not found")
    return report


@router.get("/{report_id}/steps", response_model=List[ReportStepResponse])
async def get_report_steps(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取报告步骤详情"""
    result = await db.execute(
        select(ReportStep).where(ReportStep.report_id == report_id).order_by(ReportStep.created_at)
    )
    return result.scalars().all()


@router.get("")
async def list_all_reports(
    project_id: int,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目的所有报告"""
    result = await db.execute(
        select(TestReport)
        .join(TestScene, TestReport.scene_id == TestScene.id)
        .where(TestScene.project_id == project_id)
        .order_by(TestReport.started_at.desc())
        .limit(limit)
    )
    reports = result.scalars().all()
    
    return [
        {
            "id": r.id,
            "scene_id": r.scene_id,
            "status": r.status,
            "total_steps": r.total_steps,
            "passed_steps": r.passed_steps,
            "failed_steps": r.failed_steps,
            "duration_ms": r.duration_ms,
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "finished_at": r.finished_at.isoformat() if r.finished_at else None
        }
        for r in reports
    ]


# 需要导入 TestScene
from app.models.entities import TestScene