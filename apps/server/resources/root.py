from fastapi import FastAPI, APIRouter


app = FastAPI()


router = APIRouter()


@router.get("/", include_in_schema=False)
async def root():
    return {"message": "Hello World"}

