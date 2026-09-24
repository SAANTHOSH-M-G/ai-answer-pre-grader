// ============================================================
// AI EXAM ANSWER PRE-GRADER
// FRONTEND JAVASCRIPT
// ============================================================

const API_URL = "http://127.0.0.1:5000";


// ============================================================
// GLOBAL STATE
// ============================================================

let questions = [];
let structuredAnswers = [];
let evaluationResults = [];


// ============================================================
// ELEMENTS
// ============================================================

const questionsContainer =
    document.getElementById("questions-container");

const addQuestionBtn =
    document.getElementById("add-question-btn");

const answerSheetInput =
    document.getElementById("answer-sheet");

const chooseFileBtn =
    document.getElementById("choose-file-btn");

const fileName =
    document.getElementById("file-name");

const processBtn =
    document.getElementById("process-btn");

const processing =
    document.getElementById("processing");

const ocrSection =
    document.getElementById("ocr-section");

const resultsSection =
    document.getElementById("results-section");

const evaluateBtn =
    document.getElementById("evaluate-btn");


// ============================================================
// INITIAL QUESTIONS
// ============================================================

addQuestion();


// ============================================================
// ADD QUESTION
// ============================================================

addQuestionBtn.addEventListener(
    "click",
    addQuestion
);


function addQuestion() {

    const questionNumber =
        questions.length + 1;

    const question = {

        number: questionNumber,

        question: "",

        answer_key: "",

        rubric: "",

        max_marks: 1

    };


    questions.push(question);

    renderQuestions();
}


// ============================================================
// RENDER QUESTIONS
// ============================================================

function renderQuestions() {

    questionsContainer.innerHTML = "";


    questions.forEach(
        (question, index) => {

            const card =
                document.createElement("div");

            card.className =
                "question-card";


            card.innerHTML = `

                <div class="question-header">

                    <h3>
                        Question ${question.number}
                    </h3>

                    <button
                        class="remove-question"
                        onclick="removeQuestion(${index})">

                        Remove

                    </button>

                </div>


                <label>
                    Question
                </label>

                <textarea
                    class="question-text"
                    data-index="${index}"
                    placeholder="Enter exam question...">${escapeHtml(question.question)}</textarea>


                <label>
                    Teacher Answer Key
                </label>

                <textarea
                    class="answer-key"
                    data-index="${index}"
                    placeholder="Enter the correct answer...">${escapeHtml(question.answer_key)}</textarea>


                <label>
                    Marking Rubric
                </label>

                <textarea
                    class="rubric"
                    data-index="${index}"
                    placeholder="Example: Definition - 1 mark&#10;Purpose - 1 mark&#10;Example - 1 mark">${escapeHtml(question.rubric)}</textarea>


                <label>
                    Maximum Marks
                </label>

                <input
                    type="number"
                    class="max-marks"
                    data-index="${index}"
                    min="1"
                    value="${question.max_marks}">

            `;


            questionsContainer.appendChild(card);

        }
    );


    attachQuestionListeners();
}


// ============================================================
// QUESTION INPUT LISTENERS
// ============================================================

function attachQuestionListeners() {

    document
        .querySelectorAll(".question-text")
        .forEach(input => {

            input.addEventListener(
                "input",
                event => {

                    const index =
                        event.target.dataset.index;

                    questions[index].question =
                        event.target.value;

                }
            );

        });


    document
        .querySelectorAll(".answer-key")
        .forEach(input => {

            input.addEventListener(
                "input",
                event => {

                    const index =
                        event.target.dataset.index;

                    questions[index].answer_key =
                        event.target.value;

                }
            );

        });


    document
        .querySelectorAll(".rubric")
        .forEach(input => {

            input.addEventListener(
                "input",
                event => {

                    const index =
                        event.target.dataset.index;

                    questions[index].rubric =
                        event.target.value;

                }
            );

        });


    document
        .querySelectorAll(".max-marks")
        .forEach(input => {

            input.addEventListener(
                "input",
                event => {

                    const index =
                        event.target.dataset.index;

                    questions[index].max_marks =
                        Number(event.target.value);

                }
            );

        });

}


// ============================================================
// REMOVE QUESTION
// ============================================================

function removeQuestion(index) {

    if (questions.length === 1) {

        alert(
            "At least one question is required."
        );

        return;
    }


    questions.splice(
        index,
        1
    );


    questions.forEach(
        (question, i) => {

            question.number =
                i + 1;

        }
    );


    renderQuestions();
}


// ============================================================
// FILE SELECTION
// ============================================================

chooseFileBtn.addEventListener(
    "click",
    () => {

        answerSheetInput.click();

    }
);


answerSheetInput.addEventListener(
    "change",
    () => {

        if (
            answerSheetInput.files.length > 0
        ) {

            fileName.textContent =
                "Selected: " +
                answerSheetInput.files[0].name;

        }

    }
);


// ============================================================
// RUN OCR + AI STRUCTURING
// ============================================================

processBtn.addEventListener(
    "click",
    processAnswerSheet
);


async function processAnswerSheet() {

    // --------------------------------------------------------
    // Validate questions
    // --------------------------------------------------------

    if (!validateQuestions()) {

        return;

    }


    // --------------------------------------------------------
    // Validate file
    // --------------------------------------------------------

    if (
        answerSheetInput.files.length === 0
    ) {

        alert(
            "Please upload the handwritten answer sheet."
        );

        return;

    }


    const file =
        answerSheetInput.files[0];


    // --------------------------------------------------------
    // Form data
    // --------------------------------------------------------

    const formData =
        new FormData();


    formData.append(
        "image",
        file
    );


    formData.append(
        "questions",
        JSON.stringify(questions)
    );


    // --------------------------------------------------------
    // UI
    // --------------------------------------------------------

    processBtn.disabled =
        true;

    processBtn.textContent =
        "Processing...";

    processing.classList.remove(
        "hidden"
    );


    try {

        const response =
            await fetch(
                `${API_URL}/api/process-answer-sheet`,
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Failed to process answer sheet."
            );

        }


        // ----------------------------------------------------
        // Save results
        // ----------------------------------------------------

        structuredAnswers =
            data.structured_answers || [];


        // ----------------------------------------------------
        // Display OCR
        // ----------------------------------------------------

        document.getElementById(
            "ocr-confidence"
        ).textContent =
            formatPercent(
                data.ocr.confidence
            );


        document.getElementById(
            "parser-confidence"
        ).textContent =
            formatPercent(
                data.parser_confidence
            );


        document.getElementById(
            "ocr-text"
        ).textContent =
            data.ocr.text || "";


        renderStructuredAnswers();


        ocrSection.classList.remove(
            "hidden"
        );


        // Scroll to OCR section

        ocrSection.scrollIntoView({
            behavior: "smooth"
        });


    } catch (error) {

        console.error(error);

        alert(
            "Error:\n" +
            error.message
        );

    } finally {

        processBtn.disabled =
            false;

        processBtn.textContent =
            "🔎 Run OCR + AI Structuring";

        processing.classList.add(
            "hidden"
        );

    }

}


// ============================================================
// RENDER STRUCTURED ANSWERS
// ============================================================

function renderStructuredAnswers() {

    const container =
        document.getElementById(
            "structured-answers"
        );


    container.innerHTML = "";


    if (
        structuredAnswers.length === 0
    ) {

        container.innerHTML = `
            <div class="answer-box">
                No structured answers were detected.
            </div>
        `;

        return;

    }


    structuredAnswers.forEach(
        answer => {

            const box =
                document.createElement("div");

            box.className =
                "answer-box";


            box.innerHTML = `

                <h4>
                    Q${answer.question_number}
                </h4>

                <p>
                    ${escapeHtml(
                        answer.answer || "No answer detected."
                    )}
                </p>

                <div class="answer-confidence">

                    Parser Confidence:
                    ${formatPercent(
                        answer.confidence
                    )}

                </div>

            `;


            container.appendChild(box);

        }
    );

}


// ============================================================
// EVALUATE ANSWERS
// ============================================================

evaluateBtn.addEventListener(
    "click",
    evaluateAnswers
);


async function evaluateAnswers() {

    if (
        structuredAnswers.length === 0
    ) {

        alert(
            "No structured answers available."
        );

        return;

    }


    evaluateBtn.disabled =
        true;

    evaluateBtn.textContent =
        "Evaluating...";


    try {

        const response =
            await fetch(
                `${API_URL}/api/evaluate`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        questions:
                            questions,

                        structured_answers:
                            structuredAnswers

                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Evaluation failed."
            );

        }


        evaluationResults =
            data.results || [];


        renderResults(
            data
        );


        resultsSection.classList.remove(
            "hidden"
        );


        resultsSection.scrollIntoView({
            behavior: "smooth"
        });


    } catch (error) {

        console.error(error);

        alert(
            "Evaluation error:\n" +
            error.message
        );

    } finally {

        evaluateBtn.disabled =
            false;

        evaluateBtn.textContent =
            "🚀 Evaluate Answers Using Rubric";

    }

}


// ============================================================
// RENDER RESULTS
// ============================================================

function renderResults(data) {

    const summary =
        data.summary;


    document.getElementById(
        "ai-total"
    ).textContent =

        `${formatNumber(summary.ai_total)} / ${formatNumber(summary.maximum_total)}`;


    document.getElementById(
        "percentage"
    ).textContent =

        `${formatNumber(summary.percentage)}%`;


    document.getElementById(
        "review-count"
    ).textContent =

        summary.manual_review_count;


    const container =
        document.getElementById(
            "question-results"
        );


    container.innerHTML = "";


    data.results.forEach(
        result => {

            const grading =
                result.grading;


            const card =
                document.createElement("div");

            card.className =
                "question-result";


            const reviewClass =
                grading.manual_review
                    ? "review-yes"
                    : "review-no";


            const reviewText =
                grading.manual_review
                    ? "⚠ Manual Review"
                    : "🟢 No Review";


            let criteriaHTML =
                "";


            if (
                grading.criteria
            ) {

                grading.criteria.forEach(
                    criterion => {

                        criteriaHTML += `

                            <div class="rubric-item">

                                <strong>

                                    ${escapeHtml(
                                        criterion.name
                                    )}

                                    — ${criterion.awarded_marks}
                                    /
                                    ${criterion.max_marks}

                                </strong>

                                <div class="rubric-evidence">

                                    ${escapeHtml(
                                        criterion.evidence
                                    )}

                                </div>

                            </div>

                        `;

                    }
                );

            }


            let missingHTML =
                "";


            if (
                grading.missing_concepts &&
                grading.missing_concepts.length > 0
            ) {

                missingHTML = `

                    <p>
                        <strong>
                            Missing Concepts:
                        </strong>

                        ${grading.missing_concepts
                            .map(
                                concept =>
                                    escapeHtml(concept)
                            )
                            .join(", ")
                        }

                    </p>

                `;

            }


            card.innerHTML = `

                <div class="question-result-header">

                    <div>

                        <h3>
                            Q${result.question_number}
                        </h3>

                        <span>
                            Grading Confidence:
                            ${formatPercent(
                                grading.confidence
                            )}
                        </span>

                    </div>


                    <div>

                        <div class="score">

                            ${grading.suggested_score}
                            /
                            ${grading.maximum_score}

                        </div>

                        <span class="review-badge ${reviewClass}">

                            ${reviewText}

                        </span>

                    </div>

                </div>


                <p>

                    <strong>
                        Student Answer:
                    </strong>

                </p>

                <p>

                    ${escapeHtml(
                        result.student_answer ||
                        "No answer detected."
                    )}

                </p>


                <div style="margin-top:15px">

                    <strong>
                        Rubric Breakdown
                    </strong>

                    ${criteriaHTML}

                </div>


                <div style="margin-top:15px">

                    ${missingHTML}

                </div>


                <div style="margin-top:15px">

                    <strong>
                        AI Reason:
                    </strong>

                    <p>
                        ${escapeHtml(
                            grading.reason || ""
                        )}
                    </p>

                </div>

            `;


            container.appendChild(card);

        }
    );


    // --------------------------------------------------------
    // Automatically set teacher score to AI total
    // --------------------------------------------------------

    document.getElementById(
        "teacher-score"
    ).value =
        summary.ai_total;

}


// ============================================================
// FINALIZE RESULT
// ============================================================

document.getElementById(
    "finalize-btn"
).addEventListener(
    "click",
    finalizeResult
);


function finalizeResult() {

    const score =
        document.getElementById(
            "teacher-score"
        ).value;


    const comment =
        document.getElementById(
            "teacher-comment"
        ).value;


    if (score === "") {

        alert(
            "Please enter the teacher's final score."
        );

        return;

    }


    document.getElementById(
        "final-score"
    ).textContent =

        score;


    document.getElementById(
        "final-comment"
    ).textContent =

        comment ||
        "Final result confirmed by teacher.";


    document.getElementById(
        "final-result"
    ).classList.remove(
        "hidden"
    );


    document.getElementById(
        "final-result"
    ).scrollIntoView({
        behavior: "smooth"
    });

}


// ============================================================
// VALIDATE QUESTIONS
// ============================================================

function validateQuestions() {

    for (
        const question of questions
    ) {

        if (
            !question.question.trim()
        ) {

            alert(
                `Please enter Question ${question.number}.`
            );

            return false;

        }


        if (
            !question.answer_key.trim()
        ) {

            alert(
                `Please enter the answer key for Question ${question.number}.`
            );

            return false;

        }


        if (
            !question.rubric.trim()
        ) {

            alert(
                `Please enter the rubric for Question ${question.number}.`
            );

            return false;

        }


        if (
            !question.max_marks ||
            question.max_marks <= 0
        ) {

            alert(
                `Please enter valid maximum marks for Question ${question.number}.`
            );

            return false;

        }

    }


    return true;

}


// ============================================================
// HELPERS
// ============================================================

function formatPercent(value) {

    const number =
        Number(value || 0) * 100;


    return (
        number.toFixed(1) +
        "%"
    );

}


function formatNumber(value) {

    const number =
        Number(value || 0);


    return Number.isInteger(number)
        ? number
        : number.toFixed(1);

}


function escapeHtml(value) {

    if (
        value === null ||
        value === undefined
    ) {

        return "";

    }


    return String(value)

        .replaceAll("&", "&amp;")

        .replaceAll("<", "&lt;")

        .replaceAll(">", "&gt;")

        .replaceAll('"', "&quot;")

        .replaceAll("'", "&#039;");

}