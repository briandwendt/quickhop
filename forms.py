from flask_wtf import Form
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

    # This is the SERVER date (in UTC), maybe not quite right to use this.
    # We really need the LOCALE from of the user's device...
    today = datetime.today()

    # List only this year, +/- 1 month
    year = SelectField('Year', default=str(today.year),
        choices=[(str(today.year-1), str(today.year-1)),
                 (str(today.year+0), str(today.year+0)),
                 (str(today.year+1), str(today.year+1))])

    # List only this month, +/- 1 month
    months = [(str(today.month-1), (today-timedelta(weeks=4)).strftime("%b")),
              (str(today.month), today.strftime("%b")),
              (str(today.month+1), (today+timedelta(weeks=4)).strftime("%b"))]

    month = SelectField('Month', default=today.month, choices=months)

    # List only today +3/-7 days (FlightStats search limitation)
    days = [( (today+timedelta(days=i)).strftime('%d'),
           (today+timedelta(days=i)).strftime('%d') ) for i in range(-1,3)]

    day = SelectField('Day', default=today.strftime("%d"), choices=days)


class Contact(Form):

    # 
    # TODO:
    #
    # We need a recaptcha or some kind of anti-bot-spam thing here...
    #

    name = StringField('Name', validators=[
        Length(max=50), Required(message=u'A name. Any name will do.') ])
    email = StringField('Email',
        validators=[ Email(message=u'Please provide a valid email address.') ])
    message = TextAreaField('Comments',
        validators=[ Required(message=u'You really should say SOMEthing.') ])

