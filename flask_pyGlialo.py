from flask import Flask

from pyGlialo import random_goodies_giveaway

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/p')
def spread_the_goodies():
    return random_goodies_giveaway()

if __name__ == '__main__':
    app.run()