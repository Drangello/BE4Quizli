def create_dummy_questions():
    """
    Return 10 dummy questions.
    """

    questions = []

    for number in range(1, 11):
        questions.append(
            {
                "question_title": f"Question {number}",
                "question_options": [
                    "Option A",
                    "Option B",
                    "Option C",
                    "Option D",
                ],
                "answer": "Option A",
            }
        )

    return questions