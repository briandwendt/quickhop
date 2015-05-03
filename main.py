from flask import Flask, render_template
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
    if form.validate_on_submit():
        return redirect('/flights')
    return render_template('search.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
