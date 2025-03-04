const yearSelect = document.getElementById('yearSelect');
const startPYQTestBtn = document.getElementById('startPYQTestBtn');
const questionContainer = document.getElementById('questionContainer');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const submitBtn = document.getElementById('submitBtn');
const resultsContainer = document.getElementById('resultsContainer');
const scorecardFrame = document.getElementById('scorecardFrame');
const scorecardContent = document.getElementById('scorecardContent');
const homeButton = document.getElementById('homeButton');

let questions = [];
let userAnswers = {};
let currentQuestionIndex = 0;

function populateYears() {
    const startYear = 2014;
    const currentYear = new Date().getFullYear();

    for (let year = startYear; year <= currentYear; year++) {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearSelect.appendChild(option);
    }
}

populateYears();

async function fetchQuestions(year) {
    try {
        const response = await fetch(`/api/get_yearwise_pyq/?year=${year}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching questions:", error);
        return [];
    }
}

startPYQTestBtn.addEventListener('click', async () => {
    const selectedYear = yearSelect.value;
    questions = await fetchQuestions(selectedYear);
    if (questions.length > 0) {
        startQuiz();
    } else {
        alert("No questions found for the selected year.");
    }
});

function startQuiz() {
    startPYQTestBtn.style.display = 'none';
    yearSelect.style.display = 'none';
    prevBtn.style.display = 'inline-block';
    nextBtn.style.display = 'inline-block';
    submitBtn.style.display = 'inline-block';
    currentQuestionIndex = 0;
    userAnswers = {};
    scorecardFrame.style.display = 'none';
    displayQuestion();
}

function displayQuestion() {
    questionContainer.innerHTML = '';
    const question = questions[currentQuestionIndex];
    if (!question) return;

    const questionNumberFrame = document.createElement('div');
    questionNumberFrame.className = 'question-number-frame';
    questionNumberFrame.textContent = `Q. ${currentQuestionIndex + 1} )`;
    questionContainer.appendChild(questionNumberFrame);

    const questionTextElement = document.createElement('h3');
    questionTextElement.innerHTML = question.question_text.replace('**', '').replace(/\n/g, '<br><br>');
    questionContainer.appendChild(questionTextElement);

    const options = ['a', 'b', 'c', 'd'];
    options.forEach(option => {
        const optionBtn = document.createElement('button');
        optionBtn.className = 'option-btn';
        optionBtn.textContent = question[`option_${option}`];
        optionBtn.dataset.option = option;

        const optionNumberContainer = document.createElement('div');
        optionNumberContainer.className = 'option-number-container';
        optionNumberContainer.textContent = option.toUpperCase();
        optionBtn.prepend(optionNumberContainer);

        if (userAnswers[currentQuestionIndex] === option) {
            optionBtn.classList.add('selected');
        }

        optionBtn.addEventListener('click', () => {
            if (userAnswers[currentQuestionIndex] === option) {
                delete userAnswers[currentQuestionIndex];
                optionBtn.classList.remove('selected');
            } else {
                userAnswers[currentQuestionIndex] = option;
                document.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('selected'));
                optionBtn.classList.add('selected');
            }
        });

        questionContainer.appendChild(optionBtn);
    });

    prevBtn.disabled = currentQuestionIndex === 0;
    nextBtn.disabled = currentQuestionIndex === questions.length - 1;
}

function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    } else {
        showResults();
    }
}

function prevQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
}

function showResults() {
    questionContainer.style.display = 'none';
    prevBtn.style.display = 'none';
    nextBtn.style.display = 'none';
    submitBtn.style.display = 'none';
    resultsContainer.style.display = 'block';
    yearSelect.disabled = true;
    startPYQTestBtn.style.display = 'none';
    let resultsHTML = '';
    let score = 0;
    let correctCount = 0;
    let incorrectCount = 0;
    let attemptedCount = 0;

    questions.forEach((question, index) => {
        const correctAnswer = question.correct_option.replace(/[()]/g, '').toLowerCase();
        const userAnswer = userAnswers[index];
        const isCorrect = userAnswer === correctAnswer;

        resultsHTML += `
            <div class="question-result">
                <div class="question-number-frame">Q. ${index + 1} )</div>
                <p>${question.question_text.replace('**', '').replace(/\n/g, '<br><br>')}</p>
        `;

        const options = ['a', 'b', 'c', 'd'];
        options.forEach(option => {
            const optionText = question[`option_${option}`];
            let className = 'option-btn';

            if (option === correctAnswer) className += ' correct';
            if (option === userAnswer && option !== correctAnswer) className += ' incorrect';
            if (option === userAnswer) className += ' selected';

            const optionBtn = document.createElement('button');
            optionBtn.className = className.trim();
            optionBtn.textContent = optionText;
            optionBtn.disabled = true;

            const optionNumberContainer = document.createElement('div');
            optionNumberContainer.className = 'option-number-container';
            optionNumberContainer.textContent = option.toUpperCase();
            optionBtn.prepend(optionNumberContainer);

            resultsHTML += optionBtn.outerHTML;
        });

        resultsHTML += `
            <p class="explanation">Explanation: ${question.explanation.replace(/\n/g, '<br>')}</p>
        `;
        if (isCorrect) {
            score += 2;
            correctCount++;
            attemptedCount++;
        } else if (userAnswer) {
            score -= 2 / 3;
            incorrectCount++;
            attemptedCount++;
        }
    });

    scorecardContent.innerHTML = `
        <p><span class="scorecard-label">Score:</span><span class="scorecard-value">${score.toFixed(2)}</span></p>
        <p><span class="scorecard-label">Correct:</span><span class="scorecard-value">${correctCount}</span></p>
        <p><span class="scorecard-label">Incorrect:</span><span class="scorecard-value">${incorrectCount}</span></p>
        <p><span class="scorecard-label">Attempted:</span><span class="scorecard-value">${attemptedCount}</span></p>
        <p><span class="scorecard-label">Total:</span><span class="scorecard-value">${questions.length}</span></p>
    `;
    scorecardFrame.style.display = 'block';

    resultsHTML += `<p>Score: ${score.toFixed(2)}</p>`;
    resultsHTML += `<p>Correct Answers: ${correctCount}</p>`;
    resultsHTML += `<p>Incorrect Answers: ${incorrectCount}</p>`;
    resultsHTML += `<p>Attempted Answers: ${attemptedCount}</p>`;
    resultsHTML += `<p>Total Questions: ${questions.length}</p>`;

    resultsContainer.innerHTML = resultsHTML;
}

homeButton.addEventListener('click', () => {
    window.location.href = "{% url 'quiz_view' %}";
});

prevBtn.addEventListener('click', prevQuestion);
nextBtn.addEventListener('click', nextQuestion);
submitBtn.addEventListener('click', showResults);