# -*- coding=utf-8 -*-

import os
import random
from notifiers import get_notifier


def random_color():
    """
    Random CSS color, HEX format
    """

    letters = '0123456789ABCDEF'
    return '#' + ''.join([letters[int(random.random() * 16)] for x in range(6)])


def slack_notifier(message):
    if not os.environ['FLASK_DEBUG']:
        p = get_notifier('slack')
        p.notify(webhook_url=os.environ['SLACK_WEB_HOOK'], message=message)
