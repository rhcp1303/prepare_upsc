	document.addEventListener('DOMContentLoaded', () => {
		const generateButton = document.getElementById('generateButton');
		const testContainer = document.getElementById('testContainer');
		const testForm = document.getElementById('testForm');
		const submitButton = document.getElementById('submitButton');
		const resultContainer = document.getElementById('resultContainer');
		const scoreDiv = document.getElementById('score');
		const explanationsDiv = document.getElementById('explanations');
		const timerDisplay = document.getElementById('time');

		let questions;
		let timerInterval;
		let timeLeft = 60 * 60;
		let currentQuestionIndex = 0;

		generateButton.addEventListener('click', () => {
			fetch('/api/get_mock_mcq/?num_questions=50')
				.then(response => response.json())
				.then(data => {
					if (data.error) {
						alert(data.error);
						return;
					}
					questions = data.questions;
					displayQuestions(questions);
					startTimer();
					testContainer.style.display = 'block';
					resultContainer.style.display = 'none';
					generateButton.disabled = true;
				})
				.catch(error => {
					console.error("Error fetching questions:", error);
					alert("An error occurred while fetching questions.");
				});
		});

		function displayQuestions(questions) {
			testForm.innerHTML = '';
			currentQuestionIndex = 0;
			showQuestion(currentQuestionIndex);
		}



		function showQuestion(index) {
			if (index < 0 || index >= questions.length) return;

			const question = questions[index];
			const questionDiv = document.createElement('div');
			questionDiv.className = 'question';

			const questionTextWithoutAsterisks = question.question_text.replace(/\*/g, "");
			const questionTextWithTabs = questionTextWithoutAsterisks.replace(/:/g, ":\t\t\t");
			const questionTextWithBreaks = questionTextWithTabs.replace(/\n/g, "<br>");

			questionDiv.innerHTML = `<h5>${questionTextWithBreaks}</h5>`;

			if (question.pairs && question.pairs.length > 0) {
				const pairsContainer = document.createElement('div');
				pairsContainer.className = 'pairs-container';

				question.pairs.forEach(pair => {
					const pairDiv = document.createElement('div');
					pairDiv.className = 'pair';
					pairDiv.innerHTML = `
                        <span class="pair-label">${pair.label}</span>: <span>${pair.description}</span>
                    `;
					pairsContainer.appendChild(pairDiv);
				});
				questionDiv.appendChild(pairsContainer);
			}

			const optionsDiv = document.createElement('div');
			optionsDiv.className = 'options';

			['option_a', 'option_b', 'option_c', 'option_d'].forEach(optionKey => {
				if (question[optionKey]) {
					optionsDiv.innerHTML += `
                        <div class="option"> <input type="radio" name="q${index}" value="${optionKey}" id="q${index}-${optionKey}"> <label for="q${index}-${optionKey}">${question[optionKey]}</label> </div>
                    `;
				}
			});

			questionDiv.appendChild(optionsDiv);
			document.getElementById('questionContainer').innerHTML = '';
			document.getElementById('questionContainer').appendChild(questionDiv);

			prevButton.disabled = index === 0;
			nextButton.disabled = index === questions.length - 1;
		}

		const prevButton = document.getElementById('prevButton');
		const nextButton = document.getElementById('nextButton');

		prevButton.addEventListener('click', () => {
			currentQuestionIndex--;
			showQuestion(currentQuestionIndex);
		});

		nextButton.addEventListener('click', () => {
			currentQuestionIndex++;
			showQuestion(currentQuestionIndex);
		});

		submitButton.addEventListener('click', () => {
			clearInterval(timerInterval);
			const answers = getAnswers();
			evaluateTest(questions, answers);
		});

		function getAnswers() {
			const answers = {};
			questions.forEach((question, index) => {
				const selectedOption = document.querySelector(`input[name="q${index}"]:checked`);
				answers[index] = selectedOption ? selectedOption.value : null;
			});
			return answers;
		}

		function evaluateTest(questions, answers) {
			let score = 0;
			const explanations = [];

			questions.forEach((question, index) => {
				const correctAnswer = question.correct_option;
				const userAnswer = answers[index];
				const isCorrect = userAnswer !== null && userAnswer === correctAnswer;

				if (isCorrect) {
					score++;
				}
				explanations.push(question.explanation);
			});

			displayResults(score, explanations);
		}

		function displayResults(score, explanations) {
			scoreDiv.textContent = `Score: ${score}`;
			explanationsDiv.innerHTML = '';
			explanations.forEach((explanation, index) => {
				const explanationDiv = document.createElement('div');
				explanationDiv.innerHTML = `<p><b>${index + 1}.</b> ${explanation}</p>`;
				explanationsDiv.appendChild(explanationDiv);
			});

			testContainer.style.display = 'none';
			resultContainer.style.display = 'block';
			generateButton.disabled = false;
		}

		function startTimer() {
			timerInterval = setInterval(() => {
				const minutes = Math.floor(timeLeft / 60);
				const seconds = timeLeft % 60;
				timerDisplay.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
				timeLeft--;
				if (timeLeft < 0) {
					clearInterval(timerInterval);
					alert("Time's up!");
					submitButton.click();
				}
			}, 1000);
		}
	});