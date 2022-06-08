const $guessForm = $("#guess-form");
const $guessResult = $('#guess-result');
const $currentScore = $('.current-score');
const $gameContainer = $('#game-container')
let score = 0;
let gameStarted = false;

//On submit call getUserGuess, which normalizes case to lowercase
//and then sends to the server to validate

$guessForm.on("submit", getUserGuess);

function getUserGuess(e){
    e.preventDefault();
    const $guess = $("#guess").val().toLowerCase();
    sendGuessToServer($guess);
   
    //check if game has already started
    if(!gameStarted){
        gameStarted = true;
        startTimer();
    }
}

//Send to server to validate the guess, await response, then pass to showGuessResult
async function sendGuessToServer(guess){
    const response = await axios.get('/is-word-valid', {params: {guess}});
    const {result} = response.data;
    showGuessResult(result);
}

//showGuessResult show the users the whether their guess was valid word and on the board, valid word but not on board, or not a word period
function showGuessResult(result){
    
    $guessResult.empty();
    
    if(result === 'ok') {
        $guessResult.text('You found a valid word!');
        updateScore();
    } else if (result === 'not-word'){
        $guessResult.text('Sorry, that word is in invalid or not in our dictionary');
    } else if(result === 'already-played'){
        return $guessResult.text('This word was already played')
    }
     else {
        $guessResult.text('That is a word, but it is not on the board');
    }
}

//show and update current score
function updateScore(){
    score++;
    $currentScore.empty().text(`Score: ${score}`)
}

//countdown from 60 seconds to 0
function startTimer(){
    let timeRem = 60;
    let countdown = setInterval(function (){
        timeRem--
        if(timeRem <= 0){
            clearInterval(countdown)
            $("#timer").empty().text("Time's Up!");
            $guessForm.off()
            $('#interact').remove()
            $('button').text('Start Over')
            postScoreAndNumPlays()
            return;
        } else {
            $("#seconds").text(`${timeRem}`);
        }
    }, 1000);
}

//When timer runs out, check if new high score, and update number of times played
async function postScoreAndNumPlays(){
    const response = await axios.post("/update-score-plays", {score})
    if(response.data.newBestScore){
        $guessResult.text(`The new high score is ${score}`)
    }
}