import ast
import asyncio
from typing import Any, Dict, Optional, Callable


class ScriptExecutor:
    """预/后执行脚本处理器"""

    def __init__(self):
        self._globals: Dict[str, Any] = {}
        self._locals: Dict[str, Any] = {}

    def set_context(self, variables: Dict[str, Any], request_data: Optional[Dict[str, Any]] = None, response_data: Optional[Dict[str, Any]] = None):
        """设置执行上下文"""
        self._globals = {
            "variables": variables,
            "request": request_data or {},
            "response": response_data or {},
            "console": [],
        }
        self._locals = {}

    def get_context(self) -> Dict[str, Any]:
        """获取执行上下文"""
        return {
            "variables": self._globals.get("variables", {}),
            "console": self._globals.get("console", []),
        }

    async def execute(self, script: str) -> Dict[str, Any]:
        """执行 Python 脚本"""
        if not script or not script.strip():
            return {"success": True, "output": None, "error": None}

        try:
            # 解析脚本
            tree = ast.parse(script, mode="exec")

            # 创建安全的执行环境
            safe_globals = {
                "__builtins__": {
                    "print": lambda *args: self._globals["console"].append(" ".join(str(a) for a in args)),
                    "len": len,
                    "str": str,
                    "int": int,
                    "float": float,
                    "bool": bool,
                    "list": list,
                    "dict": dict,
                    "tuple": tuple,
                    "set": set,
                    "range": range,
                    "enumerate": enumerate,
                    "zip": zip,
                    "map": map,
                    "filter": filter,
                    "sorted": sorted,
                    "reversed": reversed,
                    "any": any,
                    "all": all,
                    "abs": abs,
                    "min": min,
                    "max": max,
                    "sum": sum,
                    "round": round,
                    "isinstance": isinstance,
                    "type": type,
                },
                "variables": self._globals.get("variables", {}),
                "request": self._globals.get("request", {}),
                "response": self._globals.get("response", {}),
                "console": self._globals["console"],
            }

            safe_locals = {}

            # 执行脚本
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    # 捕获变量赋值
                    exec(compile(ast.Expression(node.value), "<string>", "eval"), safe_globals, safe_locals)
                else:
                    exec(compile(ast.Module([node], []), "<string>", "exec"), safe_globals, safe_locals)

            # 更新变量
            if "variables" in safe_globals:
                self._globals["variables"] = safe_globals["variables"]

            return {
                "success": True,
                "output": "\n".join(safe_globals["console"]) if safe_globals["console"] else None,
                "error": None
            }

        except SyntaxError as e:
            return {
                "success": False,
                "output": None,
                "error": f"Syntax error: {e}"
            }
        except Exception as e:
            return {
                "success": False,
                "output": None,
                "error": f"Runtime error: {str(e)}"
            }

    async def execute_async(self, script: str) -> Dict[str, Any]:
        """异步执行脚本（用于支持 async 语法）"""
        # 目前简化为同步执行
        return await self.execute(script)

    def extract_variable(self, script: str, key: str) -> Any:
        """从脚本提取特定变量"""
        try:
            tree = ast.parse(script, mode="exec")
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == key:
                            if isinstance(node.value, ast.Constant):
                                return node.value.value
            return None
        except Exception:
            return None