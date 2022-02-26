from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt import jwt_required
import os
import logging
from marshmallow import ValidationError

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# Get All GuestBooks
@jwt_required
@app.route('/api/guestbooks', methods=['GET'])
def get_guestbooks():
    from guestbooks.model import GuestBook
    from guestbooks.schemas import guestbook_schema

    all_g_books = GuestBook.query.all()

    return jsonify(guestbook_schema.dump(all_g_books, many=True))


# Create a GuestBook Entry
@jwt_required
@app.route('/api/guestbook', methods=['GET', 'POST'])
def create_guestbook_entry():
    from guestbooks.model import GuestBook
    from guestbooks.schemas import guestbook_schema, register_guestbook_schema

    try:
        data = register_guestbook_schema.load(request.json)
    except ValidationError as err:
        errors = err.messages
        response = {'error': errors}
        logging.error('GuestBook cannot be registered due to schema errors.')
        return jsonify(response), 422

    guestbook = GuestBook(name=data['name'],
                          message=data['message'],
                          subject=data['subject'])

    db.session.add(guestbook)
    db.session.commit()
    logging.info('GuestBook has been sent.')

    return guestbook_schema.jsonify(guestbook)


# Delete a GuestBook
@jwt_required
@app.route('/api/guestbooks/<id>', methods=['DELETE'])
def delete_guestbook(id):
    from guestbooks.model import GuestBook
    from guestbooks.schemas import guestbook_schema

    guestbook = GuestBook.query.get(id)
    if guestbook is None:
        logging.error('GuestBook to be deleted is not found.')
        return jsonify({'msg': 'GuestBook to be deleted is not found.'}), 404

    db.session.delete(guestbook)
    db.session.commit()
    logging.info(f'GuestBook #({id}) has been deleted.')
    return guestbook_schema.jsonify(guestbook)


# Run Server
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
