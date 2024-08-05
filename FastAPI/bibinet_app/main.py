from fastapi import FastAPI
import uvicorn

from routers.router import router

bibinet_app = FastAPI()

bibinet_app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("FastAPI.bibinet_app.main:bibinet_app", reload=True)
