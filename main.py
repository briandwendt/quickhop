# Flask microframework
from flask import Flask, request, redirect, render_template, url_for, flash
from forms import FindFlights
from secret_keys import CSRF_SECRET_KEY, FS_APP_ID, FS_APP_KEY

# HTTP Requests and datetime utilities
import requests
from datetime import datetime
import dateutil.parser

# Create a new Flask app
app = Flask(__name__)

# Date & time filters
@app.template_filter()
def as_time(value, format='%l:%M'):
    """ Converts ISO-8601 format datetime to HH:MM. """
    return dateutil.parser.parse(value).strftime(format)

@app.template_filter()
def am_pm(value, format='%p'):
    """ Converts ISO-8601 format datetime to AM/PM. """
    return dateutil.parser.parse(value).strftime(format)

@app.template_filter()
def as_date(value, format='%B %d, %Y'):
    """ Converts ISO-8601 format datetime to prettified date. """
    return dateutil.parser.parse(value).strftime(format)

app.jinja_env.filters['as_time'] = as_time
app.jinja_env.filters['as_date'] = as_date
app.jinja_env.filters['am_pm'] = am_pm

# Configure the app
app.config['DEBUG'] = True
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = CSRF_SECRET_KEY

# Define the routes
# TODO: move these to views.py ?
# TODO: move business logic to models.py ?

@app.route('/', methods=('GET', 'POST'))
def search():
    """

    The main flights search page.

    """

    # Forms are in forms.py
    form = FindFlights()

    # If the completed form validates, show the flights list
    if request.method == 'POST' and form.validate_on_submit():
        return redirect(url_for('flights',
            origin = request.form['origin'].upper(),
            destination = request.form['destination'].upper(),
            year = request.form['year'],
            month = request.form['month'],
            day = request.form['day']))

    # Render the flights search form
    return render_template('search.html', form=form)

@app.route('/thanks')
def thanks():
    """

    Thanks for your donation!

    """

    return render_template('thanks.html')


@app.errorhandler(404)
def page_not_found(e):
    """

    Custom 404 message.

    """
    return 'Sorry, nothing at this URL.', 404


@app.route('/flights/<origin>/<destination>/<year>/<month>/<day>/')
def flights(origin, destination, year, month, day):
    """

    The flights list page.

    """

    # FlightStats API: "Flight Status by Route"
    fs_url = 'https://api.flightstats.com/flex/flightstatus/rest/v2/json/route/status/'
    fs_url = fs_url + '{orig}/{dest}/dep/{year}/{month}/{day}'\
        .format(orig=origin,dest=destination,year=year,month=month,day=day)
    fs_params = {'appId': FS_APP_ID,
                 'appKey': FS_APP_KEY,
                 'hourOfDay': 0,
                 'utc': 'false',
                 'numHours': 24,
                 'codeType': 'IATA',
                 'extendedOptions': 'useInlinedReferences'}

    # Send and store the HTTP GET request
    r = requests.get(fs_url, params=fs_params)

    # Build the flights dict
    flights = r.json()

    # If there are errors, return to the search form
    if "error" in flights:
        flash(flights['error']['errorMessage'])
        return redirect(url_for('search'))

    # Render the flights list page
    return render_template('flights.html', flights=flights)
