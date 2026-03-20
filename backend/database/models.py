import uuid
from sqlalchemy import Column, ForeignKey, Integer, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID, ENUM as PGENUM

from .database import Base
import enum

class RoleEnum(enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class CourseLevelEnum(enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    all_levels = "all_levels"

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    is_verified = Column(Integer, nullable=False, default=0)    

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(20))
    profile_picture = Column(String)

    role = PGENUM(RoleEnum, name="role_enum", create_type=True, nullable=False, default=RoleEnum.student)
    hashed_password = Column(String, nullable=False)
    token_version = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)

    title = Column(String(100), nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)
    course_picture = Column(String)
    level = PGENUM(CourseLevelEnum, name="course_level_enum", create_type=True, nullable=False, default=CourseLevelEnum.beginner)
    total_duration = Column(Integer, nullable=False)  # in minutes

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

class CourseUnit(Base):
    __tablename__ = "course_units"

    unit_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.course_id"), nullable=False)

    title = Column(String(100), nullable=False)
    position = Column(Integer, nullable=False)  # order of the unit in the course

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class CourseLectures(Base):
    __tablename__ = "course_lectures"

    lecture_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("course_units.unit_id"), nullable=False)

    title = Column(String(100), nullable=False)
    description = Column(String)
    video_url = Column(String, nullable=False)
    duration = Column(Integer)  # in minutes
    position = Column(Integer, nullable=False)  # order of the lecture in the unit
    is_preview = Column(Integer, nullable=False, default=0)  # 0 for False, 1 for True

    created_at = Column(DateTime, nullable=False, server_default=func.now())


class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.course_id"), nullable=False)

    enrolled_at = Column(DateTime, nullable=False, server_default=func.now())

class Rating(Base):
    __tablename__ = "ratings"

    rating_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.course_id"), nullable=False)

    rating = Column(Integer, nullable=False)  # 1 to 5
    review = Column(String)

    created_at = Column(DateTime, nullable=False, server_default=func.now())



