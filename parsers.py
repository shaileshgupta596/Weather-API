from flask_restful import reqparse
from validators import datestring

# Define the following Parsers
# NOTE: Use the custom 'datestring' validator defined in 'WeatherAPI/validators.py' for validating input date string.
# 1. WeatherRequestParser : It parses the values of input fields-  'id', 'date', 'temperature', and 'location', present in a JSON entry
## The value of 'location' field is another json entry, whose values are parsed by LocationParser
WeatherRequestParser = reqparse.RequestParser()
WeatherRequestParser.add_argument("id",type=int,location = 'json',required =True)
WeatherRequestParser.add_argument("date",type= datestring ,location='json',required =True,nullable=False)
WeatherRequestParser.add_argument("location",type=dict , location = 'json',required =True)
WeatherRequestParser.add_argument('temperature' , type = list ,location = 'json',required =True)

# 2. LocationParser : It parses the values of input fields - 'lat', 'lon', 'city', and 'state', passed to 'location' field of weather JSON input entry.
LocationParser = reqparse.RequestParser()
LocationParser.add_argument("lat",type=float,required =True,location ="location")
LocationParser.add_argument("lon" ,type = float,required =True,location ="location")
LocationParser.add_argument("city" , type= str,required =True,location ="location")
LocationParser.add_argument("state" ,type= str,required =True,location ="location")
# 3. WeatherGetParser : It parses the values of input fields - 'date', 'lat' and 'lon', present in a query string.
WeatherGetParser = reqparse.RequestParser()
WeatherGetParser.add_argument('date',type = datestring ,location = "args")
WeatherGetParser.add_argument('lat',type=float,location="args")
WeatherGetParser.add_argument('lon',type=float,location="args")

# 4. WeatherEraseParser : It parses the values of input fields - 'start', 'end', 'lat' and 'lon', present in  a query string
WeatherEraseParser = reqparse.RequestParser()
WeatherEraseParser.add_argument('start',type = datestring, location = "args")
WeatherEraseParser.add_argument('end',type = datestring, location = "args")
WeatherEraseParser.add_argument('lat',type = float, location = "args")
WeatherEraseParser.add_argument('lon',type = float, location = "args")
# 5. TemperatureGetParser : It parses the values of input fields - 'start', 'end', present in  a query string
TemperatureGetParser = reqparse.RequestParser()
TemperatureGetParser.add_argument('start',type = datestring ,required =True ,location ="args")
TemperatureGetParser.add_argument('end',type = datestring ,required =True ,location ="args")
# 6. PreferredLocationsParser : It parses the values of input fields - 'date', 'lat' and 'lon', present in  a query string
PreferredLocationsParser = reqparse.RequestParser()
PreferredLocationsParser.add_argument('date',type= datestring ,required =True, location = "args")
PreferredLocationsParser.add_argument('lat',type= float ,required =True, location = "args")
PreferredLocationsParser.add_argument('lon',type= float ,required =True, location = "args")
