# Flask microframework
from flask import Flask, request, redirect, render_template, url_for, flash
from forms import FindFlights, Contact
from config import CSRF_SECRET_KEY, FS_APP_ID, FS_APP_KEY, APP_EMAIL, \
                   ADMIN_EMAIL, RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY

# Google AppEngine Mail Python API
from google.appengine.api import mail

# HTTP Requests and datetime utilities
import requests
import dateutil.parser
from datetime import datetime

# Create a new Flask app
app = Flask(__name__)

# Date & time filters for Jinja
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
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY

# Define the routes

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
            origin = request.form['origin'].upper().strip(),
            destination = request.form['destination'].upper().strip(),
            year = request.form['date'].split('/')[0],
            month = request.form['date'].split('/')[1],
            day = request.form['date'].split('/')[2]))
    elif request.method == 'POST':
        flash('Please correct the following errors:')

    # Render the flights search form
    return render_template('search.html', form=form)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # Forms are in forms.py
    form = Contact()

    if request.method == 'POST' and form.validate_on_submit():
        # Google App Engine Mail Python API
        message = mail.EmailMessage(
            sender="{0} {1}".format(request.form['name'], APP_EMAIL),
                      to=ADMIN_EMAIL,
                      subject="QuickHop Feedback",
                      body=request.form['message'])
        message.send()

        flash('Your message has been sent!', 'success')
        return redirect(url_for('search'))
    elif request.method == 'POST':
        flash('Please correct the following errors:', 'error')

    return render_template('contact.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


@app.errorhandler(404)
def page_not_found(e):
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

    # If no HTTP response, return to the search form
    if r.status_code != 200:
        flash('Flights data unavailable at this time.')
        return redirect(url_for('search'))

    # Build the flights dict
    flights = r.json()

    # For local testing without API requests:
    # import json
    # f = open("sample_response.json", "r")
    # flights = json.loads(f.read())
    # f.close()

    # If there are errors, return to the search form
    if 'error' in flights:
        flash(flights['error']['errorMessage'], 'error')
        return redirect(url_for('search'))

    # Count the flights
    if 'flightStatuses' in flights:
        count = 0
        for flight in flights['flightStatuses']:
            count += 1
    else:
        flash('No flights found for {0} to {1}.'.format(origin, destination), 'error')
        return redirect(url_for('search'))

    if count == 0:
        flash('No flights found for {0} to {1}.'.format(origin, destination), 'error')
        return redirect(url_for('search'))

    # Render the flights list page
    return render_template('flights.html', flights=flights, count=count)
