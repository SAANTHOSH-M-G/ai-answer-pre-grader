from ocr import extract_text
from parser import structure_answers


# --------------------------------------------------
# 1. IMAGE
# --------------------------------------------------

image_path = "sample_answer.jpg"


# --------------------------------------------------
# 2. KNOWN EXAM QUESTIONS
# --------------------------------------------------

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


# --------------------------------------------------
# 3. OCR
# --------------------------------------------------

print("\n========== STEP 1: OCR ==========\n")

ocr_text, ocr_confidence = extract_text(image_path)

print("Raw OCR Text:")
print(ocr_text)

print(
    f"\nOCR Confidence: "
    f"{ocr_confidence * 100:.1f}%"
)


# --------------------------------------------------
# 4. LLM ANSWER STRUCTURING
# --------------------------------------------------

print("\n========== STEP 2: AI STRUCTURING ==========\n")

result = structure_answers(
    ocr_text,
    question_list
)


# --------------------------------------------------
# 5. DISPLAY STRUCTURED ANSWERS
# --------------------------------------------------

for answer in result["answers"]:

    print(
        f"Q{answer['question_number']}"
    )

    print(
        f"Parser Confidence: "
        f"{answer['confidence'] * 100:.1f}%"
    )

    print("Student Answer:")

    print(answer["answer"])

    print("\n" + "-" * 60)