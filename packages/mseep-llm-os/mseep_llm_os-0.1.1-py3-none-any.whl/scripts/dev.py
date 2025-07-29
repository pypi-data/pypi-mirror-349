import typer
from typing import Optional
import subprocess
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

app = typer.Typer()

@app.command()
def run(
    frontend: bool = True,
    backend: bool = True,
    frontend_port: Optional[int] = None,
    backend_port: Optional[int] = None,
):
    """Run the development servers"""
    # Load environment variables from .env file
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
    
    # Use environment variables or defaults for ports
    frontend_port = frontend_port or int(os.getenv('STREAMLIT_SERVER_PORT', 8501))
    backend_port = backend_port or int(os.getenv('API_SERVER_PORT', 8000))
    
    # Create a new environment with the current environment variables
    env = os.environ.copy()
    
    if frontend:
        frontend_process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "app/app.py", "--server.port", str(frontend_port)],
            env=env
        )
    
    if backend:
        backend_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "api.main:app", "--reload", "--port", str(backend_port)],
            env=env
        )
    
    try:
        if frontend:
            frontend_process.wait()
        if backend:
            backend_process.wait()
    except KeyboardInterrupt:
        if frontend:
            frontend_process.terminate()
        if backend:
            backend_process.terminate()

if __name__ == "__main__":
    app() 