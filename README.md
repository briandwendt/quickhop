## QuickHop - Find Flights Fast

Quickhop is a fast and lightweight airline flights search tool designed to
meet the needs of non-revenue travelers and commuters.

#### Key Components

* Written in Python using the [Flask web framework](http://flask.pocoo.org).
* Flight data in JSON format from [FlightStats API](https://developer.flightstats.com/).
* [Materialize.css](http://materializecss.com/) responsive front-end framework.
* Runs on [Google App Engine](https://cloud.google.com/appengine/).

#### To Run Locally

Download or clone this repo, then navigate to the `quickhop-mobile` directory and run

    pip install -r requirements.txt -t lib/

This will install all required dependencies into the `lib` subdirectory, a requirement
for getting things to work on Google App Engine.

You'll need to download and install the [Google App Engine SDK for Python](https://cloud.google.com/appengine/downloads), after which you can run

    dev_appserver.py .

This starts the development server on your local machine. QuickHop should now be running on
`http://localhost:8080`.

