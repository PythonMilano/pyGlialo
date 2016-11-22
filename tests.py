# -*- coding: utf-8 -*-
from coverage import coverage

cov = coverage(branch=True, omit=['*/flask/*',
                                  '*/click/*',
                                  '*/jinja2/*',
                                  '*/werkzeug/*',
                                  '*/itsdangerous.py',
                                  '*/markupsafe/*',
                                  'config.py',
                                  'tests.py',
                                  'secrets.py'])
cov.exclude('if __name__ == .__main__.:')

cov.start()

import datetime  # noqa
import os  # noqa
import unittest  # noqa
from unittest.mock import patch, MagicMock, PropertyMock  # noqa

import flask_pyGlialo  # noqa
from config import URL_EVENTS  # noqa
from pyglialo import PyGlialo, get_data_from_url  # noqa


def fake_data_empty(url):
    return {}


def fake_data_load(url):
    """
    Omitted some json response that pyGlialo doesn't use
    :param url:
    :return:
    """
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
            'venue': {
                'id': 24633392,
                'name': 'Mikamai/LinkMe',
                'lat': 45.49055480957031,
                'lon': 9.215377807617188,
                'repinned': 'false',
                'address_1': 'Via Giulio e Corrado Venini, 42',
                'city': 'Milano',
                'country': 'it',
                'localized_country_name': 'Italia'
            },
            'id': '235147743'
        }]
    else:
        return [
            {
                'response': 'yes',
                'member': {
                    'id': 1,
                    'name': 'Tatablinda Tapioca',
                    'photo': {
                        'photo_link': 'http://url/to/photos/member.jpg',
                    },
                }
            },
            {
                'response': 'yes',
                'member': {
                    'id': 2,
                    'name': 'Antani Tatablinda',
                },
            },
            {
                'response': 'no',
                'member': {
                    'id': 3,
                    'name': 'Arnoldo Truffaldoni',
                    'photo': {
                        'photo_link': 'http://url/to/photos/member.jpg',
                    },
                }
            }
        ]


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
        self.assertEqual(len(py.event_rsvps), 3)
        self.assertEqual(py.list_of_winners, [])

    @patch('random.randint', return_value=0)
    def test_extract_winner(self, random_patched):
        py = PyGlialo()
        py.event_rsvps = fake_data_load('fake_data')
        py.extract_safe_winner()
        self.assertEqual(py.winner['name'], 'Tatablinda Tapioca')
        self.assertEqual(py.winner['member_id'], 1)
        self.assertEqual(len(py.event_rsvps), 2)

    @patch('random.randint', return_value=0)
    def test_extract_winner_no_rsvp(self, random_patched):
        py = PyGlialo()
        py.event_rsvps = [{
            'response': 'no',
            'member': {
                'id': 3,
                'name': 'Arnoldo Truffaldoni',
                'photo': {
                    'photo_link': 'http://url/to/photos/member.jpg',
                }
            }
        }]
        py.extract_safe_winner()
        self.assertEqual(len(py.event_rsvps), 0)

    @patch('random.randint', return_value=1)
    def test_extract_winner_no_photo(self, random_patched):
        py = PyGlialo()
        py.event_rsvps = fake_data_load('fake_data')
        py.extract_safe_winner()
        self.assertEqual(py.winner['name'], 'Antani Tatablinda')
        self.assertEqual(py.winner['member_id'], 2)
        self.assertEqual(py.winner['photo_url'], '/static/img/no_image.png')

    def test_extract_winner_empty_rsvps(self):
        py = PyGlialo()
        py.extract_safe_winner()
        self.assertIsNone(py.winner)

    def test_save_winners_list(self):
        py = PyGlialo()
        py.list_of_winners = ['antani', 'tapioca']
        py.save_winners_list()
        try:
            os.remove('winner_list_{}.txt'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
        except FileNotFoundError:
            self.fail('Something went wrong.')


class TestPyGlialoApp(unittest.TestCase):
    def setUp(self):
        self.app = flask_pyGlialo.app.test_client()

    @patch('pyglialo.PyGlialo.load_meetup_data')
    def test_index(self, piglialo_mock):
        response = self.app.get('/')
        piglialo_mock.assert_called_with()
        self.assertEqual(response.status_code, 200)

    @patch('pyglialo.PyGlialo.load_meetup_data')
    def test_reset(self, piglialo_mock):
        response = self.app.get('/reset')
        piglialo_mock.assert_called_with()
        self.assertEqual(response.status_code, 200)

    @patch('pyglialo.PyGlialo.winner')
    @patch('pyglialo.PyGlialo.extract_safe_winner')
    def test_random_winner(self, piglialo_mock, piglialo_mock_winner):
        with patch.object(PyGlialo, 'list_of_winners', new_callable=PropertyMock) as list_of_winners_mock:
            list_of_winners_mock.return_value = ['antani', 'tatablinda']
            response = self.app.get('/random')
            piglialo_mock.assert_called_with()
            self.assertEqual(response.status_code, 200)
            self.assertTrue('Rolling for goodies Number' in str(response.data))

    @patch('pyglialo.PyGlialo.extract_safe_winner')
    def test_random_no_winner(self, piglialo_mock):
        with patch.object(PyGlialo, 'list_of_winners', new_callable=PropertyMock) as list_of_winners_mock:
            list_of_winners_mock.return_value = []
            response = self.app.get('/random')
            piglialo_mock.assert_called_with()
            self.assertEqual(response.status_code, 200)
            self.assertTrue('No one else can win!!!' in str(response.data))

    def test_save_winner_already_in_list(self):
        with patch.object(PyGlialo, 'list_of_winners', new_callable=PropertyMock) as list_of_winners_mock:
            list_of_winners_mock.return_value = ['antani']
            response = self.app.get('/save/antani/')
            self.assertEqual(response.status_code, 302)

    def test_save_winner_in_list(self):
        with patch.object(PyGlialo, 'list_of_winners', new_callable=PropertyMock) as list_of_winners_mock:
            list_of_winners_mock.return_value = ['antani']
            response = self.app.get('/save/tapioca/')
            self.assertEqual(response.status_code, 302)

    def test_saved(self):
        with patch.object(PyGlialo, 'list_of_winners', new_callable=PropertyMock) as list_of_winners_mock:
            list_of_winners_mock.return_value = ['antani', 'tapioca']
            response = self.app.get('/saved')
            self.assertEqual(response.status_code, 200)
            self.assertTrue('Winner for slot 2' in str(response.data))
            self.assertTrue('tapioca' in str(response.data))

    @patch('pyglialo.PyGlialo.save_winners_list')
    def test_finalize(self, pyglialo_mock):
        with patch.object(PyGlialo, 'list_of_winners', new_callable=PropertyMock) as list_of_winners_mock:
            list_of_winners_mock.return_value = ['antani', 'tapioca']
            response = self.app.get('/finalize')
            pyglialo_mock.assert_called_with()
            self.assertEqual(response.status_code, 200)
            self.assertTrue('antani' in str(response.data))
            self.assertTrue('tapioca' in str(response.data))


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
