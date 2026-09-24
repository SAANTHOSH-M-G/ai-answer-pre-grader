from parser import structure_answers


ocr_text = """
Q1 Explain the CIA Triad in information security.

Ans:
The CIA Triad consists of three important principles
in information security: Confidentiality, Integrity
and Availability.

Confidentiality means protecting information from
unauthorized access.

Integrity ensures that information is accurate and
not altered without permission.

Availability means authorized users can access the
information when needed.

Q2 Explain the difference between Authentication
and Authorization.

Ans:
Authentication means checking the identity of a user.

Authorization decides what an authenticated user is
allowed to access or do.

Authentication uses passwords and OTPs.
Authorization uses roles and permissions.

Q3 What is a firewall?

Ans:
A firewall is a security system that controls
network traffic. It can block unauthorized traffic.
"""


question_list = [
    {
        "number": 1,
        "question": "Explain the CIA Triad in information security."
    },
    {
        "number": 2,
        "question": "Explain the difference between Authentication and Authorization."
    },
    {
        "number": 3,
        "question": "What is a firewall? Explain its purpose and how it protects a network."
    }
]


result = structure_answers(
    ocr_text,
    question_list
)


print("\n========== STRUCTURED ANSWERS ==========\n")

for answer in result["answers"]:

    print(
        f"Q{answer['question_number']}"
    )

    print(
        f"Confidence: "
        f"{answer['confidence'] * 100:.1f}%"
    )

    print("Answer:")

    print(answer["answer"])

    print("\n" + "-" * 50)