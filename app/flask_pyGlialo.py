from flask import Flask, render_template

from app.pyGlialo import extract_winner, get_meetup_json

app = Flask(__name__)

meetup_json = get_meetup_json()


@app.route('/')
def spread_the_goodies():
    winner_json = extract_winner(meetup_json)
    winner = {'name': winner_json['name']}
    return render_template('index.html', winner=winner)


if __name__ == '__main__':
    app.run()
