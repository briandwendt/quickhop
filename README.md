# QuickHop

QuickHop is a fast and lightweight airline flights search tool designed to
meet the needs of non-revenue travelers and airline commuters.

QuickHop is live at [QuickHop.info](http://quickhop.info/).

#### Key Components

* Written in Python using the [Flask web framework](http://flask.pocoo.org).
* Flight data in JSON format from [FlightStats API](https://developer.flightstats.com/).
* [Materialize.css](http://materializecss.com/) responsive front-end framework.
* Runs on [Google App Engine](https://cloud.google.com/appengine/).

#### To Run Locally

Download or clone this repo, then navigate to the `quickhop-mobile` directory and run

    pip install -r requirements.txt -t lib/

This will install all required dependencies into the `lib` subdirectory, a necessary step
for getting things to work on Google App Engine.

Next you'll need to manually create the `config.py` file, which should look something
like the following:

    # CSRF for Flask-WTF
    CSRF_SECRET_KEY = 'supersecretjibberish'

    # FlightStats API
    FS_APP_ID = 'YOUR_FLIGHTSTATS_APP_ID'
    FS_APP_KEY = 'YOUR_FLIGHTSTATS_APP_KEY'

    # Admin & AppEngine emails for contact form
    ADMIN_EMAIL = 'Your Name <you@example.com>'
    APP_EMAIL = '<no-reply@YOUR_GOOGLE_APP_ID.appspotmail.com>'

    # Recaptcha for contact form
    # https://www.google.com/recaptcha/
    RECAPTCHA_PUBLIC_KEY = 'YOUR_RECAPTCHA_SITE_KEY'
    RECAPTCHA_PRIVATE_KEY = 'YOUR_RECAPTCHA_SECRET_KET'


Finally you'll need to download and install the [Google App Engine SDK for Python](https://cloud.google.com/appengine/downloads), after which you can run

    dev_appserver.py .

This starts the development server on your local machine. QuickHop should now be running on
`http://localhost:8080`.

