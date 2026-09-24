import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:8b"


def evaluate_answer(
    question,
    student_answer,
    answer_key,
    rubric,
    max_marks
):

    prompt = f"""
You are an AI-assisted examination pre-grader.

Your task is to evaluate a student's answer STRICTLY against
the teacher's answer key and marking rubric.

IMPORTANT GRADING RULES:

1. This is a SUGGESTED score, not a final score.
2. The teacher's rubric is the ONLY marking standard.
3. Evaluate EVERY rubric criterion separately.
4. A criterion must receive marks ONLY when the student's answer
   provides sufficient evidence that the required concept is understood.
5. DO NOT award marks merely because the student mentions the
   name or keyword of a concept.
6. If a concept is only mentioned but not explained when the
   rubric requires an explanation, award 0 marks for that criterion.
7. Equivalent wording is acceptable if it clearly communicates
   the same meaning as the answer key.
8. Minor spelling, grammar, or wording errors should NOT reduce marks
   when the intended concept is clearly understandable.
9. Do not invent information that is not present in the student's answer.
10. Do not assume that an omitted explanation is present.
11. Each criterion must be supported by evidence from the student's answer.
12. The total suggested score MUST NOT exceed the maximum marks.
13. If the answer is unclear or there is insufficient evidence to
    confidently evaluate a criterion, consider manual review.
14. Return ONLY valid JSON.
15. Confidence must be between 0.0 and 1.0.

QUESTION:
{question}

TEACHER ANSWER KEY:
{answer_key}

TEACHER RUBRIC:
{rubric}

STUDENT ANSWER:
{student_answer}

MAXIMUM MARKS:
{max_marks}

Before producing the final JSON, reason internally about each
rubric criterion.

For EVERY criterion ask:

- What does the rubric require?
- What evidence does the student's answer provide?
- Does the evidence actually demonstrate the concept?
- Is the student merely mentioning the keyword?
- How many marks does the rubric justify?

Return EXACTLY this JSON structure:

{{
    "suggested_score": 0,
    "maximum_score": {max_marks},
    "confidence": 0.0,
    "criteria": [
        {{
            "name": "criterion name",
            "max_marks": 0,
            "awarded_marks": 0,
            "evidence": "Explain specifically what evidence in the student's answer supports or fails to support the mark."
        }}
    ],
    "missing_concepts": [],
    "manual_review": false,
    "reason": "Short explanation of the overall grading decision."
}}
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

    # --------------------------------------------------
    # SAFETY CHECKS
    # --------------------------------------------------

    confidence = result.get("confidence", 0)

    try:
        confidence = float(confidence)
    except:
        confidence = 0.0

    confidence = max(0.0, min(1.0, confidence))

    result["confidence"] = confidence

    # Calculate score from rubric criteria
    calculated_score = sum(
        float(c.get("awarded_marks", 0))
        for c in result.get("criteria", [])
    )

    # Never exceed maximum marks
    calculated_score = min(
        calculated_score,
        float(max_marks)
    )

    result["suggested_score"] = calculated_score

    # Low confidence requires teacher review
    if confidence < 0.70:
        result["manual_review"] = True

    # If the model itself requests review, preserve it
    if result.get("manual_review", False):
        result["manual_review"] = True

    return result
