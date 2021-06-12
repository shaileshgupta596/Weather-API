import re
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#db = SQLAlchemy()
#migrate = Migrate()

# Define two models : Location and Weather

# Location Model must contain the following attributes.
#    'id' - a primary key holding Integer value
#    'lat' - Float field
#    'lon' - Float field
#    'city' - String field of maximum length 100 characters.
#    'state' - String field of maximum length 100 characters.


# Weather Model must contain the following attributes.
#    'id' - a primary key holding Integer value
#    'date' - Date Time Field
#    '_temperature' - A string field to store 24 temperature values, separated by semicolon (';').
# Define a property named 'temparature', whose getter method returns 24 temperature values in a list and
# setter method sets the joined temperature string to '_temperature'

# Establish one to many relationship between Location and Weather models.
# A location object must able to access associated weather details of the location using 'weathers' attribute, and
# A weather object must able to access associated location details using 'location' attribute.

class Location(db.Model):
    __tablename__ = "location"
    id = db.Column('location_id', db.Integer, primary_key = True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    weathers = db.relationship('Weather',backref='loc')
    '''
    def __init__(self,lat,lon,city,state):
        self.lat = lat 
        self.lon = lon 
        self.city = city 
        self.state = state
    '''

class Weather(db.Model):
    __tablename__ = "weather"
    id = db.Column('weather_id', db.Integer, primary_key = True)
    date = db.Column(db.Date)
    _temperature = db.Column(db.String(500))
    locations = db.Column(db.Integer , db.ForeignKey('location.location_id'))
    '''

    def __init__(self,date,temparature=""):
        self.date = date
        self._temperature = temparature
    '''

    def get_temperature(self):
        return self._temperature

    def set_temperature(self,x):
        x = [str(temp) for temp in x ]
        self._temperature = ";".join(x)

