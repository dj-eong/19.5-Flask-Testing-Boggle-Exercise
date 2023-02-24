from boggle import Boggle
from flask import Flask, render_template, request, session, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"

debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/board')
def show_board():
    size = request.args['size']
    board = boggle_game.make_board(int(size))
    session['size'] = int(size)
    session['board'] = board
    return render_template('board.html', board=board)


@app.route('/process-guess')
def process_guess():
    guess = request.args['guess']
    result = boggle_game.check_valid_word(
        session['board'], guess, session['size'])

    return jsonify({'result': result})


@app.route('/update-high-score')
def update_score():
    score = request.args['highscore']
    session['plays'] = int(session.get('plays', 0)) + 1
    session['highscore'] = max(int(session.get('highscore', 0)), int(score))

    return jsonify({'highscore': session['highscore'], 'plays': session['plays']})
