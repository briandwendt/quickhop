from flask_wtf import Form, RecaptchaField
from wtforms import StringField, DateField, TextAreaField
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

    # See /static/js/init.js for datepicker parameters
    date = DateField(format='%Y/%m/%d')


class Contact(Form):
    name = StringField('Name', validators=[
        Length(max=50), Required(message=u'A name. Any name will do.') ])
    message = TextAreaField('Comments',
        validators=[ Required(message=u'You really should say SOMEthing.') ])
    recaptcha = RecaptchaField()
