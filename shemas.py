from typing import Optional
from pydantic import BaseModel, ConfigDict

class SCourseAdd(BaseModel):
    course_name: str
    description: Optional[str] = None
    reference: str
    hours_count: int

class SCourse(SCourseAdd):
    course_id: int
    model_config = ConfigDict(from_attributes=True)

class SCourseId(BaseModel):
    course_id: int



class SEmployeeAdd(BaseModel):
    name: str
    age: int

class SEmployee(SEmployeeAdd):
    employee_id: int
    model_config = ConfigDict(from_attributes=True)

class SEmployeeId(BaseModel):
    employee_id: int




class SNewCourseforEmplAdd(BaseModel):
    course_id: int
    employee_id: int

class SNewCourseforEmpl(SNewCourseforEmplAdd):
    empl_course_id: int

class SNewCourseforEmplId(BaseModel):
    empl_course_id: int


class SEmployeeCoursesProgress(BaseModel):
    course_id: Optional[int]
    employee_id: Optional[int]
    progress: int
    model_config = ConfigDict(from_attributes=True)


class SSetProgressAdd(BaseModel):
    course_id: int
    employee_id: int
    new_progress: int

class SSetProgress(BaseModel):
    progress: int
    model_config = ConfigDict(from_attributes=True)

class SInfo(BaseModel):
    course_id: int
    course_name: str
    description: Optional[str] = None
    hours_count: int
    employee_id: int
    name: str
    age: int
    progress: int
    model_config = ConfigDict(from_attributes=True)