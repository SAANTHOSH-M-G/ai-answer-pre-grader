import requests
import json


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:8b"


def structure_answers(ocr_text, question_list):

    questions_text = "\n".join(
        f"Q{q['number']}: {q['question']}"
        for q in question_list
    )

    prompt = f"""
You are an AI assistant that structures OCR text from a
handwritten student examination answer sheet.

Your job is ONLY to:
1. Identify each student's answer.
2. Separate answers according to the known questions.
3. Remove question headings.
4. Repair obvious OCR corruption.

You MUST NOT grade the answer.

You MUST NOT assign marks.

You MUST NOT add new knowledge.

KNOWN EXAM QUESTIONS:

{questions_text}

RAW OCR TEXT:

{ocr_text}


============================================================
OCR REPAIR RULES
============================================================

OCR can accidentally remove short words.

For example, OCR may produce:

"Authentication is the of verifying the identity of user or"

The intended sentence is clearly:

"Authentication is the process of verifying the identity of a user or system."

In this situation you MUST repair the obvious missing words:

- "process"
- "a"
- "system"

because the surrounding sentence clearly supports them.

Another example:

OCR:
"Authorization is the of determining what an authenticated user or
is allowed to access or perform."

Repair to:

"Authorization is the process of determining what an authenticated
user or system is allowed to access or perform."

You may repair:

- missing short words
- obvious OCR word omissions
- obvious OCR spelling errors
- broken words

BUT ONLY when the intended wording is strongly supported by
the surrounding text.

============================================================
STRICT NO-INVENTION RULE
============================================================

Do NOT add:

- new concepts
- new examples
- new explanations
- new facts
- new arguments
- information from the teacher's answer key

You may repair OCR corruption.

You may NOT improve the student's answer.

You may NOT make the student's answer more complete.

The answer must remain faithful to what the student actually wrote.

============================================================
TASK
============================================================

1. Identify which question each answer belongs to.
2. Extract ONLY the student's answer.
3. Remove question text.
4. Remove headings such as:
   Q1
   Question 1
   Ans
   Answer
5. Repair obvious OCR corruption.
6. Preserve the student's meaning.
7. Do not grade the answer.

============================================================
CONFIDENCE
============================================================

Confidence represents confidence that the extracted answer
belongs to the identified question.

0.90 - 1.00 = very clear
0.70 - 0.89 = reasonably clear
0.40 - 0.69 = uncertain
0.00 - 0.39 = very uncertain

If the answer clearly belongs to the question,
confidence should normally be 0.90 or higher.

============================================================
FINAL CHECK BEFORE OUTPUT
============================================================

Before returning the JSON:

For each answer, check:

1. Did OCR obviously remove a short word?
2. Can that word be restored from the surrounding sentence?
3. Did you accidentally add information that the student did not write?
4. Did you accidentally grade the answer?

Repair only obvious OCR corruption.

============================================================
OUTPUT
============================================================

Return ONLY valid JSON.

Use exactly:

{{
    "answers": [
        {{
            "question_number": 1,
            "answer": "student answer",
            "confidence": 0.95
        }}
    ]
}}

IMPORTANT:

- confidence MUST be a number between 0.0 and 1.0.
- Do not use null.
- Do not use an empty string.
- Do not put confidence inside the answer.
- Do not grade the answer.
- Do not assign marks.
- Do not include rubric information.
"""


    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0
        }
    }


    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )

    response.raise_for_status()

    data = response.json()

    content = data["message"]["content"]

    result = json.loads(content)


    if "answers" not in result:
        result["answers"] = []


    # ========================================================
    # SAFETY CHECK FOR ANSWER CONFIDENCE
    # ========================================================

    for answer in result["answers"]:

        confidence = answer.get(
            "confidence",
            None
        )

        try:
            confidence = float(confidence)

        except:
            confidence = None


        if confidence is None:

            if answer.get(
                "answer",
                ""
            ).strip():

                confidence = 0.70

            else:

                confidence = 0.0


        confidence = max(
            0.0,
            min(
                1.0,
                confidence
            )
        )

        answer["confidence"] = confidence


    return result
