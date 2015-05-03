from flask import Flask, request, redirect, render_template, url_for, flash
from forms import FindFlights
from secret_keys import CSRF_SECRET_KEY

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = CSRF_SECRET_KEY


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/', methods=('GET', 'POST'))
def search():
    """The main flights search page."""
    form = FindFlights()
    if request.method == 'POST':
        return redirect(url_for('flights',
            origin = request.form['origin'].upper(),
            destination = request.form['destination'].upper(),
            date = request.form['date']))
    return render_template('search.html', form=form)


@app.route('/flights/<origin>/<destination>/<date>/')
def flights(origin, destination, date):
    return 'Here is the flights list.'


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
