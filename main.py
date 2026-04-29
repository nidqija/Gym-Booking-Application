import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from View.router import router as user_router
from Model.database_service import DatabaseRegistryManager



@asynccontextmanager
async def lifespan(app: FastAPI):
    try :
        db_resource = DatabaseRegistryManager.get_db_resource()
        service = DatabaseRegistryManager(db_resource)
        service.migrate()
        print("Database migration completed successfully.")

    except Exception as e:
        print(f"Database migration failed: {e}")
        raise e  # re-raise the exception to prevent the app from starting
    
    yield  # this is where the app runs
    print("App is shutting down. Perform any cleanup if necessary.")



# main application instance
app = FastAPI(title="Gym Booking System", lifespan=lifespan)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)