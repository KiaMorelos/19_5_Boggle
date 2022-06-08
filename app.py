from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "its_a_secret_to-everybody"

boggle_game = Boggle()

@app.route('/')
def display_board():
    """Display Boggle Board"""
    board = boggle_game.make_board()
   
    session['board'] = board
    bestscore = session.get("bestscore", 0)
    times_played = session.get("plays", 0)

    return render_template('board.html', board=board, bestscore=bestscore, times_played=times_played)

@app.route('/is-word-valid')
def check_word_guess():
    """Check that users word is in the dictionary and on the board, return result"""
    word_guess = request.args['guess']
    board = session['board']
    result = boggle_game.check_valid_word(board, word_guess)
    return jsonify({"result" : result})
    
@app.route('/update-score-plays', methods=["POST"])
def update_score_plays():
    """See if the players score beats the orginal high score, and update number of times played"""
    score = request.json["score"]
    bestscore = session.get("bestscore", 0)
    times_played = session.get("plays", 0)

    session['plays'] = times_played + 1
    session['bestscore'] = max(score, bestscore)
   
    return jsonify(newBestScore = score > bestscore)