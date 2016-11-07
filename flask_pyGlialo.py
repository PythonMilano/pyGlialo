from flask import Flask, render_template, redirect, url_for

from pyglialo import PyGlialo

app = Flask(__name__)
piglialo = PyGlialo()
piglialo.load_meetup_data()


@app.route('/')
def index():
    return render_template('index.html', event=piglialo.event)


@app.route('/reset')
def reset_app():
    piglialo.load_meetup_data()
    return redirect(url_for('index'))


@app.route('/random')
def spread_the_goodies():
    piglialo.extract_safe_winner()
    if piglialo.winner:
        lead_text = 'Rolling for goodies Number {}'.format(len(piglialo.list_of_winners) + 1)
    else:
        lead_text = 'No one else can win!!!'
    return render_template('random.html', winner=piglialo.winner, winners=piglialo.list_of_winners, lead_text=lead_text)


@app.route('/save/<name>/')
def save_winner(name):
    if name not in piglialo.list_of_winners:
        piglialo.list_of_winners.append(name)
        piglialo.remove_rsvp(name)
    return redirect(url_for('saved'))


@app.route('/saved')
def saved():
    name = piglialo.list_of_winners[-1]
    winner = {
        'name': name
    }
    lead_text = 'Winner for slot {}'.format(len(piglialo.list_of_winners))
    return render_template('saved.html', winner=winner, winners=piglialo.list_of_winners, lead_text=lead_text)


@app.route('/pass')
def pass_extraction():
    piglialo.list_of_winners.append('empty_slot')
    lead_text = 'Slot {} is empty :('.format(len(piglialo.list_of_winners))
    return render_template('pass.html', winners=piglialo.list_of_winners, lead_text=lead_text)


@app.route('/finalize')
def finalize_the_goodies():
    piglialo.save_winners_list()
    return render_template('finalize.html', winners=piglialo.list_of_winners)


if __name__ == '__main__':
    app.run(debug=True)
