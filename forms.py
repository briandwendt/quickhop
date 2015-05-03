from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class FindFlights(Form):
    origin = StringField('Departure Airport Code', validators=[DataRequired()])
    destination = StringField('Arrival Airport Code', validators=[DataRequired()])