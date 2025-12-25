from fastapi import FastAPI

from apps.server.resources.root import router as root_router
from apps.server.resources.users import router as users_router

DOCS_URL = "/api"

ROOT_PREFIX = ""
USERS_PREFIX = "/users"


app = FastAPI(docs_url=DOCS_URL)
app.include_router(root_router, prefix=ROOT_PREFIX)
app.include_router(users_router, prefix=USERS_PREFIX)
