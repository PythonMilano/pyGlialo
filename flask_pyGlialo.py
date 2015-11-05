from flask import Flask

from pyGlialo import extract_winner, get_meetup_json

app = Flask(__name__)

meetup_json = get_meetup_json()


@app.route('/')
def spread_the_goodies():
    winner = extract_winner(meetup_json)
    return 'Il vincitore è: ' + winner['name']


if __name__ == '__main__':
    app.run()
