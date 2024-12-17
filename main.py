from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from router import education_router, employment_router, courses_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База реди")
    yield
    print("Выкл")



app = FastAPI(lifespan=lifespan)

app.include_router(courses_router)
app.include_router(education_router)
app.include_router(employment_router)




