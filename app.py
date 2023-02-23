from boggle import Boggle
from flask import Flask, render_template, request, session, redirect, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"

boggle_game = Boggle()


@app.route('/')
def show_board():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('home.html', board=board)


@app.route('/process-guess')
def process_guess():
    guess = request.args['guess']
    result = boggle_game.check_valid_word(session['board'], guess)

    return jsonify({'result': result})
