# -*- coding: utf-8 -*-
from coverage import coverage

cov = coverage(branch=True, omit=['*/flask/*',
                                  '*/click/*',
                                  '*/jinja2/*',
                                  '*/werkzeug/*',
                                  '*/itsdangerous.py',
                                  '*/markupsafe/*',
                                  'tests.py'])
cov.start()

import os  # noqa
import unittest  # noqa
from unittest.mock import patch, MagicMock  # noqa
from config import URL_EVENTS  # noqa
from pyglialo import PyGlialo, get_data_from_url  # noqa
from flask_pyGlialo import *  # noqa


def fake_data_empty(url):
    return {}


def fake_data_load(url):
    venue = {
        'lat': 45.49055480957031,
        'address_1': 'Via Giulio e Corrado Venini, 42',
        'country': 'it',
        'city': 'Milano',
        'repinned': False,
        'localized_country_name': 'Italy',
        'id': 24633392,
        'lon': 9.215377807617188,
        'name': 'Mikamai/LinkMe'
    }
    event = {
        'name': "Python Mashup! Casi d'uso: virtualenv, Fabric, uWSGI, ngnix, Vagrant...",
        'event_url': 'http://www.meetup.com/Python-Milano/events/235147743/',
        'time': 1480528800000,
        'id': '235147743'
    }
    group = {
        'join_mode': 'open',
        'urlname': 'Python-Milano',
        'group_lat': 45.459999084472656,
        'id': 8923782,
        'created': 1478519732926,
        'group_lon': 9.1899995803833
    }
    if url == URL_EVENTS:
        return [{
            'rsvp_limit': 50,
            'visibility': 'public',
            'created': 1477550982000,
            'updated': 1478255480000,
            'description': '...',
            'time': 1480528800000,
            'name': "Python Mashup! Casi d'uso: virtualenv, Fabric, uWSGI, ngnix, Vagrant...",
            'waitlist_count': 0,
            'utc_offset': 3600000,
            'yes_rsvp_count': 2,
            'link': 'http://www.meetup.com/Python-Milano/events/235147743/',
            'group': {
                'who': 'Pythonista',
                'created': 1371202502000,
                'id': 8923782,
                'lat': 45.459999084472656,
                'urlname': 'Python-Milano',
                'name': 'Python Milano',
                'lon': 9.1899995803833,
                'join_mode': 'open'
            },
            'duration': 7200000,
            'status': 'upcoming',
            'how_to_find_us': 'vagrant fabric python postgres uwsgi devops',
            'venue': venue,
            'id': '235147743'
        }]
    else:
        return {
            'meta': {
                # not under test
            },
            'results': [
                {
                    'member': {
                        'name': 'Antani Tatablinda',
                        'member_id': 1
                    },
                    'rsvp_id': 1,
                    'group': group,
                    'event': event,
                    'response': 'yes',
                    'guests': 0,
                    'mtime': 1478498756000,
                    'member_photo': {
                        'base_url': 'http://photos4.meetupstatic.com',
                        'thumb_link': 'http://photos4.meetupstatic.com/photos/member/0/0/0/8/thumb_1.jpeg',
                        'photo_link': 'http://photos2.meetupstatic.com/photos/member/c/a/c/8/member_1.jpeg',
                        'type': 'member',
                        'photo_id': 101
                    },
                    'venue': venue,
                    'created': 1478498756000
                },
                {
                    'member': {
                        'name': 'Arnoldo Truffaldoni',
                        'member_id': 2
                    },
                    'rsvp_id': 1638255364,
                    'group': group,
                    'event': event,
                    'response': 'no',
                    'guests': 0,
                    'mtime': 1478468670000,
                    'member_photo': {
                        'base_url': 'http://photos3.meetupstatic.com',
                        'thumb_link': 'http://photos3.meetupstatic.com/photos/member/0/0/7/thumb_2.jpeg',
                        'highres_link': 'http://photos3.meetupstatic.com/photos/member/0/0/7/highres_2.jpeg',
                        'photo_id': 102,
                        'photo_link': 'http://photos3.meetupstatic.com/photos/member/0/0/7/member_2.jpeg',
                        'type': 'member'
                    },
                    'venue': venue,
                    'created': 1478468670000
                },
                {
                    'member': {
                        'name': 'Tatablinda Tapioca',
                        'member_id': 3
                    },
                    'rsvp_id': 3,
                    'group': group,
                    'event': event,
                    'response': 'yes',
                    'guests': 0,
                    'mtime': 1478312467000,
                    'member_photo': {
                        'base_url': 'http://photos1.meetupstatic.com',
                        'thumb_link': 'http://photos1.meetupstatic.com/photos/member/0/0/0/2/thumb_3.jpeg',
                        'highres_link': 'http://photos1.meetupstatic.com/photos/member/0/0/0/2/highres_3.jpeg',
                        'photo_id': 103,
                        'photo_link': 'http://photos1.meetupstatic.com/photos/member/0/0/0/2/member_3.jpeg',
                        'type': 'member'
                    },
                    'venue': venue,
                    'created': 1478312467000
                }
            ]
        }


def fake_randint():
    return 1


class TestGetDataFromUrl(unittest.TestCase):
    @patch('json.loads', return_value='some json')
    @patch('urllib.request.urlopen', return_value=MagicMock())
    def test_func_call(self, urllib_patched, json_patched):
        get_data_from_url('some_url')
        urllib_patched.assert_called_with('some_url')


class TestPyGlialo(unittest.TestCase):
    def test_create_pyglialo(self):
        self.assertIsNone(PyGlialo.event)
        self.assertIsNone(PyGlialo.event_id)
        self.assertIsNone(PyGlialo.event_rsvps)
        self.assertIsNone(PyGlialo.list_of_winners)
        self.assertIsNone(PyGlialo.winner)

    @patch('pyglialo.get_data_from_url', side_effect=fake_data_empty)
    def test_load_meetup_data_empty_response(self, fake_data):
        py = PyGlialo()
        py.load_meetup_data()
        self.assertEqual(py.event, {})
        self.assertIsNone(py.event_id)
        self.assertEqual(py.event_rsvps, {})
        self.assertEqual(py.list_of_winners, [])

    @patch('pyglialo.get_data_from_url', side_effect=fake_data_load)
    def test_load_meetup_data_nearest_meetup(self, fake_data):
        py = PyGlialo()
        py.load_meetup_data()
        self.assertEqual(py.event.get('id', None), '235147743')
        self.assertEqual(py.event_id, '235147743')
        self.assertEqual(len(py.event_rsvps), 2)
        self.assertEqual(py.list_of_winners, [])

    def test_remove_rsvp(self):
        py = PyGlialo()
        py.event_rsvps = {'results': [{
            'member': {
                'name': 'Antani Tatablinda',
                'member_id': 1
            },
        }]}
        py.remove_rsvp(1)
        self.assertEqual(len(py.event_rsvps['results']), 0)

    def test_remove_rsvp_not_in_list(self):
        py = PyGlialo()
        py.event_rsvps = {'results': [{
            'member': {
                'name': 'Foobar',
                'member_id': 1
            },
        }]}
        py.remove_rsvp(42)
        self.assertEqual(len(py.event_rsvps['results']), 1)

    def test_extract_winner(self):
        py = PyGlialo()
        py.event_rsvps = {'results': [{
            'member': {
                'name': 'Foobar',
                'member_id': 1
            },
            'response': 'yes'
        }]}
        py.extract_safe_winner()
        self.assertEqual(py.winner['name'], 'Foobar')
        self.assertEqual(py.winner['member_id'], 1)

    @patch('random.randint', return_value=0)
    def test_extract_winner_no_rsvp(self, random_patched):
        py = PyGlialo()
        py.event_rsvps = {'results': [
            {
                'member': {
                    'name': 'Foobar',
                    'member_id': 1
                },
                'response': 'no'
            },
            {
                'member': {
                    'name': 'Barfoo',
                    'member_id': 2
                },
                'response': 'yes',
                'member_photo': {
                    'photo_link': 'http://photos1.meetupstatic.com/photos/member/0/0/0/2/member_3.jpeg',
                },
            }
        ]}
        py.extract_safe_winner()
        self.assertEqual(len(py.event_rsvps['results']), 0)
        self.assertEqual(py.winner['name'], 'Barfoo')
        self.assertEqual(py.winner['member_id'], 2)
        self.assertEqual(py.winner['photo_url'], 'http://photos1.meetupstatic.com/photos/member/0/0/0/2/member_3.jpeg')

    def test_extract_winner_no_photo(self):
        py = PyGlialo()
        py.event_rsvps = {'results': [
            {
                'member': {
                    'name': 'Foobar',
                    'member_id': 1
                },
                'response': 'yes'
            }
        ]}
        py.extract_safe_winner()
        self.assertEqual(len(py.event_rsvps['results']), 0)
        self.assertEqual(py.winner['name'], 'Foobar')
        self.assertEqual(py.winner['member_id'], 1)
        self.assertEqual(py.winner['photo_url'], '/static/img/no_image.png')

    def test_extract_winner_empty_rsvps(self):
        py = PyGlialo()
        py.extract_safe_winner()
        self.assertIsNone(py.winner)


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: {}/tmp/coverage/index.html".format(os.path.join(os.path.abspath(os.path.dirname(__file__)))))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
