from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class RunSceneRequest(BaseModel):
    scene_id: int
    environment_id: Optional[int] = None


class TestReportResponse(BaseModel):
    id: int
    scene_id: int
    status: str
    total_steps: int
    passed_steps: int
    failed_steps: int
    duration_ms: Optional[int] = None
    started_at: datetime
    finished_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ReportStepResponse(BaseModel):
    id: int
    report_id: int
    step_name: str
    step_type: str
    status: str
    request_data: Optional[Dict[str, Any]] = None
    response_data: Optional[Dict[str, Any]] = None
    assertions_result: Optional[List[Dict[str, Any]]] = None
    error_message: Optional[str] = None
    duration_ms: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class RunResultResponse(BaseModel):
    report_id: int
    status: str
    message: str