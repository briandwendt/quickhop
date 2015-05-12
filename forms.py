from flask_wtf import Form, RecaptchaField
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import Length, Required, Email
from datetime import date, time, datetime, timedelta

def strip_whitespace(s):
    if isinstance(s, basestring):
        s = s.strip()
    return s 


class FindFlights(Form):
    origin = StringField('Departure Airport', validators=[
        Length(min=3, max=3, message=(u'3-letter IATA code'))
        ], filters=[strip_whitespace])

    destination = StringField('Arrival Airport', validators=[
        Length(min=3, max=3, message=(u'3-letter IATA code'))
        ], filters=[strip_whitespace])

    # This mostly corrects for UTC -- as long as the user is in CDT :/
    # TODO: Get user's locale (if this is even really possible)
    today = datetime.today() - timedelta(hours=5)

    # List only this year, +/- 1 year
    year = SelectField('Year', default=str(today.year),
        choices=[(str(today.year-1), str(today.year-1)),
                 (str(today.year+0), str(today.year+0)),
                 (str(today.year+1), str(today.year+1))])

    # List only this month, +/- 1 month
    # TODO: I don't really like how we're doing this here, with the
    #       timedelta(weeks=4) crap. Seems flimsy.
    months = [(str(today.month-1), (today-timedelta(weeks=4)).strftime("%b")),
              (str(today.month), today.strftime("%b")),
              (str(today.month+1), (today+timedelta(weeks=4)).strftime("%b"))]

    month = SelectField('Month', default=today.month, choices=months)

    # List only today +3/-1 days (FlightStats +3/-7 search limitation)
    days = [( (today+timedelta(days=i)).strftime('%d'),
           (today+timedelta(days=i)).strftime('%d') ) for i in range(-1,3)]

    day = SelectField('Day', default=today.day, choices=days)


class Contact(Form):
    name = StringField('Name', validators=[
        Length(max=50), Required(message=u'A name. Any name will do.') ])
    message = TextAreaField('Comments',
        validators=[ Required(message=u'You really should say SOMEthing.') ])
    recaptcha = RecaptchaField()
