from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import Length, Required, Email
from datetime import date, time, datetime

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

    year = SelectField('Year', default=str(datetime.now().year),
        choices=[(str(datetime.now().year-1), str(datetime.now().year-1)),
                 (str(datetime.now().year+0), str(datetime.now().year+0)),
                 (str(datetime.now().year+1), str(datetime.now().year+1))])

    month = SelectField('Month', default=datetime.now().strftime("%m"),
        choices=[("01", "JAN"),("02", "FEB"),("03", "MAR"),("04", "APR"),("05", "MAY"),
                 ("06", "JUN"),("07", "JUL"),("08", "AUG"),("09", "SEP"),("10", "OCT"),
                 ("11", "NOV"),("12", "DEC")])

    day = SelectField('Day', default=datetime.now().strftime("%d"),
        choices=[("01", 1),("02", 2),("03", 3),("04", 4),("05", 5),("06", 6),("07", 7),("08", 8),("09", 9),
                 ("10", 10),("11", 11),("12", 12),("13", 13),("14", 14),("15", 15),("16", 16),
                 ("17", 17),("18", 18),("19", 19),("20", 20),("21", 21),("22", 22),("23", 23),
                 ("24", 24),("25", 25),("26", 26),("27", 27),("28", 28),("29", 29),("30", 30),
                 ("31", 31)])


class Feedback(Form):
    name = TextAreaField('Name')
    email = TextAreaField('Email', validators=[
        Required(),
        Email()
        ])
    message = TextAreaField('Message', validators=[
        Required()
        ])
    submit = SubmitField('Send Feedback')
