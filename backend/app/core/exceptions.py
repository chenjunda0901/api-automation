class BizError(Exception):
    """业务异常基类"""
    def __init__(self, message: str, code: str = "BIZ_ERROR", status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(BizError):
    """资源未找到"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, "NOT_FOUND", 404)


class UnauthorizedError(BizError):
    """未授权"""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, "UNAUTHORIZED", 401)


class ForbiddenError(BizError):
    """禁止访问"""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, "FORBIDDEN", 403)


class ValidationError(BizError):
    """验证错误"""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, "VALIDATION_ERROR", 422)


class ConflictError(BizError):
    """资源冲突"""
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message, "CONFLICT", 409)