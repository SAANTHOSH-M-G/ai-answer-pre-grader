from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback

from ocr import extract_text
from parser import structure_answers
from grader import evaluate_answer


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "AI Answer Pre-Grader Backend is running"
    })


# ============================================================
# OCR + AI STRUCTURING
# ============================================================

@app.route("/api/process-answer-sheet", methods=["POST"])
def process_answer_sheet():

    try:

        # ----------------------------------------------------
        # Check image
        # ----------------------------------------------------

        if "image" not in request.files:
            return jsonify({
                "error": "No answer sheet image uploaded."
            }), 400

        image = request.files["image"]

        if image.filename == "":
            return jsonify({
                "error": "No image selected."
            }), 400

        # ----------------------------------------------------
        # Get questions
        # ----------------------------------------------------

        questions_json = request.form.get("questions")

        if not questions_json:
            return jsonify({
                "error": "Question data is missing."
            }), 400

        import json

        questions = json.loads(questions_json)

        # ----------------------------------------------------
        # Save image
        # ----------------------------------------------------

        image_path = os.path.join(
            UPLOAD_FOLDER,
            image.filename
        )

        image.save(image_path)

        # ----------------------------------------------------
        # STEP 1: OCR
        # ----------------------------------------------------

        print("\n========== OCR START ==========")

        ocr_text, ocr_confidence = extract_text(
            image_path
        )

        print("OCR Confidence:", ocr_confidence)

        print("\nOCR TEXT:")
        print(ocr_text)

        # ----------------------------------------------------
        # STEP 2: AI STRUCTURING
        # ----------------------------------------------------

        print("\n========== AI STRUCTURING ==========")

        structured = structure_answers(
            ocr_text,
            questions
        )

        print("\nSTRUCTURED ANSWERS:")
        print(structured)

        # ----------------------------------------------------
        # Parser confidence
        # ----------------------------------------------------

        answers = structured.get(
            "answers",
            []
        )

        if answers:

            parser_confidence = sum(
                float(
                    answer.get(
                        "confidence",
                        0
                    )
                )
                for answer in answers
            ) / len(answers)

        else:

            parser_confidence = 0.0

        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "ocr": {
                "text": ocr_text,
                "confidence": ocr_confidence
            },

            "structured_answers": answers,

            "parser_confidence": parser_confidence

        })

    except Exception as e:

        print("\nERROR:")
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================================
# RUBRIC GRADING
# ============================================================

@app.route("/api/evaluate", methods=["POST"])
def evaluate():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No evaluation data received."
            }), 400

        questions = data.get(
            "questions",
            []
        )

        structured_answers = data.get(
            "structured_answers",
            []
        )

        results = []

        # ----------------------------------------------------
        # Evaluate every question
        # ----------------------------------------------------

        for question in questions:

            question_number = question["number"]

            # Find student's answer
            student_answer = ""

            parser_confidence = 0.0

            for answer in structured_answers:

                if int(
                    answer.get(
                        "question_number",
                        -1
                    )
                ) == int(question_number):

                    student_answer = answer.get(
                        "answer",
                        ""
                    )

                    parser_confidence = float(
                        answer.get(
                            "confidence",
                            0
                        )
                    )

                    break

            print(
                f"\n========== EVALUATING Q{question_number} =========="
            )

            # ------------------------------------------------
            # AI grading
            # ------------------------------------------------

            grading_result = evaluate_answer(

                question=question["question"],

                student_answer=student_answer,

                answer_key=question["answer_key"],

                rubric=question["rubric"],

                max_marks=question["max_marks"]

            )

            # ------------------------------------------------
            # Force manual review if parser confidence low
            # ------------------------------------------------

            if parser_confidence < 0.70:

                grading_result["manual_review"] = True

                grading_result["reason"] = (
                    grading_result.get(
                        "reason",
                        ""
                    )
                    + " Low OCR/answer-structuring confidence."
                )

            # ------------------------------------------------
            # Add metadata
            # ------------------------------------------------

            result = {

                "question_number": question_number,

                "question": question["question"],

                "student_answer": student_answer,

                "parser_confidence": parser_confidence,

                "grading": grading_result

            }

            results.append(result)

        # ----------------------------------------------------
        # Calculate total
        # ----------------------------------------------------

        ai_total = sum(

            float(
                result["grading"].get(
                    "suggested_score",
                    0
                )
            )

            for result in results
        )

        maximum_total = sum(

            float(
                question["max_marks"]
            )

            for question in questions
        )

        percentage = (

            (ai_total / maximum_total) * 100

            if maximum_total > 0

            else 0
        )

        manual_review_count = sum(

            1

            for result in results

            if result["grading"].get(
                "manual_review",
                False
            )
        )

        # ----------------------------------------------------
        # Final response
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "results": results,

            "summary": {

                "ai_total": ai_total,

                "maximum_total": maximum_total,

                "percentage": percentage,

                "manual_review_count":
                    manual_review_count

            }

        })

    except Exception as e:

        print("\nERROR:")
        traceback.print_exc()

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# SERVER
# ============================================================

if __name__ == "__main__":

    print("\n======================================")
    print(" AI ANSWER PRE-GRADER BACKEND")
    print("======================================")
    print("Server: http://127.0.0.1:5000")
    print("======================================\n")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
