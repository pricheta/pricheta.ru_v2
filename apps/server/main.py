from fastapi import FastAPI

from apps.server.resources.root import router as root_roter


DOCS_URL = '/api'

ROOT_PREFIX = ''


app = FastAPI(docs_url=DOCS_URL)
app.include_router(root_roter, prefix=ROOT_PREFIX)