import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import manage, shell, models, settings, query, logs, hooks, packages, modules, templates, elements, memory, start  # Import the new router
from services.element_indexer import index_elements  # Import the indexing service
from models.gpt_memory import Base as GPTMemoryBase  # Import the GPTMemory model
from sqlalchemy import create_engine

# Load environment variables from .env file
load_dotenv()
print(f"DEBUG: DATABASE_URL={os.getenv('DATABASE_URL')}")  # Add this line

# Add the Django project directory to PYTHONPATH
project_dir = os.getenv("DJANGO_PROJECT_DIR", "/home/lotfikan/blogv3")
if project_dir not in sys.path:
    sys.path.append(project_dir)

# Ensure DJANGO_SETTINGS_MODULE is set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings.base")  # Replace 'mysite.settings' with your actual settings module

app = FastAPI(
    servers=[
        {"url": "https://smartapp-dd.beyond-board.me", "description": "Production server"}
    ]
)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the memory table during startup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///element_assets.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
GPTMemoryBase.metadata.create_all(bind=engine)

# Include routers
app.include_router(start.router)  # Add the start router
app.include_router(manage.router)
app.include_router(shell.router)
#app.include_router(models.router)
app.include_router(settings.router)
app.include_router(query.router)
app.include_router(logs.router)
app.include_router(hooks.router)
app.include_router(packages.router)
app.include_router(modules.router)
app.include_router(templates.router)
app.include_router(elements.router)  # Add the elements router
app.include_router(memory.router)  # Add the memory router

# Perform indexing during server startup
print("Checking if indexing is required...")
index_elements()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=1118, reload=True)