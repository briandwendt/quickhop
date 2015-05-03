from flask_wtf import Form
from wtforms import StringField, SelectField, DateField
from wtforms.validators import InputRequired, Length

class FindFlights(Form):
    origin = StringField('Departure Airport Code', validators=[
        InputRequired(),
        Length(min=3, max=3, message=(u'Must be a 3-letter IATA code (e.g., BOS)'))
    ])
    destination = StringField('Arrival Airport Code', validators=[
        InputRequired(),
        Length(min=3, max=3, message=(u'Must be a 3-letter IATA code (e.g., DEN)'))
    ])
    date = DateField('Date', format='%Y-%m-%d', validators=[
        InputRequired()
    ])