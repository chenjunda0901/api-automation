from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TrendDataPoint(BaseModel):
    date: str
    passed: int
    failed: int
    total: int


class HealthScore(BaseModel):
    score: int
    level: str
    trend: int


class SceneStat(BaseModel):
    id: int
    name: str
    runs: int
    pass_rate: float
    last_run: Optional[str] = None
    last_status: Optional[str] = None


class FailedScene(BaseModel):
    id: int
    name: str
    fail_count: int
    last_fail: str


class QuickAction(BaseModel):
    id: str
    name: str
    icon: str
    route: str


class DashboardStatsResponse(BaseModel):
    total_projects: int
    total_apis: int
    total_scenes: int
    total_runs: int
    pass_rate: float
    avg_duration: int
    trend_data: List[TrendDataPoint]
    health_score: HealthScore
    top_scenes: List[SceneStat]
    failed_scenes: List[FailedScene]
    quick_actions: List[QuickAction]
