from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import json
import csv
from io import StringIO

from app.database import get_db
from app.models.entities import ApiDefinition, TestCase, TestScene, SceneStep, Environment
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/import-export", tags=["导入导出"])


@router.get("/export/project/{project_id}")
async def export_project(
    project_id: int,
    format: str = "json",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """导出项目数据"""
    # 获取项目数据
    apis_result = await db.execute(select(ApiDefinition).where(ApiDefinition.project_id == project_id))
    apis = apis_result.scalars().all()
    
    cases_result = await db.execute(select(TestCase).where(TestCase.project_id == project_id))
    cases = cases_result.scalars().all()
    
    scenes_result = await db.execute(select(TestScene).where(TestScene.project_id == project_id))
    scenes = scenes_result.scalars().all()
    
    env_result = await db.execute(select(Environment).where(Environment.project_id == project_id))
    environments = env_result.scalars().all()
    
    data = {
        "apis": [api_to_dict(api) for api in apis],
        "cases": [case_to_dict(case) for case in cases],
        "scenes": [scene_to_dict(scene) for scene in scenes],
        "environments": [env_to_dict(env) for env in environments]
    }
    
    if format == "csv":
        # CSV 格式只导出 API
        csv_data = apis_to_csv([api_to_dict(api) for api in apis])
        return JSONResponse(content={"csv": csv_data})
    
    return data


@router.post("/import/project/{project_id}")
async def import_project(
    project_id: int,
    format: str = "json",
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """导入项目数据"""
    content = await file.read()
    
    if format == "json":
        data = json.loads(content)
        
        imported = {"apis": 0, "cases": 0, "scenes": 0, "environments": 0}
        
        # 导入 API
        for api_data in data.get("apis", []):
            api = ApiDefinition(
                project_id=project_id,
                name=api_data.get("name"),
                method=api_data.get("method"),
                path=api_data.get("path"),
                description=api_data.get("description"),
                headers=api_data.get("headers", []),
                params=api_data.get("params", []),
                body=api_data.get("body"),
                body_type=api_data.get("body_type", "none"),
                response=api_data.get("response")
            )
            db.add(api)
            imported["apis"] += 1
        
        # 导入环境
        for env_data in data.get("environments", []):
            env = Environment(
                project_id=project_id,
                name=env_data.get("name"),
                variables=env_data.get("variables", {}),
                headers=env_data.get("headers", {})
            )
            db.add(env)
            imported["environments"] += 1
        
        await db.commit()
        
        return {"message": "Import completed", "imported": imported}
    
    return {"error": "Unsupported format"}


def api_to_dict(api: ApiDefinition) -> dict:
    return {
        "name": api.name,
        "method": api.method,
        "path": api.path,
        "description": api.description,
        "headers": api.headers,
        "params": api.params,
        "body": api.body,
        "body_type": api.body_type,
        "response": api.response
    }


def case_to_dict(case: TestCase) -> dict:
    return {
        "name": case.name,
        "description": case.description,
        "api_id": case.api_id,
        "headers": case.headers,
        "params": case.params,
        "body": case.body,
        "body_type": case.body_type,
        "pre_script": case.pre_script,
        "post_script": case.post_script,
        "assertions": case.assertions
    }


def scene_to_dict(scene: TestScene) -> dict:
    return {
        "name": scene.name,
        "description": scene.description,
        "global_variables": scene.global_variables
    }


def env_to_dict(env: Environment) -> dict:
    return {
        "name": env.name,
        "variables": env.variables,
        "headers": env.headers
    }


def apis_to_csv(apis: List[dict]) -> str:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["name", "method", "path", "description"])
    for api in apis:
        writer.writerow([
            api.get("name", ""),
            api.get("method", ""),
            api.get("path", ""),
            api.get("description", "")
        ])
    return output.getvalue()