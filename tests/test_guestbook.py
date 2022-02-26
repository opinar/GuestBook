import unittest
import pytest
from app import app as flask_app
import json
from guestbooks.model import GuestBook


@pytest.mark.usefixtures("all_guestbooks")
class GuestBookTestCase(unittest.TestCase):
    def test_get_all_guestbooks(self):
        # Lists all guestbooks
        tester = flask_app.test_client(self)
        response = tester.get('/api/guestbooks')

        data = json.loads(response.data)
        assert len(data) > 0

    def test_create_guestbook_no_name(self):
        # Name required
        params = json.dumps({"name": "",
                             "subject": "Leo integer malesuada",
                             "message": "Cum sociis natoque penatibus et magnis dis parturient montes."})
        tester = flask_app.test_client(self)
        tester.post('/api/guestbook', headers={"Content-Type": "application/json"}, data=params)

        # GuestBook cannot be created
        guestbook = GuestBook.query.filter_by(subject='Leo integer malesuada').first()
        assert guestbook is None

    def test_create_guestbook_no_subject(self):
        # Subject required
        params = json.dumps({"name": "The Muse",
                             "subject": "",
                             "message": "Cum sociis natoque penatibus et magnis dis parturient montes."})
        tester = flask_app.test_client(self)
        tester.post('/api/guestbook', headers={"Content-Type": "application/json"}, data=params)

        # GuestBook cannot be created
        guestbook = GuestBook.query.filter_by(name='The Muse').first()
        assert guestbook is None

    def test_create_guestbook_no_message(self):
        # Message required
        params = json.dumps({"name": "The Muse",
                             "subject": "Leo integer malesuada",
                             "message": ""})
        tester = flask_app.test_client(self)
        tester.post('/api/guestbook', headers={"Content-Type": "application/json"}, data=params)

        # GuestBook cannot be created
        guestbook = GuestBook.query.filter_by(name='The Muse').first()
        assert guestbook is None

    def test_create_guestbook_successful(self):
        # Valid parameters
        params = json.dumps({"name": "The Muse",
                             "subject": "Leo integer malesuada",
                             "message": "Cum sociis natoque penatibus et magnis dis parturient montes."})
        tester = flask_app.test_client(self)
        res = tester.post('/api/guestbook', headers={"Content-Type": "application/json"}, data=params)

        # GuestBook is created
        assert res.status_code == 200
        guestbook = GuestBook.query.filter_by(name='The Muse').first()
        assert guestbook is not None
        assert guestbook.subject == "Leo integer malesuada"
        assert "Cum sociis natoque penatibus" in guestbook.message

    def test_delete_guestbook_without_success(self):
        tester = flask_app.test_client(self)
        res = tester.delete('/api/guestbooks/123')

        # GuestBook is not found
        assert res.status_code == 404

    def test_delete_guestbook_with_success(self):
        guestbook = GuestBook.query.filter_by(name="Warby Parker").first()
        assert guestbook is not None

        tester = flask_app.test_client(self)
        res = tester.delete(f'/api/guestbooks/{guestbook.id}')

        # GuestBook is deleted
        assert res.status_code == 200
        guestbook = GuestBook.query.filter_by(name="Warby Parker").first()
        assert guestbook is None
