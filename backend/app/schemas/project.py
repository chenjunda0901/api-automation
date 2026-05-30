from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProjectMemberBase(BaseModel):
    user_id: int
    role: str = "member"


class ProjectMemberCreate(ProjectMemberBase):
    pass


class ProjectMemberResponse(ProjectMemberBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class EnvironmentBase(BaseModel):
    name: str
    variables: Dict[str, str] = {}
    headers: Dict[str, str] = {}


class EnvironmentCreate(EnvironmentBase):
    pass


class EnvironmentUpdate(BaseModel):
    name: Optional[str] = None
    variables: Optional[Dict[str, str]] = None
    headers: Optional[Dict[str, str]] = None


class EnvironmentResponse(EnvironmentBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EnvVarCreate(BaseModel):
    key: str
    value: str


class EnvVarUpdate(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None