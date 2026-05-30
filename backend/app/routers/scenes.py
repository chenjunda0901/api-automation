from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
from app.database import get_db
from app.models.entities import TestScene, SceneStep
from app.schemas.api import (
    TestSceneCreate, TestSceneUpdate, TestSceneResponse,
    SceneStepCreate, SceneStepUpdate, SceneStepResponse
)
from app.middleware.auth import get_current_user
from app.models.user import User
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/api/scenes", tags=["场景管理"])


@router.get("/project/{project_id}", response_model=List[TestSceneResponse])
async def list_scenes(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取项目的场景列表"""
    result = await db.execute(
        select(TestScene).where(TestScene.project_id == project_id).order_by(TestScene.updated_at.desc())
    )
    return result.scalars().all()


@router.post("", response_model=TestSceneResponse)
async def create_scene(
    scene_data: TestSceneCreate,
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建场景"""
    scene = TestScene(
        project_id=project_id,
        name=scene_data.name,
        description=scene_data.description,
        global_variables=scene_data.global_variables
    )
    db.add(scene)
    await db.commit()
    await db.refresh(scene)
    return scene


@router.get("/{scene_id}", response_model=TestSceneResponse)
async def get_scene(
    scene_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取场景详情"""
    result = await db.execute(select(TestScene).where(TestScene.id == scene_id))
    scene = result.scalar_one_or_none()
    if not scene:
        raise NotFoundError("Scene not found")
    return scene


@router.put("/{scene_id}", response_model=TestSceneResponse)
async def update_scene(
    scene_id: int,
    scene_data: TestSceneUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新场景"""
    result = await db.execute(select(TestScene).where(TestScene.id == scene_id))
    scene = result.scalar_one_or_none()
    if not scene:
        raise NotFoundError("Scene not found")

    for key, value in scene_data.model_dump(exclude_unset=True).items():
        setattr(scene, key, value)

    await db.commit()
    await db.refresh(scene)
    return scene


@router.delete("/{scene_id}")
async def delete_scene(
    scene_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除场景"""
    await db.execute(delete(SceneStep).where(SceneStep.scene_id == scene_id))
    await db.execute(delete(TestScene).where(TestScene.id == scene_id))
    await db.commit()
    return {"message": "Scene deleted"}


# 场景步骤管理
@router.get("/{scene_id}/steps", response_model=List[SceneStepResponse])
async def list_scene_steps(
    scene_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取场景步骤列表"""
    result = await db.execute(
        select(SceneStep).where(SceneStep.scene_id == scene_id).order_by(SceneStep.order)
    )
    return result.scalars().all()


@router.post("/{scene_id}/steps", response_model=SceneStepResponse)
async def create_scene_step(
    scene_id: int,
    step_data: SceneStepCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建场景步骤"""
    step = SceneStep(
        scene_id=scene_id,
        name=step_data.name,
        step_type=step_data.step_type,
        ref_id=step_data.ref_id,
        order=step_data.order,
        enabled=step_data.enabled
    )
    db.add(step)
    await db.commit()
    await db.refresh(step)
    return step


@router.put("/{scene_id}/steps/{step_id}", response_model=SceneStepResponse)
async def update_scene_step(
    scene_id: int,
    step_id: int,
    step_data: SceneStepUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新场景步骤"""
    result = await db.execute(
        select(SceneStep).where(
            SceneStep.id == step_id,
            SceneStep.scene_id == scene_id
        )
    )
    step = result.scalar_one_or_none()
    if not step:
        raise NotFoundError("Step not found")

    for key, value in step_data.model_dump(exclude_unset=True).items():
        setattr(step, key, value)

    await db.commit()
    await db.refresh(step)
    return step


@router.delete("/{scene_id}/steps/{step_id}")
async def delete_scene_step(
    scene_id: int,
    step_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除场景步骤"""
    await db.execute(
        delete(SceneStep).where(
            SceneStep.id == step_id,
            SceneStep.scene_id == scene_id
        )
    )
    await db.commit()
    return {"message": "Step deleted"}


@router.post("/{scene_id}/steps/reorder")
async def reorder_scene_steps(
    scene_id: int,
    step_orders: List[dict],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """重新排序场景步骤"""
    for item in step_orders:
        result = await db.execute(
            select(SceneStep).where(
                SceneStep.id == item["id"],
                SceneStep.scene_id == scene_id
            )
        )
        step = result.scalar_one_or_none()
        if step:
            step.order = item["order"]

    await db.commit()
    return {"message": "Steps reordered"}