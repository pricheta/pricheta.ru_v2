from fastapi import FastAPI

from apps.server.resources.auth import router as auth_router
from apps.server.resources.root import router as root_router
from apps.server.resources.users import router as users_router


DOCS_URL = "/api"

ROOT_PREFIX = ""
USERS_PREFIX = "/users"
AUTH_PREFIX = "/auth"


app = FastAPI(docs_url=DOCS_URL)
app.include_router(auth_router, prefix=AUTH_PREFIX, include_in_schema=False)
app.include_router(root_router, prefix=ROOT_PREFIX)
app.include_router(users_router, prefix=USERS_PREFIX)
