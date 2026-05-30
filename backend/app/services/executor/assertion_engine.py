import json
import re
from typing import Any, Dict, List, Optional, Tuple


class AssertionEngine:
    """断言引擎，支持 JSONPath 提取和多种比较操作"""

    def assert_equal(actual: Any, expected: Any) -> Tuple[bool, str]:
        """相等断言"""
        if actual == expected:
            return True, f"Equal: {actual}"
        return False, f"Expected {expected}, got {actual}"

    def assert_not_equal(actual: Any, expected: Any) -> Tuple[bool, str]:
        """不相等断言"""
        if actual != expected:
            return True, f"Not equal: {actual}"
        return False, f"Expected not {expected}"

    def assert_contains(container: str, item: str) -> Tuple[bool, str]:
        """包含断言"""
        if item in container:
            return True, f"Contains: '{item}'"
        return False, f"'{container}' does not contain '{item}'"

    def assert_not_contains(container: str, item: str) -> Tuple[bool, str]:
        """不包含断言"""
        if item not in container:
            return True, f"Not contains: '{item}'"
        return False, f"'{container}' contains '{item}'"

    def assert_greater(actual: float, expected: float) -> Tuple[bool, str]:
        """大于断言"""
        try:
            actual_val = float(actual)
            expected_val = float(expected)
            if actual_val > expected_val:
                return True, f"Greater: {actual_val} > {expected_val}"
            return False, f"Expected > {expected_val}, got {actual_val}"
        except (ValueError, TypeError):
            return False, f"Cannot compare non-numeric values: {actual} vs {expected}"

    def assert_less(actual: float, expected: float) -> Tuple[bool, str]:
        """小于断言"""
        try:
            actual_val = float(actual)
            expected_val = float(expected)
            if actual_val < expected_val:
                return True, f"Less: {actual_val} < {expected_val}"
            return False, f"Expected < {expected_val}, got {actual_val}"
        except (ValueError, TypeError):
            return False, f"Cannot compare non-numeric values: {actual} vs {expected}"

    def assert_in(actual: Any, expected_list: List[Any]) -> Tuple[bool, str]:
        """在列表中断言"""
        if actual in expected_list:
            return True, f"In: {actual}"
        return False, f"{actual} not in {expected_list}"

    def assert_not_in(actual: Any, expected_list: List[Any]) -> Tuple[bool, str]:
        """不在列表中断言"""
        if actual not in expected_list:
            return True, f"Not in: {actual}"
        return False, f"{actual} in {expected_list}"

    def assert_status_code(response: Dict[str, Any], expected: int) -> Tuple[bool, str]:
        """HTTP 状态码断言"""
        actual = response.get("status_code", 0)
        if actual == expected:
            return True, f"Status code: {actual}"
        return False, f"Expected status {expected}, got {actual}"

    def assert_json_path(data: Dict[str, Any], path: str, expected: Any, operator: str = "eq") -> Tuple[bool, str]:
        """JSONPath 提取断言"""
        value = AssertionEngine._extract_json_path(data, path)
        if value is None:
            return False, f"Path not found: {path}"

        operators = {
            "eq": AssertionEngine.assert_equal,
            "ne": AssertionEngine.assert_not_equal,
            "contains": lambda a, e: AssertionEngine.assert_contains(str(a), str(e)),
            "not_contains": lambda a, e: AssertionEngine.assert_not_contains(str(a), str(e)),
            "gt": AssertionEngine.assert_greater,
            "lt": AssertionEngine.assert_less,
            "in": AssertionEngine.assert_in,
            "not_in": AssertionEngine.assert_not_in,
        }

        op_func = operators.get(operator, AssertionEngine.assert_equal)
        return op_func(value, expected)

    @staticmethod
    def _extract_json_path(data: Dict[str, Any], path: str) -> Any:
        """提取 JSONPath 路径的值"""
        parts = path.replace("$.", "").replace("[", ".").replace("]", "").split(".")
        value = data

        for part in parts:
            if not part:
                continue
            if isinstance(value, dict):
                value = value.get(part)
            elif isinstance(value, list):
                try:
                    idx = int(part)
                    value = value[idx] if 0 <= idx < len(value) else None
                except ValueError:
                    return None
            else:
                return None

        return value

    @staticmethod
    def evaluate(assertion: Dict[str, Any], response: Dict[str, Any]) -> Tuple[bool, str]:
        """评估断言"""
        path = assertion.get("path", "")
        operator = assertion.get("operator", "eq")
        expected = assertion.get("expected")

        return AssertionEngine.assert_json_path(response, path, expected, operator)

    @staticmethod
    def evaluate_all(assertions: List[Dict[str, Any]], response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """评估所有断言"""
        results = []
        for assertion in assertions:
            passed, message = AssertionEngine.evaluate(assertion, response)
            results.append({
                "path": assertion.get("path"),
                "operator": assertion.get("operator"),
                "expected": assertion.get("expected"),
                "passed": passed,
                "message": message
            })
        return results