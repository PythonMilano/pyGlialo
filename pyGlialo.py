import datetime
import json
import urllib.error
import urllib.parse
import urllib.request
from random import randint
from secrets import meetup_api_key
import time

def get_event_id():
    url = "https://api.meetup.com/Python-Milano/events"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))
    nearest_event = min(data, key = lambda event:abs(event['time'] - time.time()))
    print(" --> Nearest event in time: "+nearest_event['name']+ " at time "+str(nearest_event['time']))
    return str(nearest_event['id'])

def spin_the_wheel(some_meetup_json):
    max_int = len(some_meetup_json['results']) - 1
    return randint(0, max_int)


def extract_safe_winner(meetup_json):
    winner_json = extract_winner(meetup_json)
    if winner_json['response'] == 'yes':
        return winner_json
    else:
        remove_member_from_pool(winner_json['member']['name'])
        return extract_winner(meetup_json)


def extract_winner(some_meetup_json):
    lucky_number = spin_the_wheel(some_meetup_json)
    return some_meetup_json['results'][lucky_number]


def get_meetup_json():
    event_id = get_event_id()
    url = "https://api.meetup.com/2/rsvps?offset=0&format=json&event_id=" + \
          event_id + \
          "&key=" + \
          meetup_api_key
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))
    return data


def save_winners_list(winners):
    with open("winner_list.txt", "w") as out_file:
        out_file.write("File generato il: %s\n" % get_time_as_string())
        out_file.write("Lista vincitori per i goodies\n")
        for winner in winners:
            out_file.write("%s\n" % winner)


def get_time_as_string():
    date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    return date_string


def safe_photo_url(winner_json):
    if 'member_photo' in winner_json:
        return winner_json['member_photo']['photo_link']
    else:
        return "/static/img/No_image.png"


def find_index_of(name):
    for i, result in enumerate(MEETUP_JSON['results']):
        member_name = result['member']['name']
        if member_name == name:
            return i
    return NameError(name)


def remove_member_from_pool(name):
    # print('Removing: ' + name)
    index = find_index_of(name)
    MEETUP_JSON['results'].pop(index)


def get_full_details_of(name):
    index = find_index_of(name)
    return MEETUP_JSON['results'][index]


MEETUP_JSON = get_meetup_json()

LIST_OF_WINNERS = []
