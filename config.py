try:
    from secrets import meetup_api_key
except ImportError:
    meetup_api_key = 'no-api-key-provided'

URL_EVENTS = 'https://api.meetup.com/Python-Milano/events'
URL_RSVPS = 'https://api.meetup.com/2/rsvps?offset=0&format=json&event_id={id}&key=' + meetup_api_key
