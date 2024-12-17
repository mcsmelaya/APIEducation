from typing import Annotated

from fastapi import APIRouter, Depends

from repository import Employment, Course, Education

from shemas import SCourse, SCourseAdd, SCourseId, SEmployee, SEmployeeAdd, SEmployeeId, \
    SNewCourseforEmplAdd, SNewCourseforEmplId, SSetProgressAdd, SInfo, SSetProgress, SEmployeeCoursesProgress

courses_router = APIRouter(prefix="/course", tags=["Курсы"])
employment_router = APIRouter(prefix="/employee", tags=["Сотрудники"])
education_router = APIRouter(prefix="/education", tags=["Обучение"])

@courses_router.post("")
async def add_course(
    course: Annotated[SCourseAdd, Depends()],
) -> SCourseId:
    course_id = await Course.add_course(course)
    return {"course_id": course_id}

@courses_router.get("")
async def get_course() -> list[SCourse]:
    courses = await Course.get_all_courses()
    return courses

@courses_router.delete("")
async def delete_course(
        course_id: int
):
    await Course.delete_course(course_id)
    return {"message": "Обучение успешно удалено"}

@courses_router.put("")
async def update_course_info(
    course: Annotated[SCourse, Depends()],
) -> SCourse:
    courses = await Course.update_course_info(course)
    return courses

@education_router.patch("")
async def set_progress(
    progress: Annotated[SSetProgressAdd, Depends()]
) -> SSetProgress:
    new_progress = await Course.set_progress(progress)
    return new_progress

@education_router.post("")
async def add_course_for_employee(
    empl_course: Annotated[SNewCourseforEmplAdd, Depends()],
) -> SNewCourseforEmplId:
    empl_course_id = await Course.add_course_for_employee(empl_course)
    return {"empl_course_id": empl_course_id}

@employment_router.post("")
async def add_employee(
    employee: Annotated[SEmployeeAdd, Depends()],
) -> SEmployeeId:
    employee_id = await Employment.add_employee(employee)
    return {"employee_id": employee_id}

@employment_router.delete("")
async def delete_employee(
        employee_id: int
):
    await Employment.delete_employee(employee_id)
    return {"message": "Сотрудник успешно удален!"}

@employment_router.get("")
async def get_employees() -> list[SEmployee]:
    employees = await Employment.get_employees()
    return employees

@education_router.get("/progress")
async def get_employee_progress(employee_id: int = None, course_id: int = None) -> list[SEmployeeCoursesProgress]:
    progress = await Education.get_employee_progress(employee_id=employee_id, course_id=course_id)
    return progress

@education_router.get("/info")
async def get_all_employee_info() -> list[SInfo]:
    info = await Education.get_all_empl_info()
    return info