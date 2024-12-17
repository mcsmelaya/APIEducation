from sqlalchemy import select
from database import new_session, CourseOrm, Employee, EducationOrm
from shemas import SCourseAdd, SCourse, SEmployee, SEmployeeAdd, SNewCourseforEmplAdd, SInfo, SSetProgressAdd, \
    SSetProgress


class Course:
    @staticmethod
    async def add_course(data: SCourseAdd) -> int:
        async with new_session() as session:
            course_dict = data.model_dump()
            course = CourseOrm(**course_dict)
            session.add(course)
            await session.flush()
            await session.commit()
            return course.course_id

    @staticmethod
    async def get_all_courses() -> list[SCourse]:
        async with new_session() as session:
            query = select(CourseOrm)
            result = await session.execute(query)
            course_models = result.scalars().all()
            course_shemas = [SCourse.model_validate(course) for course in course_models]
            return course_shemas

    @classmethod
    async def delete_course(cls, id: int):
        async with new_session() as session:
            query = select(CourseOrm).filter_by(course_id=id)
            result = await session.execute(query)
            course = result.scalar_one()
            await session.delete(course)
            await session.commit()
            return {"message": "Курс успешно удален"}

    @staticmethod
    async def update_course_info(data: SCourse) -> SCourse:
        async with new_session() as session:
            query = select(CourseOrm).filter_by(course_id=data.course_id)
            result = await session.execute(query)
            course = result.scalar_one()
            if data.course_name:
                course.course_name = data.course_name
            if data.description:
                course.description = data.description
            await session.commit()
            return SCourse.model_validate(course)


    @staticmethod
    async def add_course_for_employee(data: SNewCourseforEmplAdd):
        async with new_session() as session:
            course_for_employee_dict = data.model_dump()
            course = EducationOrm(**course_for_employee_dict)
            session.add(course)
            await session.flush()
            await session.commit()
            return course.id



    @staticmethod
    async def set_progress(data: SSetProgressAdd) -> SSetProgress:
        async with new_session() as session:
            query = select(EducationOrm).filter_by(employee_id=data.employee_id, course_id=data.course_id)
            result = await session.execute(query)
            old_progress = result.scalar_one()
            old_progress.progress = data.new_progress
            await session.commit()
            return SSetProgress(progress=old_progress.progress)

    @staticmethod
    async def get_employee_progress_course(course_id: int, employee_id: int):
        async with new_session() as session:
            query = select(EducationOrm).filter_by(employee_id=employee_id, course_id=course_id)
            result = await session.execute(query)
            progress = result.scalars().all()
            await session.commit()
            return progress


class Employment:

    @staticmethod
    async def add_employee(data: SEmployeeAdd) -> int:
        async with new_session() as session:
            employee_dict = data.model_dump()
            employee = Employee(**employee_dict)
            session.add(employee)
            await session.flush()
            await session.commit()
            return employee.employee_id

    @staticmethod
    async def delete_employee( id: int):
        async with new_session() as session:
            query = select(Employee).filter_by(employee_id=id)
            result = await session.execute(query)
            employee = result.scalar_one()
            await session.delete(employee)
            await session.commit()
            return {"message": "Сотрудник успешно удален!"}

    @staticmethod
    async def get_employees() -> list[SEmployee]:
        async with new_session() as session:
            query = select(Employee)
            result = await session.execute(query)
            employee_models = result.scalars().all()
            employee_shemas = [SEmployee.model_validate(employee) for employee in employee_models]
            return employee_shemas


class Education:

    @staticmethod
    async def get_employee_progress(employee_id: int = None, course_id: int = None):
        async with new_session() as session:
            query = select(EducationOrm)
            if employee_id is not None:
                query = query.filter_by(employee_id=employee_id)
            if course_id is not None:
                query = query.filter_by(course_id=course_id)
            result = await session.execute(query)
            progress = result.scalars().all()
            await session.commit()
            return progress

    @staticmethod
    async def get_all_empl_info():
        async with new_session() as session:
            query = (
                select(Employee, CourseOrm, EducationOrm)
                .join(EducationOrm, EducationOrm.employee_id == Employee.employee_id)
                .join(CourseOrm, CourseOrm.course_id == EducationOrm.course_id)
            )
            result = await session.execute(query)
            rows = result.fetchall()
            empl_info_schemas = [
                SInfo(
                    course_id=row.CourseOrm.course_id,
                    course_name=row.CourseOrm.course_name,
                    description=row.CourseOrm.description,
                    hours_count=row.CourseOrm.hours_count,
                    employee_id=row.Employee.employee_id,
                    name=row.Employee.name,
                    age=row.Employee.age,
                    progress=row.EducationOrm.progress,
                )
                for row in rows
            ]
            return empl_info_schemas