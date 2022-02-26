from app import db


# GuestBook Class/Model
class GuestBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    message = db.Column(db.String(200))
    subject = db.Column(db.String(100))

    def __init__(self, name, message, subject):
        self.name = name
        self.message = message
        self.subject = subject
