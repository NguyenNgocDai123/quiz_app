import pdfplumber
from typing import List, Dict
import app.constants.enums.questionType as QuestionType


def parse_pdf_to_questions(file_path: str) -> List[Dict]:
    questions = []
    text = ""

    # Đọc toàn bộ text từ PDF
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Tách các block theo "Câu"
    blocks = text.split("Câu ")
    for block in blocks[1:]:
        lines = [
            line.strip() for line in block.strip().split("\n") if line.strip()
        ]
        if not lines:
            continue

        # Câu hỏi nằm sau dấu ":"
        question_content = lines[0].split(":", 1)[-1].strip()

        options = []
        correct_answer = None

        for line in lines[1:]:
            if line.startswith("Đáp án"):
                correct_answer = line.split(":")[-1].strip().upper()
            elif len(line) > 2 and line[1] == ".":
                # Ví dụ: "A. Hà Nội"
                label = line[0].upper()
                opt_content = line[2:].strip()
                options.append(
                    {
                        "content": opt_content,
                        "label": label,
                        "is_correct": False,  # sẽ set đúng sau
                    }
                )

        # Set đáp án đúng
        if correct_answer:
            for opt in options:
                if opt["label"] == correct_answer:
                    opt["is_correct"] = True

        questions.append(
            {
                "content": question_content,
                "type": QuestionType.SINGLE_CHOICE,
                "points": 1,
                "options": [
                    {"content": o["content"], "is_correct": o["is_correct"]}
                    for o in options
                ],
            }
        )

    return questions
