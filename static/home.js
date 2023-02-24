const wordForm = document.querySelector('#guess-word-form');
const wordInput = document.querySelector('#guess');

const msg = document.querySelector('#msg');
const scoreDisplay = document.querySelector('#score');
const timerDisplay = document.querySelector('#timer');
const highScoreDisplay = document.querySelector('#highscore');

let score = 0;
scoreDisplay.innerText = `Score: ${score}`;

const guessedWords = new Set();

wordForm.addEventListener('submit', handleClick);

async function handleClick(e) {
    e.preventDefault();
    const response = await processGuess();
    displayWordValidityAndScore(response);
    wordForm.reset();
}

async function processGuess() {
    const config = { params: { guess: wordInput.value } };
    const res = await axios.get('/process-guess', config);
    return res.data.result;
}

function displayWordValidityAndScore(response) {
    msg.innerText = `${wordInput.value} is ${response}`;
    if (response == 'ok') {
        if (guessedWords.has(wordInput.value)) {
            msg.innerText = `${wordInput.value} was already guessed`;
        } else {
            score += wordInput.value.length;
            guessedWords.add(wordInput.value);
        }
    }
    scoreDisplay.innerText = `Score: ${score}`;
}

let time = 60;
timerDisplay.innerText = `Time Left: ${time}`;
const timer = setInterval(async function () {
    time--;
    timerDisplay.innerText = `Time Left: ${time}`;
    if (time == 0) {
        clearInterval(timer);
        wordForm.removeEventListener('submit', handleClick);
        wordInput.disabled = true;
        wordInput.value = '';
        await updateHighScore(score);
    }
}, 1000);

async function updateHighScore(score) {
    const config = { params: { highscore: score } };
    const response = await axios.get('/update-high-score', config);
    let highscore = response.data.highscore;
    let plays = response.data.plays;
    highScoreDisplay.innerText = `High Score: ${highscore} in ${plays} play(s)`;
}