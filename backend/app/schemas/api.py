from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ApiHeader(BaseModel):
    key: str
    value: str
    enabled: bool = True


class ApiParam(BaseModel):
    key: str
    value: str
    enabled: bool = True


class ApiDefinitionBase(BaseModel):
    name: str
    method: str
    path: str
    description: Optional[str] = None


class ApiDefinitionCreate(ApiDefinitionBase):
    headers: List[ApiHeader] = []
    params: List[ApiParam] = []
    body: Optional[Dict[str, Any]] = None
    body_type: str = "none"
    response: Optional[Dict[str, Any]] = None


class ApiDefinitionUpdate(BaseModel):
    name: Optional[str] = None
    method: Optional[str] = None
    path: Optional[str] = None
    description: Optional[str] = None
    headers: Optional[List[ApiHeader]] = None
    params: Optional[List[ApiParam]] = None
    body: Optional[Dict[str, Any]] = None
    body_type: Optional[str] = None
    response: Optional[Dict[str, Any]] = None


class ApiDefinitionResponse(ApiDefinitionBase):
    id: int
    project_id: int
    headers: List[Dict[str, Any]] = []
    params: List[Dict[str, Any]] = []
    body: Optional[Dict[str, Any]] = None
    body_type: str
    response: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TestCaseBase(BaseModel):
    name: str
    description: Optional[str] = None


class TestCaseCreate(TestCaseBase):
    api_id: Optional[int] = None
    headers: List[ApiHeader] = []
    params: List[ApiParam] = []
    body: Optional[Dict[str, Any]] = None
    body_type: str = "none"
    pre_script: Optional[str] = None
    post_script: Optional[str] = None
    assertions: List[Dict[str, Any]] = []


class TestCaseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    api_id: Optional[int] = None
    headers: Optional[List[ApiHeader]] = None
    params: Optional[List[ApiParam]] = None
    body: Optional[Dict[str, Any]] = None
    body_type: Optional[str] = None
    pre_script: Optional[str] = None
    post_script: Optional[str] = None
    assertions: Optional[List[Dict[str, Any]]] = None


class TestCaseResponse(TestCaseBase):
    id: int
    project_id: int
    api_id: Optional[int] = None
    headers: List[Dict[str, Any]] = []
    params: List[Dict[str, Any]] = []
    body: Optional[Dict[str, Any]] = None
    body_type: str
    pre_script: Optional[str] = None
    post_script: Optional[str] = None
    assertions: List[Dict[str, Any]] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AssertionCreate(BaseModel):
    path: str
    operator: str  # eq, ne, gt, lt, contains, not_contains, in, not_in
    expected: Any


class TestSceneBase(BaseModel):
    name: str
    description: Optional[str] = None


class TestSceneCreate(TestSceneBase):
    global_variables: Dict[str, str] = {}


class TestSceneUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    global_variables: Optional[Dict[str, str]] = None


class TestSceneResponse(TestSceneBase):
    id: int
    project_id: int
    global_variables: Dict[str, str] = {}
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SceneStepBase(BaseModel):
    name: str
    step_type: str  # api, case
    ref_id: int
    order: int
    enabled: bool = True


class SceneStepCreate(SceneStepBase):
    pass


class SceneStepUpdate(BaseModel):
    name: Optional[str] = None
    step_type: Optional[str] = None
    ref_id: Optional[int] = None
    order: Optional[int] = None
    enabled: Optional[bool] = None


class SceneStepResponse(SceneStepBase):
    id: int
    scene_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True