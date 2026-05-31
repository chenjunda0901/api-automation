from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from app.database import get_db
from app.models.entities import Project, ApiDefinition, TestScene, TestReport, ProjectMember
from app.schemas.dashboard import (
    DashboardStatsResponse, TrendDataPoint, HealthScore,
    SceneStat, FailedScene, QuickAction
)
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/dashboard", tags=["仪表盘"])


@router.get("/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取仪表盘统计数据"""
    
    # 1. 获取用户项目列表（所有者或成员）
    member_projects = select(ProjectMember.project_id).where(ProjectMember.user_id == current_user.id)
    result = await db.execute(
        select(Project).where(
            (Project.owner_id == current_user.id) |
            (Project.id.in_(member_projects))
        )
    )
    user_projects = result.scalars().all()
    user_project_ids = [p.id for p in user_projects]
    
    # 2. 统计项目总数
    total_projects = len(user_project_ids)
    
    # 3. 统计接口总数
    if user_project_ids:
        apis_result = await db.execute(
            select(func.count(ApiDefinition.id)).where(
                ApiDefinition.project_id.in_(user_project_ids)
            )
        )
        total_apis = apis_result.scalar() or 0
    else:
        total_apis = 0
    
    # 4. 统计场景总数
    if user_project_ids:
        scenes_result = await db.execute(
            select(func.count(TestScene.id)).where(
                TestScene.project_id.in_(user_project_ids)
            )
        )
        total_scenes = scenes_result.scalar() or 0
    else:
        total_scenes = 0
    
    # 5. 统计总运行次数和通过率
    total_runs = 0
    pass_rate = 0.0
    avg_duration = 0
    
    if user_project_ids:
        scenes_subq = select(TestScene.id).where(TestScene.project_id.in_(user_project_ids))
        report_result = await db.execute(
            select(TestReport).where(TestReport.scene_id.in_(scenes_subq))
        )
        reports = report_result.scalars().all()
        
        total_runs = len(reports)
        if total_runs > 0:
            passed_runs = sum(1 for r in reports if r.status == 'passed')
            pass_rate = round(passed_runs / total_runs * 100, 1)
        else:
            pass_rate = 0.0
        
        durations = [r.duration_ms for r in reports if r.duration_ms]
        avg_duration = int(sum(durations) / len(durations)) if durations else 0
    else:
        total_runs = 0
        pass_rate = 0.0
        avg_duration = 0
    
    # 6. 生成趋势数据（最近7天）
    trend_data = []
    now = datetime.now()
    for i in range(6, -1, -1):
        target_date = now - timedelta(days=i)
        date_str = target_date.strftime('%Y-%m-%d')
        
        day_start = target_date.replace(hour=0, minute=0, second=0)
        day_end = target_date.replace(hour=23, minute=59, second=59)
        
        passed = 0
        failed = 0
        if user_project_ids:
            scenes_subq = select(TestScene.id).where(TestScene.project_id.in_(user_project_ids))
            day_reports = await db.execute(
                select(TestReport).where(
                    TestReport.scene_id.in_(scenes_subq),
                    TestReport.started_at >= day_start,
                    TestReport.started_at <= day_end
                )
            )
            reports_day = day_reports.scalars().all()
            passed = sum(1 for r in reports_day if r.status == 'passed')
            failed = sum(1 for r in reports_day if r.status == 'failed')
        
        trend_data.append(TrendDataPoint(
            date=date_str,
            passed=passed,
            failed=failed,
            total=passed + failed
        ))
    
    # 7. 健康度评分
    if pass_rate >= 95:
        score = min(100, int(pass_rate + 3))
        level = 'excellent'
    elif pass_rate >= 85:
        score = int(pass_rate)
        level = 'good'
    elif pass_rate >= 70:
        score = int(pass_rate)
        level = 'warning'
    else:
        score = max(0, int(pass_rate))
        level = 'critical'
    
    # 计算趋势（与上周对比）
    trend = 0
    if user_project_ids and total_runs > 0:
        week_ago = now - timedelta(days=7)
        two_weeks_ago = now - timedelta(days=14)
        
        scenes_subq = select(TestScene.id).where(TestScene.project_id.in_(user_project_ids))
        last_week_result = await db.execute(
            select(TestReport).where(
                TestReport.scene_id.in_(scenes_subq),
                TestReport.started_at >= two_weeks_ago,
                TestReport.started_at <= week_ago
            )
        )
        last_week_reports = last_week_result.scalars().all()
        
        if last_week_reports:
            last_week_passed = sum(1 for r in last_week_reports if r.status == 'passed')
            last_week_pass_rate = last_week_passed / len(last_week_reports) * 100
            trend = int(pass_rate - last_week_pass_rate)
    
    health_score = HealthScore(score=score, level=level, trend=trend)
    
    # 8. 热门场景TOP5
    top_scenes = []
    if user_project_ids:
        for project_id in user_project_ids:
            scenes_result = await db.execute(
                select(TestScene).where(TestScene.project_id == project_id)
            )
            scenes = scenes_result.scalars().all()
            
            for scene in scenes:
                runs_result = await db.execute(
                    select(func.count(TestReport.id)).where(TestReport.scene_id == scene.id)
                )
                runs = runs_result.scalar() or 0
                
                if runs > 0:
                    passed_result = await db.execute(
                        select(func.count(TestReport.id)).where(
                            TestReport.scene_id == scene.id,
                            TestReport.status == 'passed'
                        )
                    )
                    passed = passed_result.scalar() or 0
                    pass_rate_scene = round(passed / runs * 100, 1)
                    
                    last_report_result = await db.execute(
                        select(TestReport).where(
                            TestReport.scene_id == scene.id
                        ).order_by(TestReport.started_at.desc()).limit(1)
                    )
                    last = last_report_result.scalar_one_or_none()
                    
                    top_scenes.append(SceneStat(
                        id=scene.id,
                        name=scene.name,
                        runs=runs,
                        pass_rate=pass_rate_scene,
                        last_run=last.started_at.isoformat() if last and last.started_at else None,
                        last_status=last.status if last else None
                    ))
        
        top_scenes.sort(key=lambda x: x.runs, reverse=True)
        top_scenes = top_scenes[:5]
    
    # 9. 需要关注的失败场景
    failed_scenes = []
    if user_project_ids:
        for project_id in user_project_ids:
            scenes_result = await db.execute(
                select(TestScene).where(TestScene.project_id == project_id)
            )
            scenes = scenes_result.scalars().all()
            
            for scene in scenes:
                recent_fails_result = await db.execute(
                    select(TestReport).where(
                        TestReport.scene_id == scene.id,
                        TestReport.status == 'failed'
                    ).order_by(TestReport.started_at.desc()).limit(10)
                )
                fail_reports = recent_fails_result.scalars().all()
                
                if fail_reports:
                    fail_count = len(fail_reports)
                    last_fail = fail_reports[0].started_at.strftime('%Y-%m-%d %H:%M') if fail_reports[0].started_at else '未知时间'
                    
                    failed_scenes.append(FailedScene(
                        id=scene.id,
                        name=scene.name,
                        fail_count=fail_count,
                        last_fail=last_fail
                    ))
        
        failed_scenes.sort(key=lambda x: x.fail_count, reverse=True)
        failed_scenes = failed_scenes[:5]
    
    # 10. 快捷操作
    quick_actions = [
        QuickAction(id='new-project', name='新建项目', icon='folder-plus', route='/projects'),
        QuickAction(id='import-api', name='导入接口', icon='download', route='/apis'),
        QuickAction(id='run-scene', name='运行场景', icon='play', route='/scenes'),
    ]
    
    return DashboardStatsResponse(
        total_projects=total_projects,
        total_apis=total_apis,
        total_scenes=total_scenes,
        total_runs=total_runs,
        pass_rate=pass_rate,
        avg_duration=avg_duration,
        trend_data=trend_data,
        health_score=health_score,
        top_scenes=top_scenes,
        failed_scenes=failed_scenes,
        quick_actions=quick_actions
    )
