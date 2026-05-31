from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
import html
import re
from app.database import get_db
from app.models.entities import Project, ProjectMember, Environment
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectMemberCreate, ProjectMemberResponse, EnvironmentCreate, EnvironmentUpdate, EnvironmentResponse
from app.middleware.auth import get_current_user
from app.models.user import User
from app.core.exceptions import NotFoundError, ForbiddenError

router = APIRouter(prefix="/api/projects", tags=["项目管理"])


def sanitize_html(text: str) -> str:
    """清理HTML和脚本内容，防止XSS攻击"""
    if not text:
        return text
    # HTML转义
    escaped = html.escape(text, quote=True)
    # 额外移除script标签和事件处理器
    patterns = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
    ]
    for pattern in patterns:
        escaped = re.sub(pattern, '', escaped, flags=re.IGNORECASE | re.DOTALL)
    return escaped


@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目列表"""
    # 获取用户拥有或参与的项目
    result = await db.execute(
        select(Project).where(
            (Project.owner_id == current_user.id) |
            (Project.id.in_(
                select(ProjectMember.project_id).where(ProjectMember.user_id == current_user.id)
            ))
        ).order_by(Project.updated_at.desc())
    )
    return result.scalars().all()


@router.post("", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建项目"""
    project = Project(
        name=sanitize_html(project_data.name),
        description=sanitize_html(project_data.description) if project_data.description else None,
        owner_id=current_user.id
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目详情"""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise NotFoundError("Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新项目"""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise NotFoundError("Project not found")

    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise ForbiddenError("No permission to update this project")

    for key, value in project_data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)

    await db.commit()
    await db.refresh(project)
    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除项目"""
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise NotFoundError("Project not found")

    if project.owner_id != current_user.id and not current_user.is_superuser:
        raise ForbiddenError("No permission to delete this project")

    await db.execute(delete(Project).where(Project.id == project_id))
    await db.commit()
    return {"message": "Project deleted"}


# 项目成员管理
@router.get("/{project_id}/members", response_model=List[ProjectMemberResponse])
async def list_project_members(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目成员列表"""
    result = await db.execute(
        select(ProjectMember).where(ProjectMember.project_id == project_id)
    )
    return result.scalars().all()


@router.post("/{project_id}/members", response_model=ProjectMemberResponse)
async def add_project_member(
    project_id: int,
    member_data: ProjectMemberCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """添加项目成员"""
    member = ProjectMember(
        project_id=project_id,
        user_id=member_data.user_id,
        role=member_data.role
    )
    db.add(member)
    await db.commit()
    await db.refresh(member)
    return member


@router.delete("/{project_id}/members/{member_id}")
async def remove_project_member(
    project_id: int,
    member_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """移除项目成员"""
    await db.execute(
        delete(ProjectMember).where(
            ProjectMember.id == member_id,
            ProjectMember.project_id == project_id
        )
    )
    await db.commit()
    return {"message": "Member removed"}


# 环境管理
@router.get("/{project_id}/environments", response_model=List[EnvironmentResponse])
async def list_environments(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取环境列表"""
    result = await db.execute(
        select(Environment).where(Environment.project_id == project_id)
    )
    return result.scalars().all()


@router.post("/{project_id}/environments", response_model=EnvironmentResponse)
async def create_environment(
    project_id: int,
    env_data: EnvironmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建环境"""
    environment = Environment(
        project_id=project_id,
        name=env_data.name,
        variables=env_data.variables,
        headers=env_data.headers
    )
    db.add(environment)
    await db.commit()
    await db.refresh(environment)
    return environment


@router.get("/{project_id}/environments/{env_id}", response_model=EnvironmentResponse)
async def get_environment(
    project_id: int,
    env_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取环境详情"""
    result = await db.execute(
        select(Environment).where(
            Environment.id == env_id,
            Environment.project_id == project_id
        )
    )
    env = result.scalar_one_or_none()
    if not env:
        raise NotFoundError("Environment not found")
    return env


@router.put("/{project_id}/environments/{env_id}", response_model=EnvironmentResponse)
async def update_environment(
    project_id: int,
    env_id: int,
    env_data: EnvironmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新环境"""
    result = await db.execute(
        select(Environment).where(
            Environment.id == env_id,
            Environment.project_id == project_id
        )
    )
    environment = result.scalar_one_or_none()
    if not environment:
        raise NotFoundError("Environment not found")

    for key, value in env_data.model_dump(exclude_unset=True).items():
        setattr(environment, key, value)

    await db.commit()
    await db.refresh(environment)
    return environment


@router.delete("/{project_id}/environments/{env_id}")
async def delete_environment(
    project_id: int,
    env_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除环境"""
    await db.execute(
        delete(Environment).where(
            Environment.id == env_id,
            Environment.project_id == project_id
        )
    )
    await db.commit()
    return {"message": "Environment deleted"}