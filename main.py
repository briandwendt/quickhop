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


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/', methods=('GET', 'POST'))
def search():
    """The main flights search page."""
    form = FindFlights()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect(url_for('flights',
            origin = request.form['origin'].upper(),
            destination = request.form['destination'].upper(),
            date = request.form['date']))
    return render_template('search.html', form=form)


@app.route('/flights/<origin>/<destination>/<date>/')
def flights(origin, destination, date):
    """The flights list page."""

    # Google's QPX Express Airfare API + Google API Client Library
    # https://developers.google.com/qpx-express/
    # https://developers.google.com/api-client-library/python/
    qpx = build('qpxExpress', 'v1', developerKey=QPX_API_KEY)
    json_request = {"request": {
                        "passengers": {
                            "adultCount": 1
                        },
                        "slice": [
                            {
                                "origin": origin,
                                "destination": destination,
                                "date": date,
                                "maxStops": 0
                            },
                        ]}
                    }
                    
    request = qpx.trips().search(body=json_request)
    response = request.execute()
    return "<pre>%s</pre>" % json.dumps(response['trips']['tripOption'], sort_keys=True, indent=4)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
