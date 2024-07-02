from fastapi import HTTPException
def exception(code: int, detail: str):
    """
    根据提供的 code 和 detail 抛出一个 HTTP 异常。
    """
    raise HTTPException(status_code=code, detail=detail)
