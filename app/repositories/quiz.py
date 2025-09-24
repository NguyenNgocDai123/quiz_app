from sqlalchemy.orm import Session
from uuid import UUID
from app.models.models import CourseQuiz
from app.schemas.quiz import QuizCreate, QuizUpdate


def create_quiz(db: Session, quiz_in: QuizCreate, teacher_id: UUID):
    quiz = CourseQuiz(
        title=quiz_in.title,
        description=quiz_in.description,
        course_id=quiz_in.course_id,
        teacher_id=teacher_id,
        time_limit=quiz_in.time_limit,
        max_attempts=quiz_in.max_attempts,
        total_points=quiz_in.total_points,
        is_published=quiz_in.is_published,
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)   # cần dòng này
    return quiz


def get_quiz(db: Session, quiz_id: UUID) -> CourseQuiz | None:
    return db.query(CourseQuiz).filter(CourseQuiz.id == quiz_id).first()


def list_quizzes(db: Session, course_id: UUID) -> list[CourseQuiz]:
    return db.query(CourseQuiz).filter(CourseQuiz.course_id == course_id)


def update_quiz(
        db: Session, quiz: CourseQuiz, quiz_in: QuizUpdate) -> CourseQuiz:
    for field, value in quiz_in.dict(exclude_unset=True).items():
        setattr(quiz, field, value)
    db.commit()
    db.refresh(quiz)
    return quiz


def delete_quiz(db: Session, quiz: CourseQuiz):
    db.delete(quiz)
    db.commit()
