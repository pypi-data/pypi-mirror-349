"""
Main entry point for the LYRAIOS API server.
"""

import uvicorn

from app.api.main import app


def main():
    """Run the API server."""
    uvicorn.run(
        "app.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main() 