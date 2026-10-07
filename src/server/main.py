"""
Main module for the file transfer app
"""

import uvicorn
from fastapi import FastAPI
from nicegui import ui

from server.frontend import pages
from server.routes import fts, generic

app = FastAPI()


def configure_routing():
    """Configures the routes for the app"""
    app.include_router(generic.router, tags=["Generic"])
    app.include_router(fts.router, tags=["File Transfer"])


configure_routing()

ui.run_with(app=app, title="File Transfer")

if __name__ == "__main__":
    uvicorn.run("server.main:app", host="127.0.0.1", port=8000, reload=False)
