from fastapi import Request, status
from fastapi.responses import JSONResponse

class ErrorHandler:
    async def __call__(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            # Log the error here
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": str(e),
                    "status": "error"
                }
            ) 