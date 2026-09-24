from grader import evaluate_answer


question = "Explain the CIA Triad in cybersecurity."

answer_key = """
The CIA Triad consists of:
1. Confidentiality - protecting information from unauthorized access.
2. Integrity - ensuring information remains accurate and unaltered.
3. Availability - ensuring authorized users can access information when needed.
"""

rubric = """
Confidentiality - 1 mark
Integrity - 1 mark
Availability - 1 mark
"""

student_answer = """
The CIA triad consists of confidentiality, integrity and availability.

Confidentiality protects information from unauthorized people.

Integrity makes sure the information is accurate and has not been
changed without authorization.

Availability means authorized users can access information when needed.
"""

result = evaluate_answer(
    question,
    student_answer,
    answer_key,
    rubric,
    3
)

print("\n========== AI GRADING RESULT ==========\n")

print(f"Score      : {result['suggested_score']} / {result['maximum_score']}")
print(f"Confidence : {result['confidence'] * 100:.1f}%")
print(f"Review     : {result['manual_review']}")

print("\nRubric Breakdown:")

for criterion in result["criteria"]:
    print(
        f"- {criterion['name']}: "
        f"{criterion['awarded_marks']}/{criterion['max_marks']}"
    )

print("\nMissing Concepts:")

for concept in result["missing_concepts"]:
    print(f"- {concept}")

print("\nReason:")
print(result["reason"])