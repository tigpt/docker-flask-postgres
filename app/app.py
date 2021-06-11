from elasticapm.contrib.flask import ElasticAPM
import os

from flask import Flask, request, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
apm = ElasticAPM(APP)
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

APP.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%s:%s@%s/%s' % (
    # ARGS.dbuser, ARGS.dbpass, ARGS.dbhost, ARGS.dbname
    os.environ['DBUSER'], os.environ['DBPASS'], os.environ['DBHOST'], os.environ['DBNAME']
)

# initialize the database connection
DB = SQLAlchemy(APP)

# initialize database migration management
MIGRATE = Migrate(APP, DB)

from models import *


@APP.route('/')
def view_registered_guests():
    guests = Guest.query.all()
    return render_template('guest_list.html', guests=guests)

@APP.route('/bad_query')
def view_registered_guests_bad_query():
    for _ in range(20):
        guests = Guest.query.all()
    return render_template('guest_list.html', guests=guests)


@APP.route('/register', methods = ['GET'])
def view_registration_form():
    return render_template('guest_registration.html')


@APP.route('/register', methods = ['POST'])
def register_guest():
    name = request.form.get('name')
    email = request.form.get('email')
    partysize = request.form.get('partysize')
    if not partysize or partysize=='':
        partysize = 1

    guest = Guest(name, email, partysize)
    DB.session.add(guest)
    DB.session.commit()

    return render_template('guest_confirmation.html',
        name=name, email=email, partysize=partysize)

# error message
@APP.route('/hello')
def apm_message_hello():
    apm.capture_message('hello, world!')
    return render_template('apm_hello.html')

# Error
@APP.route('/error')
def apm_error():
    try:
        1 / 0
    except ZeroDivisionError:
        apm.capture_exception()
    return render_template('apm_error.html')

# Unhandled error
@APP.route('/fatal_error')
def apm_fatal_error():
    1 / 0
    return render_template('apm_error.html')