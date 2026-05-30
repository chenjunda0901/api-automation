import os
import httpx
from typing import Any, Dict, List, Optional, Tuple
from app.services.executor.variable_renderer import VariableRenderer


class RequestBuilder:
    """HTTP 请求构建器"""

    def __init__(self, renderer: VariableRenderer):
        self.renderer = renderer

    async def build_request(
        self,
        method: str,
        url: str,
        headers: Optional[List[Dict[str, Any]]] = None,
        params: Optional[List[Dict[str, Any]]] = None,
        body: Optional[Dict[str, Any]] = None,
        body_type: str = "none",
        files: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """构建 HTTP 请求"""
        # 渲染 URL
        rendered_url = self.renderer.render_string(url)

        # 渲染 headers
        rendered_headers = {}
        if headers:
            for header in headers:
                if header.get("enabled", True):
                    key = self.renderer.render_string(header.get("key", ""))
                    value = self.renderer.render_string(header.get("value", ""))
                    if key:
                        rendered_headers[key] = value

        # 渲染 params
        rendered_params = {}
        if params:
            for param in params:
                if param.get("enabled", True):
                    key = self.renderer.render_string(param.get("key", ""))
                    value = self.renderer.render_string(param.get("value", ""))
                    if key:
                        rendered_params[key] = value

        # 渲染 body
        rendered_body = None
        if body:
            if body_type == "json":
                rendered_body = self.renderer.render(body)
            elif body_type == "form":
                rendered_body = self.renderer.render_dict(body)
            elif body_type == "raw":
                if isinstance(body, dict) and "raw" in body:
                    rendered_body = self.renderer.render_string(body["raw"])
                elif isinstance(body, str):
                    rendered_body = self.renderer.render_string(body)

        return {
            "method": method.upper(),
            "url": rendered_url,
            "headers": rendered_headers,
            "params": rendered_params,
            "body": rendered_body,
            "body_type": body_type,
            "files": files
        }

    async def execute_request(self, request_config: Dict[str, Any]) -> Dict[str, Any]:
        """执行 HTTP 请求"""
        method = request_config["method"]
        url = request_config["url"]
        headers = request_config.get("headers", {})
        params = request_config.get("params", {})
        body = request_config.get("body")
        body_type = request_config.get("body_type", "none")
        files = request_config.get("files")

        timeout = httpx.Timeout(30.0, connect=10.0)

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                if method == "GET":
                    response = await client.get(url, headers=headers, params=params)
                elif method == "POST":
                    if files:
                        # 文件上传
                        files_data = self._prepare_files(files)
                        response = await client.post(url, headers=headers, data=body, files=files_data)
                    elif body_type == "json":
                        response = await client.post(url, headers=headers, json=body)
                    elif body_type == "form":
                        response = await client.post(url, headers=headers, data=body)
                    else:
                        response = await client.post(url, headers=headers, content=body)
                elif method == "PUT":
                    if body_type == "json":
                        response = await client.put(url, headers=headers, json=body)
                    else:
                        response = await client.put(url, headers=headers, content=body)
                elif method == "DELETE":
                    response = await client.delete(url, headers=headers, params=params)
                elif method == "PATCH":
                    response = await client.patch(url, headers=headers, json=body)
                else:
                    response = await client.request(method, url, headers=headers, params=params)

                return {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": response.text,
                    "json": self._try_parse_json(response.text),
                    "elapsed_ms": int(response.elapsed.total_seconds() * 1000)
                }

        except httpx.TimeoutException:
            return {
                "status_code": 0,
                "error": "Request timeout",
                "elapsed_ms": 30000
            }
        except httpx.RequestError as e:
            return {
                "status_code": 0,
                "error": str(e),
                "elapsed_ms": 0
            }

    def _try_parse_json(self, text: str) -> Optional[Dict[str, Any]]:
        """尝试解析 JSON"""
        try:
            return {"data": text}
        except Exception:
            return {"data": text}

    def _prepare_files(self, files: Dict[str, Any]) -> Dict[str, Any]:
        """准备文件上传"""
        prepared = {}
        for key, file_config in files.items():
            if isinstance(file_config, dict):
                path = file_config.get("path", "")
                # 验证文件路径，防止路径遍历攻击
                if self._validate_file_path(path):
                    filename = file_config.get("filename", os.path.basename(path))
                    prepared[key] = (filename, open(path, "rb"))
            elif isinstance(file_config, str):
                if self._validate_file_path(file_config):
                    prepared[key] = (os.path.basename(file_config), open(file_config, "rb"))
        return prepared

    def _validate_file_path(self, path: str) -> bool:
        """验证文件路径，防止路径遍历攻击"""
        # 确保路径是绝对路径且不包含 .. 
        abs_path = os.path.abspath(path)
        return ".." not in path and os.path.isfile(abs_path)