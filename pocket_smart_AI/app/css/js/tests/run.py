"""
PocketSmartAI application runner.

Run the application with:

    python run.py

The FastAPI application will be available at:

    http://127.0.0.1:8000
"""

import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )