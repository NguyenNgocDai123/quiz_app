from sqlalchemy.orm import Session
from uuid import UUID
from app.models.models import CourseQuiz, QuizQuestion, QuestionOption
from app.schemas.quiz import QuizCreate, QuizUpdate, QuestionCreate
from typing import List
import uuid


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
    db.refresh(quiz)  # cần dòng này
    return quiz


def add_questions_to_quiz(
    db: Session, quiz_id: UUID,
    questions: List[QuestionCreate]
):
    created_questions = []
    for q in questions:
        question = QuizQuestion(
            id=uuid.uuid4(),
            quiz_id=quiz_id,
            content=q.content,
            type=q.type,
            points=q.points,
        )
        db.add(question)
        db.flush()

        for opt in q.options:
            option = QuestionOption(
                id=uuid.uuid4(),
                question_id=question.id,
                content=opt.content,
                is_correct=opt.is_correct,
            )
            db.add(option)

        created_questions.append(question)

    db.commit()
    return created_questions


def repo_get_questions(db: Session, quiz_id: UUID):
    """
    Trả về query object để service xử lý tiếp (phân trang).
    """
    return db.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz_id)


def get_quiz(db: Session, quiz_id: UUID) -> CourseQuiz | None:
    return db.query(CourseQuiz).filter(CourseQuiz.id == quiz_id).first()


def list_quizzes(db: Session, course_id: UUID) -> list[CourseQuiz]:
    return db.query(CourseQuiz).filter(CourseQuiz.course_id == course_id)


def update_quiz(
    db: Session,
    quiz: CourseQuiz,
    quiz_in: QuizUpdate
) -> CourseQuiz:
    for field, value in quiz_in.dict(exclude_unset=True).items():
        setattr(quiz, field, value)
    db.commit()
    db.refresh(quiz)
    return quiz


def delete_quiz(db: Session, quiz: CourseQuiz):
    db.delete(quiz)
    db.commit()
