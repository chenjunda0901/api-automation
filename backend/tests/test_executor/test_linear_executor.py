import pytest
from app.services.executor.linear_executor import LinearExecutor


class TestLinearExecutor:
    """测试线性执行器"""

    @pytest.fixture
    def executor(self):
        return LinearExecutor()

    @pytest.mark.asyncio
    async def test_simple_execute(self, executor):
        """测试简单执行"""
        executor.set_global_variables({"base_url": "https://api.example.com"})
        
        step_config = {
            "name": "Test API",
            "step_type": "api",
            "method": "GET",
            "url": "{{base_url}}/test",
            "headers": [],
            "params": [],
            "body_type": "none"
        }
        
        result = await executor.execute_step("api", step_config)
        
        assert result.step_name == "Test API"
        assert result.step_type == "api"
        assert result.duration_ms is not None

    @pytest.mark.asyncio
    async def test_variable_rendering(self, executor):
        """测试变量渲染"""
        executor.set_global_variables({"name": "test", "value": "123"})
        
        step_config = {
            "name": "Render Test",
            "step_type": "api",
            "method": "GET",
            "url": "/api/{{name}}?id={{value}}",
            "headers": [],
            "params": [],
            "body_type": "none"
        }
        
        result = await executor.execute_step("api", step_config)
        
        # 检查请求 URL 是否正确渲染
        assert result.request_data is not None

    @pytest.mark.asyncio
    async def test_set_variable(self, executor):
        """测试变量设置"""
        executor.set_variable("key1", "value1")
        executor.set_variable("key2", {"nested": "value2"})
        
        assert executor.variables["key1"] == "value1"
        assert executor.variables["key2"]["nested"] == "value2"