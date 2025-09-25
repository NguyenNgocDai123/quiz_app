import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    ForeignKey,
    Text,
    TIMESTAMP,
    Enum as PgEnum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.constants.enums.roles import RoleEnum
from app.constants.enums.questionType import QuestionType


# Users
class AppUser(Base):
    __tablename__ = "app_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(PgEnum(RoleEnum), nullable=False, default=RoleEnum.USER)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True)

    courses = relationship("Course", back_populates="teacher")
    enrollments = relationship("CourseEnrollment", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")


# Courses
class Course(Base):
    __tablename__ = "courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    teacher_id = Column(
        UUID(as_uuid=True), ForeignKey("app_users.id", ondelete="SET NULL")
    )
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    teacher = relationship("AppUser", back_populates="courses")
    enrollments = relationship("CourseEnrollment", back_populates="course")
    quizzes = relationship("CourseQuiz", back_populates="course")


# Course Enrollments
class CourseEnrollment(Base):
    __tablename__ = "course_enrollments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(
        UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("app_users.id", ondelete="CASCADE"),
        nullable=False,
    )
    joined_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    course = relationship("Course", back_populates="enrollments")
    user = relationship("AppUser", back_populates="enrollments")


# Course Quizzes
class CourseQuiz(Base):
    __tablename__ = "course_quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    course_id = Column(
        UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False
    )
    teacher_id = Column(
        UUID(as_uuid=True), ForeignKey("app_users.id", ondelete="SET NULL")
    )
    time_limit = Column(Integer)
    max_attempts = Column(Integer)
    total_points = Column(Integer)
    is_published = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    course = relationship("Course", back_populates="quizzes")
    teacher = relationship("AppUser")
    questions = relationship("QuizQuestion", back_populates="quiz")
    attempts = relationship("QuizAttempt", back_populates="quiz")


# Quiz Questions
class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quiz_id = Column(
        UUID(as_uuid=True),
        ForeignKey("course_quizzes.id", ondelete="CASCADE"),
        nullable=False,
    )
    content = Column(Text, nullable=False)
    type = Column(
        PgEnum(QuestionType), nullable=False,
        default=QuestionType.SINGLE_CHOICE
    )
    points = Column(Integer, nullable=False)

    quiz = relationship("CourseQuiz", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question")
    answers = relationship("QuizAttemptAnswer", back_populates="question")


# Question Options
class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(
        UUID(as_uuid=True),
        ForeignKey("quiz_questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    content = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)

    question = relationship("QuizQuestion", back_populates="options")
    answers = relationship("QuizAttemptAnswer", back_populates="option")


# Quiz Attempts
class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("app_users.id", ondelete="CASCADE"),
        nullable=False,
    )
    quiz_id = Column(
        UUID(as_uuid=True),
        ForeignKey("course_quizzes.id", ondelete="CASCADE"),
        nullable=False,
    )
    attempt_number = Column(Integer, nullable=False)
    score = Column(Integer)
    started_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    finished_at = Column(TIMESTAMP)

    user = relationship("AppUser", back_populates="quiz_attempts")
    quiz = relationship("CourseQuiz", back_populates="attempts")
    answers = relationship("QuizAttemptAnswer", back_populates="attempt")


# Quiz Attempt Answers
class QuizAttemptAnswer(Base):
    __tablename__ = "quiz_attempt_answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attempt_id = Column(
        UUID(as_uuid=True),
        ForeignKey("quiz_attempts.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_id = Column(
        UUID(as_uuid=True),
        ForeignKey("quiz_questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    option_id = Column(UUID(as_uuid=True), ForeignKey("question_options.id"))
    is_correct = Column(Boolean)
    score = Column(Integer, default=0)

    attempt = relationship("QuizAttempt", back_populates="answers")
    question = relationship("QuizQuestion", back_populates="answers")
    option = relationship("QuestionOption", back_populates="answers")
