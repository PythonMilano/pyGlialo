# -*- coding=utf-8 -*-

import datetime
import os

from box import Box
from flask import Flask, request, render_template
from eventbrite import Eventbrite

from models import Pythonista
from dbconn import database_proxy as db

from utils import random_color, slack_notifier

app = Flask(__name__)

eb_client = Eventbrite(os.environ['EVENTBRITE_TOKEN'])


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.route('/')
def index():
    """
    Index page
    """

    try:
        events = Box(eb_client.event_search(**{'organizer.id': os.environ['EVENTBRITE_ORGANIZER_ID']}))
    except:
        current_event = None
    else:
        current_event = events.events[0]
        if events.pagination.object_count > 1:
            events_map = {event.start.local: idx for idx, event in enumerate(events.events)}
            current_event = events.events[events_map[min(events_map.keys())]]

    return render_template('index.html', event=current_event)


@app.route('/wheel')
def wheel():
    """
    Wheel of Fortune page
    """

    attendees = Pythonista.select().where(Pythonista.check_in >= datetime.datetime.now().strftime('%Y-%m-%d'))
    segments = []
    for attendee in attendees:
        segments.append({'fillStyle': random_color(), 'text': attendee.name[:15], 'full_name': attendee.name})

    return render_template('wheel.html', segments=segments)


@app.route('/webhook', methods=['POST'])
def eventbrite_event_hook():
    """
    Eventbrite webhook: configure it into the eventbrite account
    """

    hook = Box(request.json)
    app.logger.info("{action} user {user_id} {api_url}".format(
        action=hook.config.action,
        user_id=hook.config.user_id,
        api_url=hook.api_url)
    )

    user = Box(eb_client.get_user(hook.config.user_id))
    with db.transaction():
        Pythonista.create(name=user.name,
                          email=user.emails[0].email,
                          eb_id=hook.config.user_id,
                          check_in=datetime.datetime.now())

    slack_notifier("Welcome {}!".format(user.name))

    return "OK"
