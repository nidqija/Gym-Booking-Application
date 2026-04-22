import uvicorn
from fastapi import FastAPI
from View.users import router as user_router

# main application instance
app = FastAPI(title="Gym Booking System")
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)