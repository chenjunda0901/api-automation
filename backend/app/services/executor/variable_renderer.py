import re
from typing import Any, Dict, Optional


class VariableRenderer:
    """变量渲染器，支持 {{variable}} 和 {{a.b.c}} 点号路径"""

    MAX_DEPTH = 10  # 循环引用保护

    def __init__(self, variables: Optional[Dict[str, Any]] = None):
        self.variables = variables or {}
        self._render_cache: Dict[str, Any] = {}

    def set_variable(self, key: str, value: Any):
        """设置变量"""
        self.variables[key] = value

    def get_variable(self, path: str) -> Any:
        """获取变量，支持点号路径"""
        parts = path.split(".")
        value = self.variables

        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            elif isinstance(value, list) and part.isdigit():
                idx = int(part)
                value = value[idx] if idx < len(value) else None
            else:
                return None

        return value

    def render_string(self, text: str, depth: int = 0) -> str:
        """渲染字符串中的变量"""
        if depth > self.MAX_DEPTH:
            return text  # 超过最大深度，返回原字符串

        pattern = r'\{\{([^}]+)\}\}'

        def replacer(match):
            var_path = match.group(1).strip()
            value = self.get_variable(var_path)
            if value is None:
                return match.group(0)  # 变量不存在，保留原样
            return str(value)

        result = re.sub(pattern, replacer, text)
        # 递归渲染，处理嵌套变量
        if result != text:
            return self.render_string(result, depth + 1)
        return result

    def render_dict(self, data: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
        """渲染字典中的变量"""
        if depth > self.MAX_DEPTH:
            return data

        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self.render_string(value, depth)
            elif isinstance(value, dict):
                result[key] = self.render_dict(value, depth + 1)
            elif isinstance(value, list):
                result[key] = self.render_list(value, depth + 1)
            else:
                result[key] = value

        return result

    def render_list(self, data: list, depth: int = 0) -> list:
        """渲染列表中的变量"""
        result = []
        for item in data:
            if isinstance(item, str):
                result.append(self.render_string(item, depth))
            elif isinstance(item, dict):
                result.append(self.render_dict(item, depth + 1))
            elif isinstance(item, list):
                result.append(self.render_list(item, depth + 1))
            else:
                result.append(item)
        return result

    def render(self, data: Any, depth: int = 0) -> Any:
        """通用渲染方法"""
        if isinstance(data, str):
            return self.render_string(data, depth)
        elif isinstance(data, dict):
            return self.render_dict(data, depth)
        elif isinstance(data, list):
            return self.render_list(data, depth)
        return data