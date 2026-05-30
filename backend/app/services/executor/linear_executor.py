from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from app.services.executor.variable_renderer import VariableRenderer
from app.services.executor.assertion_engine import AssertionEngine
from app.services.executor.request_builder import RequestBuilder
from app.services.executor.script_executor import ScriptExecutor


class StepResult:
    """步骤执行结果"""

    def __init__(
        self,
        step_name: str,
        step_type: str,
        status: str,
        request_data: Optional[Dict[str, Any]] = None,
        response_data: Optional[Dict[str, Any]] = None,
        assertions_result: Optional[List[Dict[str, Any]]] = None,
        error_message: Optional[str] = None,
        duration_ms: Optional[int] = None
    ):
        self.step_name = step_name
        self.step_type = step_type
        self.status = status
        self.request_data = request_data
        self.response_data = response_data
        self.assertions_result = assertions_result
        self.error_message = error_message
        self.duration_ms = duration_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_name": self.step_name,
            "step_type": self.step_type,
            "status": self.status,
            "request_data": self.request_data,
            "response_data": self.response_data,
            "assertions_result": self.assertions_result,
            "error_message": self.error_message,
            "duration_ms": self.duration_ms
        }


class LinearExecutor:
    """线性执行器，按顺序执行步骤"""

    def __init__(self):
        self.renderer = VariableRenderer()
        self.request_builder = RequestBuilder(self.renderer)
        self.assertion_engine = AssertionEngine()
        self.script_executor = ScriptExecutor()
        self.variables: Dict[str, Any] = {}
        self.step_results: List[StepResult] = []

    def set_global_variables(self, variables: Dict[str, Any]):
        """设置全局变量"""
        self.variables = variables
        self.renderer.variables = variables

    def set_variable(self, key: str, value: Any):
        """设置变量"""
        self.variables[key] = value
        self.renderer.set_variable(key, value)

    async def execute_step(
        self,
        step_type: str,
        step_config: Dict[str, Any],
        assertions: Optional[List[Dict[str, Any]]] = None
    ) -> StepResult:
        """执行单个步骤"""
        start_time = datetime.now()

        try:
            if step_type == "api":
                result = await self._execute_api_step(step_config)
            elif step_type == "case":
                result = await self._execute_case_step(step_config)
            else:
                result = StepResult(
                    step_name=step_config.get("name", "Unknown"),
                    step_type=step_type,
                    status="skipped",
                    error_message=f"Unknown step type: {step_type}"
                )

            # 执行后置脚本
            if step_config.get("post_script"):
                post_result = await self.script_executor.execute_async(step_config["post_script"])
                context = self.script_executor.get_context()
                if context.get("variables"):
                    for k, v in context["variables"].items():
                        self.set_variable(k, v)

            # 执行断言
            if assertions and result.status == "passed":
                assertions_result = AssertionEngine.evaluate_all(assertions, result.response_data or {})
                result.assertions_result = assertions_result
                if any(not ar["passed"] for ar in assertions_result):
                    result.status = "failed"

            end_time = datetime.now()
            result.duration_ms = int((end_time - start_time).total_seconds() * 1000)

            return result

        except Exception as e:
            return StepResult(
                step_name=step_config.get("name", "Unknown"),
                step_type=step_type,
                status="failed",
                error_message=str(e),
                duration_ms=int((datetime.now() - start_time).total_seconds() * 1000)
            )

    async def _execute_api_step(self, api_config: Dict[str, Any]) -> StepResult:
        """执行 API 步骤"""
        method = api_config.get("method", "GET").upper()
        url = api_config.get("url", api_config.get("path", ""))
        headers = api_config.get("headers", [])
        params = api_config.get("params", [])
        body = api_config.get("body")
        body_type = api_config.get("body_type", "none")

        # 构建请求
        request_config = await self.request_builder.build_request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            body=body,
            body_type=body_type
        )

        # 执行前置脚本
        if api_config.get("pre_script"):
            self.script_executor.set_context(self.variables, request_config, None)
            pre_result = await self.script_executor.execute_async(api_config["pre_script"])
            context = self.script_executor.get_context()
            if context.get("variables"):
                for k, v in context["variables"].items():
                    self.set_variable(k, v)

        # 执行请求
        response = await self.request_builder.execute_request(request_config)

        # 提取响应变量
        extract_rules = api_config.get("extract_variables", [])
        for rule in extract_rules:
            path = rule.get("path", "")
            var_name = rule.get("variable", "")
            if path and var_name:
                value = self._extract_json_path(response, path)
                if value is not None:
                    self.set_variable(var_name, value)

        status = "passed" if response.get("status_code", 0) < 400 else "failed"

        return StepResult(
            step_name=api_config.get("name", "API Request"),
            step_type="api",
            status=status,
            request_data=request_config,
            response_data=response
        )

    async def _execute_case_step(self, case_config: Dict[str, Any]) -> StepResult:
        """执行测试用例步骤"""
        # 测试用例步骤与其他步骤类似，简化处理
        return await self._execute_api_step(case_config)

    def _extract_json_path(self, data: Dict[str, Any], path: str) -> Any:
        """提取 JSONPath 值"""
        return AssertionEngine._extract_json_path(data, path)


class ExecutionEngine:
    """图执行器，支持步骤依赖和拓扑排序（未启用）"""

    def __init__(self):
        self.executor = LinearExecutor()
        self.dependency_graph: Dict[str, List[str]] = {}

    def add_step_dependency(self, step_id: str, depends_on: List[str]):
        """添加步骤依赖"""
        self.dependency_graph[step_id] = depends_on

    def topological_sort(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """拓扑排序"""
        # 实现拓扑排序算法
        in_degree = {step["id"]: 0 for step in steps}
        graph = {step["id"]: [] for step in steps}

        for step in steps:
            for dep in self.dependency_graph.get(step["id"], []):
                graph[dep].append(step["id"])
                in_degree[step["id"]] += 1

        queue = [step_id for step_id, degree in in_degree.items() if degree == 0]
        sorted_steps = []

        while queue:
            current = queue.pop(0)
            sorted_steps.append(current)
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return sorted_steps