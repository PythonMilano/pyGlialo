from flask import Flask, render_template, redirect, url_for

from pyGlialo import *

app = Flask(__name__)


@app.route('/')
def spread_the_goodies():
    winner_json = extract_safe_winner(MEETUP_JSON)
    winner = {
        'name': winner_json['member']['name'],
        'member_id': winner_json['member']['member_id'],
        'photo_url': safe_photo_url(winner_json)
    }
    lead_text = 'Rolling for goodies Number %s' % str(len(LIST_OF_WINNERS) + 1)
    print(len(MEETUP_JSON['results']))
    return render_template('index.html', winner=winner, winners=LIST_OF_WINNERS, lead_text=lead_text)


@app.route('/save/<name>/')
def save_winner(name):
    if name not in LIST_OF_WINNERS:
        LIST_OF_WINNERS.append(name)
    return redirect(url_for('spread_the_goodies'))


@app.route('/pass')
def pass_extraction():
    LIST_OF_WINNERS.append('empty_slot')
    return redirect(url_for('spread_the_goodies'))


@app.route('/finalize')
def finalize_the_goodies():
    save_winners_list(LIST_OF_WINNERS)
    return render_template('finalize.html', winners=LIST_OF_WINNERS)


@app.route('/reset')
def reset_app():
    MEETUP_JSON = get_meetup_json()  # reset_meetup_json()
    LIST_OF_WINNERS.clear()
    winner = {
        'name': 'PyGlialo is Reset',
        'member_id': '000000',
        'photo_url': '/static/img/Reset_Icon.png'
    }
    reset_text = 'Reset Successful'
    return render_template('index.html', winner=winner, winners=LIST_OF_WINNERS, lead_text=reset_text)


@app.route('/remove/<name>')
def remove_absent(name):
    member_to_eliminate = get_full_details_of(name)
    remove_member_from_pool(name)
    reset_text = 'Removed from POOL'
    # return render_template('index.html', winner=winner, winners=LIST_OF_WINNERS, lead_text=reset_text)
    return redirect(url_for('spread_the_goodies'))


if __name__ == '__main__':
    app.run(debug=True)
