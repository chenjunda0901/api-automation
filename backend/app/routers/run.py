from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import typing

from app.database import get_db
from app.models.entities import TestScene, SceneStep, TestReport, ReportStep, Environment, ApiDefinition, TestCase
from app.schemas.report import RunSceneRequest, RunResultResponse
from app.middleware.auth import get_current_user
from app.models.user import User
from app.services.executor import LinearExecutor
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/api/run", tags=["执行"])


async def run_scene_task(scene_id: int, environment_id: typing.Optional[int], db_url: str):
    """后台执行场景任务"""
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as AsyncSessionLocal
    from sqlalchemy.orm import sessionmaker
    
    engine = create_async_engine(db_url, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as db:
        # 获取场景
        result = await db.execute(select(TestScene).where(TestScene.id == scene_id))
        scene = result.scalar_one_or_none()
        if not scene:
            return
        
        # 获取环境变量
        env_variables = {}
        if environment_id:
            result = await db.execute(select(Environment).where(Environment.id == environment_id))
            env = result.scalar_one_or_none()
            if env:
                env_variables = env.variables or {}
        
        # 获取场景步骤
        result = await db.execute(
            select(SceneStep).where(SceneStep.scene_id == scene_id).order_by(SceneStep.order)
        )
        steps = result.scalars().all()
        
        # 创建报告
        report = TestReport(
            scene_id=scene_id,
            status="running",
            total_steps=len(steps),
            passed_steps=0,
            failed_steps=0
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)
        
        # 执行器
        executor = LinearExecutor()
        scene_vars = scene.global_variables or {}
        executor.set_global_variables({**scene_vars, **env_variables})
        
        passed = 0
        failed = 0
        
        for step in steps:
            if not step.enabled:
                continue
            
            step_config = {
                "name": step.name,
                "step_type": step.step_type
            }
            
            assertions = []
            
            if step.step_type == "api":
                result = await db.execute(select(ApiDefinition).where(ApiDefinition.id == step.ref_id))
                api = result.scalar_one_or_none()
                if api:
                    step_config.update({
                        "method": api.method,
                        "path": api.path,
                        "headers": api.headers or [],
                        "params": api.params or [],
                        "body": api.body,
                        "body_type": api.body_type
                    })
                    # 从测试用例获取断言
                    case_result = await db.execute(
                        select(TestCase).where(
                            TestCase.api_id == api.id,
                            TestCase.project_id == scene.project_id
                        ).limit(1)
                    )
                    case = case_result.scalar_one_or_none()
                    if case:
                        assertions = case.assertions or []
            elif step.step_type == "case":
                result = await db.execute(select(TestCase).where(TestCase.id == step.ref_id))
                case = result.scalar_one_or_none()
                if case:
                    step_config.update({
                        "method": "POST",
                        "path": "/case/execute",
                        "headers": case.headers or [],
                        "params": case.params or [],
                        "body": case.body,
                        "body_type": case.body_type,
                        "pre_script": case.pre_script,
                        "post_script": case.post_script
                    })
                    assertions = case.assertions or []
            
            result = await executor.execute_step(step.step_type, step_config, assertions)
            
            # 保存步骤报告
            report_step = ReportStep(
                report_id=report.id,
                step_name=result.step_name,
                step_type=result.step_type,
                status=result.status,
                request_data=result.request_data,
                response_data=result.response_data,
                assertions_result=result.assertions_result,
                error_message=result.error_message,
                duration_ms=result.duration_ms
            )
            db.add(report_step)
            
            if result.status == "passed":
                passed += 1
            else:
                failed += 1
        
        # 更新报告状态
        report.status = "passed" if failed == 0 else "failed"
        report.passed_steps = passed
        report.failed_steps = failed
        report.finished_at = datetime.now()
        
        await db.commit()


@router.post("/scene", response_model=RunResultResponse)
async def run_scene(
    request: RunSceneRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """执行场景（异步）"""
    # 验证场景存在
    result = await db.execute(select(TestScene).where(TestScene.id == request.scene_id))
    scene = result.scalar_one_or_none()
    if not scene:
        raise NotFoundError("Scene not found")
    
    # 获取数据库 URL
    from app.config import settings
    db_url = settings.DATABASE_URL
    
    # 后台执行
    background_tasks.add_task(run_scene_task, request.scene_id, request.environment_id, db_url)
    
    return RunResultResponse(
        report_id=0,  # 将在任务中创建
        status="running",
        message="Scene execution started"
    )


@router.post("/scene/sync", response_model=dict)
async def run_scene_sync(
    request: RunSceneRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """同步执行场景（返回完整报告）"""
    # 获取场景
    result = await db.execute(select(TestScene).where(TestScene.id == request.scene_id))
    scene = result.scalar_one_or_none()
    if not scene:
        raise NotFoundError("Scene not found")
    
    # 获取环境变量
    env_variables = {}
    if request.environment_id:
        result = await db.execute(select(Environment).where(Environment.id == request.environment_id))
        env = result.scalar_one_or_none()
        if env:
            env_variables = env.variables or {}
    
    # 获取场景步骤
    result = await db.execute(
        select(SceneStep).where(SceneStep.scene_id == request.scene_id).order_by(SceneStep.order)
    )
    steps = result.scalars().all()
    
    # 创建报告
    report = TestReport(
        scene_id=request.scene_id,
        status="running",
        total_steps=len(steps),
        passed_steps=0,
        failed_steps=0
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    
    # 执行器
    executor = LinearExecutor()
    scene_vars = scene.global_variables or {}
    executor.set_global_variables({**scene_vars, **env_variables})
    
    passed = 0
    failed = 0
    step_results = []
    
    for step in steps:
        if not step.enabled:
            continue
        
        step_config = {"name": step.name, "step_type": step.step_type}
        assertions = []
        
        if step.step_type == "api":
            result = await db.execute(select(ApiDefinition).where(ApiDefinition.id == step.ref_id))
            api = result.scalar_one_or_none()
            if api:
                step_config.update({
                    "method": api.method,
                    "url": api.path,
                    "headers": api.headers or [],
                    "params": api.params or [],
                    "body": api.body,
                    "body_type": api.body_type
                })
                case_result = await db.execute(
                    select(TestCase).where(
                        TestCase.api_id == api.id,
                        TestCase.project_id == scene.project_id
                    ).limit(1)
                )
                case = case_result.scalar_one_or_none()
                if case:
                    assertions = case.assertions or []
        elif step.step_type == "case":
            result = await db.execute(select(TestCase).where(TestCase.id == step.ref_id))
            case = result.scalar_one_or_none()
            if case:
                step_config.update({
                    "method": "POST",
                    "url": "/case/execute",
                    "headers": case.headers or [],
                    "params": case.params or [],
                    "body": case.body,
                    "body_type": case.body_type,
                    "pre_script": case.pre_script,
                    "post_script": case.post_script
                })
                assertions = case.assertions or []
        
        result = await executor.execute_step(step.step_type, step_config, assertions)
        
        report_step = ReportStep(
            report_id=report.id,
            step_name=result.step_name,
            step_type=result.step_type,
            status=result.status,
            request_data=result.request_data,
            response_data=result.response_data,
            assertions_result=result.assertions_result,
            error_message=result.error_message,
            duration_ms=result.duration_ms
        )
        db.add(report_step)
        
        if result.status == "passed":
            passed += 1
        else:
            failed += 1
        
        step_results.append(result.to_dict())
    
    report.status = "passed" if failed == 0 else "failed"
    report.passed_steps = passed
    report.failed_steps = failed
    report.finished_at = datetime.now()
    
    await db.commit()
    
    return {
        "report_id": report.id,
        "status": report.status,
        "total_steps": len(steps),
        "passed_steps": passed,
        "failed_steps": failed,
        "steps": step_results
    }