from ocr import extract_text
from parser import structure_answers
from grader import evaluate_answer


# ============================================================
# 1. IMAGE
# ============================================================

image_path = "sample_answer.jpg"


# ============================================================
# 2. EXAM QUESTIONS
# ============================================================

questions = [
    {
        "number": 1,
        "question": "Explain the CIA Triad in information security.",

        "answer_key": """
The CIA Triad consists of three important principles:
Confidentiality, Integrity and Availability.

Confidentiality means protecting information from unauthorized access.

Integrity ensures that information is accurate, complete and
not altered without permission.

Availability means authorized users can access information
when needed.
""",

        "rubric": """
Confidentiality definition and explanation - 1 mark
Integrity definition and explanation - 1 mark
Availability definition and explanation - 1 mark
""",

        "max_marks": 3
    },

    {
        "number": 2,
        "question": "Explain the difference between Authentication and Authorization in cybersecurity.",

        "answer_key": """
Authentication is the process of verifying the identity of a user or system.

Authorization is the process of determining what an authenticated user
or system is allowed to access or perform.

Authentication answers "Who are you?"

Authorization answers "What are you allowed to do?"

Authentication can use passwords, biometrics, or OTPs.

Authorization can use roles and permissions.
""",

        "rubric": """
Authentication definition - 1 mark
Authorization definition - 1 mark
Correct difference between authentication and authorization - 1 mark
Authentication examples - 1 mark
Authorization examples - 1 mark
""",

        "max_marks": 5
    },

    {
        "number": 3,
        "question": "What is a firewall? Explain its purpose and how it protects a network.",

        "answer_key": """
A firewall is a network security system that monitors and controls
incoming and outgoing network traffic based on predefined security rules.

It helps prevent unauthorized access to a network.

A firewall can allow legitimate traffic and block suspicious or
unauthorized traffic.

Firewalls can be implemented as hardware, software, or cloud-based
security controls.
""",

        "rubric": """
Definition of firewall - 1 mark
Explains monitoring or filtering network traffic - 1 mark
Explains blocking unauthorized or suspicious traffic - 1 mark
Provides a valid firewall type or implementation example - 1 mark
""",

        "max_marks": 4
    }
]


# ============================================================
# 3. OCR
# ============================================================

print("\n========================================")
print("STEP 1 - HANDWRITING OCR")
print("========================================\n")

try:

    ocr_text, ocr_confidence = extract_text(
        image_path
    )

except Exception as e:

    print("OCR ERROR:")
    print(e)

    raise


print("Raw OCR Text:")
print(ocr_text)

print(
    f"\nOCR Confidence: "
    f"{ocr_confidence * 100:.1f}%"
)


# ============================================================
# 4. AI ANSWER STRUCTURING
# ============================================================

print("\n========================================")
print("STEP 2 - AI ANSWER STRUCTURING")
print("========================================\n")

structured = structure_answers(
    ocr_text,
    questions
)


for answer in structured.get("answers", []):

    print(
        f"\nQ{answer['question_number']}"
    )

    print(
        f"Parser Confidence: "
        f"{answer['confidence'] * 100:.1f}%"
    )

    print("Extracted Answer:")

    print(answer["answer"])

    print("\n" + "-" * 60)


# ============================================================
# 5. AI EVALUATION
# ============================================================

print("\n========================================")
print("STEP 3 - AI RUBRIC EVALUATION")
print("========================================\n")


total_score = 0
total_marks = 0


for parsed_answer in structured.get("answers", []):

    question_number = parsed_answer[
        "question_number"
    ]

    question_data = next(
        (
            q for q in questions
            if q["number"] == question_number
        ),
        None
    )

    if question_data is None:

        print(
            f"Q{question_number}: "
            "No matching question found."
        )

        continue


    print(
        f"\nEvaluating Q{question_number}..."
    )


    result = evaluate_answer(

        question_data["question"],

        parsed_answer["answer"],

        question_data["answer_key"],

        question_data["rubric"],

        question_data["max_marks"]
    )


    score = result["suggested_score"]

    total_score += score
    total_marks += question_data["max_marks"]


    print("\nRESULT")

    print(
        f"Score: "
        f"{score} / "
        f"{result['maximum_score']}"
    )

    print(
        f"Confidence: "
        f"{result['confidence'] * 100:.1f}%"
    )

    print(
        f"Manual Review: "
        f"{result['manual_review']}"
    )


    print("\nRubric Breakdown:")

    for criterion in result.get(
        "criteria",
        []
    ):

        print(
            f"- {criterion.get('name', 'Criterion')}: "
            f"{criterion.get('awarded_marks', 0)} / "
            f"{criterion.get('max_marks', 0)}"
        )

        print(
            f"  Evidence: "
            f"{criterion.get('evidence', '')}"
        )


    if result.get("missing_concepts"):

        print("\nMissing Concepts:")

        for concept in result[
            "missing_concepts"
        ]:

            print(
                f"- {concept}"
            )


    print("\nAI Explanation:")

    print(
        result.get(
            "reason",
            ""
        )
    )

    print("\n" + "=" * 60)


# ============================================================
# 6. FINAL TOTAL
# ============================================================

print("\n========================================")
print("FINAL AI RESULT")
print("========================================\n")

print(
    f"AI Total Score: "
    f"{total_score} / {total_marks}"
)

if total_marks > 0:

    percentage = (
        total_score / total_marks
    ) * 100

    print(
        f"AI Percentage: "
        f"{percentage:.1f}%"
    )
