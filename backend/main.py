from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Settings

settings = Settings()
app = FastAPI(name=settings.app_name)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/")
async def root():
    return {"message": f"Hello World, this is {settings.app_name}! and we are running in {settings.ENVIRONMENT} environment."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.port)