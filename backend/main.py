from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Settings
from auth.auth import router as auth_router 

settings = Settings()
app = FastAPI(name=settings.app_name)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api_route = "/api/v1"

app.include_router(auth_router, prefix=api_route, tags=["auth"])

@app.get("/")
async def root():
    return {"message": f"Hello World, this is {settings.app_name}! and we are running in {settings.ENVIRONMENT} environment."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.port)