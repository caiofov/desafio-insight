from fastapi import FastAPI

from app.routes.ibge import router as ibge_router
import uvicorn

app = FastAPI()

app.include_router(ibge_router, prefix="/ibge")


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
