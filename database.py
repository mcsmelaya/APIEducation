from sqlalchemy import CheckConstraint
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column
from typing_extensions import Optional

engine = create_async_engine(
    "sqlite+aiosqlite:///tasks.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass


class CourseOrm(Model):
    __tablename__ = "Course"

    course_id: Mapped[int] = mapped_column(primary_key=True)
    course_name: Mapped[str]
    description: Mapped[Optional[str]]
    reference: Mapped[str]
    hours_count: Mapped[int]

class Employee(Model):
    __tablename__ = "Employee"

    employee_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]


class EducationOrm(Model): #education
    __tablename__ = "Education"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[Optional[int]]
    course_id: Mapped[Optional[int]]
    progress: Mapped[int] = mapped_column(default=0)

    __table_args__ = (
        CheckConstraint('progress >= 0 AND progress <= 100', name='check_progress_range'),
    )


async  def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async  def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)