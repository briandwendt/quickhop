# Flask microframework
from flask import Flask, request, redirect, render_template, url_for, flash
from forms import FindFlights
from secret_keys import CSRF_SECRET_KEY, QPX_API_KEY

# Google API Client Library
from apiclient.discovery import build
import simplejson as json

# Create a new Flask app
app = Flask(__name__)

# Configure the app
app.config['DEBUG'] = True
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = CSRF_SECRET_KEY


# Define the routes
@app.route('/', methods=('GET', 'POST'))
def search():
    """The main flights search page."""

    # Forms are in forms.py
    form = FindFlights()

    # If the completed form validates, show the flights list
    if request.method == 'POST' and form.validate_on_submit():
        flash("Successfully validated!")
        return redirect(url_for('flights',
            origin = request.form['origin'].upper(),
            destination = request.form['destination'].upper(),
            year = request.form['year'],
            month = request.form['month'],
            day = request.form['day']))

    # Render the flights search form
    flash(form.errors)
    return render_template('search.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.route('/flights/<origin>-<destination>/<year>-<month>-<day>/')
def flights(origin, destination, year, month, day):
    """The flights list page."""

    # Google QPX Express API + Google API Client Library
    #   https://developers.google.com/qpx-express/
    #   https://developers.google.com/api-client-library/python/

    # Build the QPX Express API service object
    #qpx = build('qpxExpress', 'v1', developerKey=QPX_API_KEY)

    # Format the date for our precious QPX
    date_formatted = "{0}-{1}-{2}".format(year, month, day)

    # Build the JSON request
    request = {"request": {
                        "passengers": {
                            "adultCount": 1
                        },
                        "slice": [
                            {
                                "origin": origin,
                                "destination": destination,
                                "date": date_formatted,
                                "maxStops": 0
                            },
                        ]}
                    }

    # Correctly format the QPX API request - no docs on this anywhere, BTW
    #qpx_request = qpx.trips().search(body=request)

    # Execute the API request
    #qpx_response = qpx_request.execute()

    # Render the flights list page
    return render_template('flights.html', orig=origin, dest=destination)
    #return "<pre>%s</pre>" % json.dumps(qpx_response, sort_keys=True, indent=4)


