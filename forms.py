from flask_wtf import Form
from wtforms import StringField, SelectField, DateField, SubmitField
from wtforms.validators import Length
from datetime import date

class FindFlights(Form):
    origin = StringField('Departure Airport Code', validators=[
        Length(min=3, max=3, message=(u'Must be a 3-letter IATA code.'))
    ])
    destination = StringField('Arrival Airport Code', validators=[
        Length(min=3, max=3, message=(u'Must be a 3-letter IATA code.'))
    ])
    date = DateField('Date', default=date.today())