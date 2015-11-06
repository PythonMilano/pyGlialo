from flask import Flask, render_template, redirect, url_for

from app.pyGlialo import extract_safe_winner, get_meetup_json, save_winners_list, safe_photo_url

app = Flask(__name__)

meetup_json = get_meetup_json()

list_of_winners = []


@app.route('/')
def spread_the_goodies():
    winner_json = extract_safe_winner(meetup_json)
    winner = {
        'name': winner_json['member']['name'],
        'member_id': winner_json['member']['member_id'],
        'photo_url': safe_photo_url(winner_json)
    }
    lead_text = 'Rolling for goodies Number %s' % str(len(list_of_winners) + 1)
    return render_template('index.html', winner=winner, winners=list_of_winners, lead_text=lead_text)


@app.route('/save/<name>/')
def save_winner(name):
    if name not in list_of_winners:
        list_of_winners.append(name)
    return redirect(url_for('spread_the_goodies'))


@app.route('/pass')
def pass_extraction():
    list_of_winners.append('empty_slot')
    return redirect(url_for('spread_the_goodies'))


@app.route('/finalize')
def finalize_the_goodies():
    save_winners_list(list_of_winners)
    return render_template('finalize.html', winners=list_of_winners)


if __name__ == '__main__':
    app.run(debug=True)
