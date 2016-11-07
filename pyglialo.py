import datetime
import json
import random
import time
import urllib.error
import urllib.parse
import urllib.request

from config import URL_EVENTS, URL_RSVPS


def get_data_from_url(url):
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))
    return data


class PyGlialo(object):
    event_id = None
    event_rsvps = None
    event = None
    list_of_winners = None
    winner = None

    def load_meetup_data(self):
        data = get_data_from_url(URL_EVENTS)
        if data:
            self.event = min(data, key=lambda event: abs(event['time'] - time.time()))
        else:
            self.event = {}
        self.event_id = self.event.get('id', None)
        self.event_rsvps = get_data_from_url(URL_RSVPS.format(id=self.event_id))
        self.list_of_winners = []

    def extract_safe_winner(self):
        self.winner = None
        if self.event_rsvps and len(self.event_rsvps['results']):
            lucky_number = random.randint(0, abs(len(self.event_rsvps['results']) - 1))
            winner = self.event_rsvps['results'][lucky_number]
            self.remove_rsvp(winner['member']['member_id'])
            if winner['response'] == 'yes':
                self.winner = {
                    'name': winner['member']['name'],
                    'member_id': winner['member']['member_id'],
                    'photo_url': winner.get('member_photo', {}).get('photo_link', '/static/img/No_image.png')
                }
            else:
                self.extract_safe_winner()

    def remove_rsvp(self, rsvp_id):
        for idx, result in enumerate(self.event_rsvps['results']):
            if rsvp_id == result['member']['member_id']:
                self.event_rsvps['results'].pop(idx)
                break

    def save_winners_list(self):
        file_date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        with open("winner_list_{}.txt".format(file_date), "w") as out_file:
            out_file.write("File generato il: {}\n".format(file_date))
            out_file.write("Lista vincitori per i goodies\n")
            for winner in self.list_of_winners:
                out_file.write("{}\n".format(winner))
