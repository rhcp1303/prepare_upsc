const queryInput = document.getElementById('queryInput');
const startBtn = document.getElementById('startBtn');
const questionContainer = document.getElementById('questionContainer');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const submitBtn = document.getElementById('submitBtn');
const resultsContainer = document.getElementById('resultsContainer');

let questions = [];
let userAnswers = {};
let currentQuestionIndex = 0;

async function fetchQuestions(query) {
    try {
        const response = await fetch(`/api/get_quiz_questions/?query=${query}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching questions:", error);
        return [];
    }
}

startBtn.addEventListener('click', async () => {
    const query = queryInput.value;
    if (query) {
        questions = await fetchQuestions(query);
        if (questions.length > 0) {
            startQuiz();
        } else {
            alert("No questions found.");
        }
    } else {
        alert("Please enter a query.");
    }
});

function startQuiz() {
    startBtn.style.display = 'none';
    prevBtn.style.display = 'inline-block';
    nextBtn.style.display = 'inline-block';
    submitBtn.style.display = 'inline-block';
    currentQuestionIndex = 0;
    userAnswers = {};
    displayQuestion();
}

function displayQuestion() {
    questionContainer.innerHTML = '';
    const question = questions[currentQuestionIndex];
    if (!question) return;

    questionContainer.innerHTML = `<h3>${question.question_text.replace(/\n/g, '<br>')}</h3>`;

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

    let resultsHTML = '<h3>Quiz Results</h3>';
    let score = 0;
    let correctCount = 0;
    let incorrectCount = 0;
    let attemptedCount = 0;

    questions.forEach((question, index) => {
        const correctAnswer = question.correct_option.replace(/[()]/g, '').toLowerCase();
        const userAnswer = userAnswers[index];
        const isCorrect = userAnswer === correctAnswer;

        resultsHTML += `
            <p><strong>Q${index + 1}: ${question.question_text.replace(/\n/g, '<br>')}</strong></p>
        `;

        const options = ['a', 'b', 'c', 'd'];
        options.forEach(option => {
            const optionText = question[`option_${option}`];
            let className = 'option-btn'; // Start with the base class

            if (option === correctAnswer) className += ' correct';
            if (option === userAnswer && option !== correctAnswer) className += ' incorrect';
            if (option === userAnswer) className += ' selected';

            // Create button element
            const optionBtn = document.createElement('button');
            optionBtn.className = className.trim();
            optionBtn.textContent = optionText;
            optionBtn.disabled = true; // Disable buttons

            const optionNumberContainer = document.createElement('div');
            optionNumberContainer.className = 'option-number-container';
            optionNumberContainer.textContent = option.toUpperCase();
            optionBtn.prepend(optionNumberContainer);

            resultsHTML += optionBtn.outerHTML; // Append the button's HTML to the results
        });

        resultsHTML += `<p>Your Answer: ${userAnswer ? userAnswer.toUpperCase() : 'Not Answered'}</p>`;
        resultsHTML += `<p>Correct Answer: ${correctAnswer.toUpperCase()}</p>`;
        resultsHTML += `<p>Explanation: ${question.explanation.replace(/\n/g, '<br>')}</p>`;

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

    resultsHTML += `<p>Score: ${score.toFixed(2)}</p>`;
    resultsHTML += `<p>Correct Answers: ${correctCount}</p>`;
    resultsHTML += `<p>Incorrect Answers: ${incorrectCount}</p>`;
    resultsHTML += `<p>Attempted Answers: ${attemptedCount}</p>`;
    resultsHTML += `<p>Total Questions: ${questions.length}</p>`;

    resultsContainer.innerHTML = resultsHTML;
}

prevBtn.addEventListener('click', prevQuestion);
nextBtn.addEventListener('click', nextQuestion);
submitBtn.addEventListener('click', showResults);