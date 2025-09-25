from enum import Enum


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    TRUE_FALSE = "TRUE_FALSE"
    SINGLE_CHOICE = "SINGLE_CHOICE"
