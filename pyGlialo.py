import json
import urllib.error
import urllib.parse
import urllib.request
from random import randint

from secrets import meetup_api_key


def get_event_id():
    # TODO recuperare l'id da https://api.meetup.com/2/events? -> result[0].ID
    return "226276326"

def spin_the_wheel(data):
    max_int = len(data['results'])
    return randint(0, max_int)


event_id = get_event_id()
url = "https://api.meetup.com/2/rsvps?offset=0&format=json&event_id=" + \
      event_id + \
      "&photo-host=public&page=20&fields=&order=event&desc=false&sig_id=99027442&sig=" + \
      meetup_api_key
response = urllib.request.urlopen(url)
data = json.loads(response.read().decode("utf-8"))

lucky_number = spin_the_wheel(data)

print(data['results'][lucky_number]['member']['name'])
