from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import supabase
from routers import users

app = FastAPI(
    title="Six-Figure AI Engineer API",
    description="Backend API for Six-Figure AI Engineer application",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Six-Figure AI Engineer app is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/get")
async def get_all_posts():
    try:
        result = (
            supabase.table("posts").select("*").order("created_at", desc=True).execute()
        )
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


app.include_router(users.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
