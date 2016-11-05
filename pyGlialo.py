import datetime
import json
import time

import urllib.error
import urllib.parse
import urllib.request

from random import randint
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

    def load_meetup_data(self, meetup_id=None):
        data = get_data_from_url(URL_EVENTS)
        event = min(data, key=lambda event: abs(event['time'] - time.time()))
        print(" --> Nearest event in time: {} at time {}".format(event['name'], event['time']))
        self.event = event
        self.event_id = event['id']
        self.event_rsvps = get_data_from_url(URL_RSVPS.format(id=self.event_id))
        self.list_of_winners = []

    def extract_safe_winner(self):
        lucky_number = randint(0, abs(len(self.event_rsvps['results']) - 1))
        if len(self.event_rsvps['results']):
            winner = self.event_rsvps['results'][lucky_number]
            self.remove_rsvp(winner['member']['name'])
            if winner['response'] == 'yes':
                self.winner = {
                    'name': winner['member']['name'],
                    'member_id': winner['member']['member_id'],
                    'photo_url': self.rsvp_photo(winner)
                }
            else:
                self.winner = None
                self.extract_safe_winner()
        else:
            self.winner = None

    def remove_rsvp(self, rsvp_name):
        for idx, result in enumerate(self.event_rsvps['results']):
            if rsvp_name == result['member']['name']:
                self.event_rsvps['results'].pop(idx)
                break

    def save_winners_list(self):
        with open("winner_list.txt", "w") as out_file:
            out_file.write("File generato il: {}\n".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")))
            out_file.write("Lista vincitori per i goodies\n")
            for winner in self.winners:
                out_file.write("{}\n".format(winner))

    def rsvp_photo(self, winner):
        if 'member_photo' in winner:
            return winner['member_photo']['photo_link']
        else:
            return "/static/img/No_image.png"
