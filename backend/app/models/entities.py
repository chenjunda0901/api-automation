from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(20), default="member")  # admin, member, viewer
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Environment(Base):
    __tablename__ = "environments"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    variables = Column(JSON, default={})  # {"key": "value"}
    headers = Column(JSON, default={})  # global headers
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ApiDefinition(Base):
    __tablename__ = "api_definitions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    method = Column(String(10), nullable=False)  # GET, POST, PUT, DELETE, etc.
    path = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    headers = Column(JSON, default=[])
    params = Column(JSON, default=[])
    body = Column(JSON, nullable=True)
    body_type = Column(String(20), default="none")  # none, json, form, raw
    response = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    api_id = Column(Integer, ForeignKey("api_definitions.id"), nullable=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    headers = Column(JSON, default=[])
    params = Column(JSON, default=[])
    body = Column(JSON, nullable=True)
    body_type = Column(String(20), default="none")
    pre_script = Column(Text, nullable=True)
    post_script = Column(Text, nullable=True)
    assertions = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TestScene(Base):
    __tablename__ = "test_scenes"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    global_variables = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SceneStep(Base):
    __tablename__ = "scene_steps"

    id = Column(Integer, primary_key=True, index=True)
    scene_id = Column(Integer, ForeignKey("test_scenes.id"), nullable=False)
    name = Column(String(100), nullable=False)
    step_type = Column(String(20), nullable=False)  # api, case
    ref_id = Column(Integer, nullable=True)  # api_id or case_id
    order = Column(Integer, nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TestReport(Base):
    __tablename__ = "test_reports"

    id = Column(Integer, primary_key=True, index=True)
    scene_id = Column(Integer, ForeignKey("test_scenes.id"), nullable=False)
    status = Column(String(20), nullable=False)  # running, passed, failed
    total_steps = Column(Integer, default=0)
    passed_steps = Column(Integer, default=0)
    failed_steps = Column(Integer, default=0)
    duration_ms = Column(Integer, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)


class ReportStep(Base):
    __tablename__ = "report_steps"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("test_reports.id"), nullable=False)
    step_name = Column(String(100), nullable=False)
    step_type = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)  # passed, failed, skipped
    request_data = Column(JSON, nullable=True)
    response_data = Column(JSON, nullable=True)
    assertions_result = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MockRule(Base):
    __tablename__ = "mock_rules"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    method = Column(String(10), nullable=False)
    path = Column(String(500), nullable=False)
    match_type = Column(String(20), default="exact")  # exact, prefix, regex
    response_status = Column(Integer, default=200)
    response_body = Column(Text, nullable=True)
    response_headers = Column(JSON, default={})
    delay_ms = Column(Integer, default=0)
    enabled = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())