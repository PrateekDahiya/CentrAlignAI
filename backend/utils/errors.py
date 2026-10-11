"""Error types only."""
class ToolError(Exception):
    pass


class RetryableError(ToolError):
    pass


class FatalError(ToolError):
    pass
