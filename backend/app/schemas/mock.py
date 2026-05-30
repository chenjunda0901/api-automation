from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class MockRuleBase(BaseModel):
    name: str
    method: str
    path: str
    match_type: str = "exact"
    response_status: int = 200
    response_body: Optional[str] = None
    response_headers: Dict[str, str] = {}
    delay_ms: int = 0
    enabled: bool = True
    priority: int = 0


class MockRuleCreate(MockRuleBase):
    pass


class MockRuleUpdate(BaseModel):
    name: Optional[str] = None
    method: Optional[str] = None
    path: Optional[str] = None
    match_type: Optional[str] = None
    response_status: Optional[int] = None
    response_body: Optional[str] = None
    response_headers: Optional[Dict[str, str]] = None
    delay_ms: Optional[int] = None
    enabled: Optional[bool] = None
    priority: Optional[int] = None


class MockRuleResponse(MockRuleBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MockMatchRequest(BaseModel):
    method: str
    path: str
    headers: Optional[Dict[str, str]] = None
    body: Optional[str] = None


class MockMatchResponse(BaseModel):
    matched: bool
    rule_id: Optional[int] = None
    status: Optional[int] = None
    body: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    delay_ms: Optional[int] = None