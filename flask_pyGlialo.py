# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for

from pyglialo import pyglialo

app = Flask(__name__)


@app.route('/')
@app.route('/reset')
def index():
    pyglialo.load_meetup_data()
    return render_template('index.html', event=pyglialo.event)


@app.route('/random')
def spread_the_goodies():
    pyglialo.extract_safe_winner()
    if pyglialo.winner:
        lead_text = 'Rolling for goodies Number {}'.format(len(pyglialo.list_of_winners) + 1)
    else:
        lead_text = 'No one else can win!!!'
    return render_template('random.html', winner=pyglialo.winner, winners=pyglialo.list_of_winners, lead_text=lead_text)


@app.route('/save/<name>/')
def save_winner(name):
    if name not in pyglialo.list_of_winners:
        pyglialo.list_of_winners.append(name)
    return redirect(url_for('saved'))


@app.route('/saved')
def saved():
    name = pyglialo.list_of_winners[-1]
    winner = {
        'name': name
    }
    lead_text = 'Winner for slot {}'.format(len(pyglialo.list_of_winners))
    return render_template('saved.html', winner=winner, winners=pyglialo.list_of_winners, lead_text=lead_text)


@app.route('/finalize')
def finalize_the_goodies():
    pyglialo.save_winners_list()
    return render_template('finalize.html', winners=pyglialo.list_of_winners)


if __name__ == '__main__':
    app.run(debug=True)
