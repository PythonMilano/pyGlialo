# -*- coding: utf-8 -*-
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
    list_of_winners = None
    winner = None

    def __init__(self):
        self.list_of_winners = []
        self.event = {}
        current_events = get_data_from_url(URL_EVENTS)
        past_events = get_data_from_url(URL_EVENTS + '?status=past')
        if current_events:
            self.event = min(current_events, key=lambda event: abs(event['time'] - time.time()))
        if not current_events and past_events:
            self.event = max(past_events, key=lambda event: abs(event['time'] - time.time()))

    def load_meetup_data(self):
        self.event_id = self.event.get('id')
        self.event_rsvps = get_data_from_url(URL_RSVPS.format(id=self.event_id))
        self.list_of_winners = []

    def extract_safe_winner(self):
        self.winner = None
        if self.event_rsvps and len(self.event_rsvps):
            lucky_number = random.randint(0, abs(len(self.event_rsvps) - 1))
            winner = self.event_rsvps[lucky_number]
            self.event_rsvps.remove(winner)
            if winner['response'] == 'yes':
                self.winner = {
                    'name': winner['member']['name'],
                    'member_id': winner['member']['id'],
                    'photo_url': winner['member'].get('photo', {}).get('photo_link', '/static/img/no_image.png')
                }
            else:
                self.extract_safe_winner()

    def save_winners_list(self):
        file_date = datetime.datetime.now()
        with open("winner_list_{}.txt".format(file_date.strftime("%Y-%m-%d")), "w") as out_file:
            out_file.write("File generato il: {}\n".format(file_date.strftime("%Y-%m-%d_%H:%M:%S")))
            out_file.write("Lista vincitori per i goodies\n")
            for winner in self.list_of_winners:
                out_file.write("{}\n".format(winner))


pyglialo = PyGlialo()
