#!/usr/bin/python3
""" Starts a Flask Web Application """

from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from os import environ
from flask import Flask, url_for, render_template
import uuid


app = Flask(__name__)
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'


@app.teardown_appcontext
def teardown_db(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/3-hbnb')
def hbnb_filters(the_id=None):
    """ request to custom template with states, cities & amentities """
    state_objs = storage.all('State').values()
    states = dict([state.name, state] for state in state_objs)
    amenities = storage.all('Amenity').values()
    places = storage.all('Place').values()
    users = dict([user.id, "{} {}".format(user.first_name, user.last_name)]
                 for user in storage.all('User').values())
    return render_template('3-hbnb.html',
                           states=states,
                           amenities=amenities,
                           places=places,
                           users=users,
                           cache_id=uuid.uuid4())


if __name__ == "__main__":
    """ Main Function """
    app.run(host=host, port=port)
