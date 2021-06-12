from flask import Flask ,request,jsonify,make_response
from flask_restful import Resource, Api ,inputs
from flask_restful import reqparse
from parsers import WeatherRequestParser,LocationParser,WeatherGetParser,WeatherEraseParser,TemperatureGetParser,PreferredLocationsParser
#from models import Location ,Weather
from methods import sthours,tfhours,extendlist,preferlocCondition,haversine

''' code by me'''
from flask_sqlalchemy import SQLAlchemy
''' code by me end'''

app = Flask(__name__)

''' code by me '''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_api.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

app.config['JSON_SORT_KEYS'] = False
''' code by me end'''

api =Api(app)

class Location(db.Model):
    __tablename__ = "location"
    id = db.Column('location_id', db.Integer, primary_key = True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    weathers = db.relationship('Weather',backref='loc')

class Weather(db.Model):
    __tablename__ = "weather"
    id = db.Column('weather_id', db.Integer, primary_key = True)
    date = db.Column(db.Date)
    _temperature = db.Column(db.String(500))
    locations = db.Column(db.Integer , db.ForeignKey('location.location_id'))

    def get_temperature(self):
        return self._temperature

    def set_temperature(self,x):
        x = [str(temp) for temp in x ]
        self._temperature = ";".join(x)


class WeatherList(Resource):
    def get(self):
        responses = []
        data = Location.query.all()

        wgp = WeatherGetParser.parse_args()
        if wgp['lat']!= None and wgp['lon']!=None:
            data = db.session.query(Location).filter(Location.lat == wgp['lat'] ,Location.lon == wgp['lon'])
            # Below condition used to check if no data found for given lat and lon
            if len([i for i in data])==0:
                return make_response(jsonify([]),404)
            # Found the data Related to given lat and lon
            for d in data:
                response = {"id":d.id,"date":d.weathers[0].date.strftime("%Y-%m-%d"),"location": {"lat": d.lat, "lon": d.lon, "city": d.city, "state": d.state},"temperature":[float(i) for i in str(d.weathers[0]._temperature).split(";")]}
                responses.append(response)
            return make_response(jsonify(responses),200)
        # Returning All the Weather DATA
        for d in data:
            response = {"id":d.id,"date":d.weathers[0].date.strftime("%Y-%m-%d"),"location": {"lat": d.lat, "lon": d.lon, "city": d.city, "state": d.state},"temperature":[float(i) for i in str(d.weathers[0]._temperature).split(";")]}
            responses.append(response)
        return make_response(jsonify(responses),200)

    def post(self):
        # Fetching data from WeatherRequestParser
        wrp = WeatherRequestParser.parse_args()
        # Fetchinf Data from Location Parser
        lp = LocationParser.parse_args(req= wrp)
        #Database Work start here
        # Condition for already Exisiting data
        check =[c for c in db.session.query(Location).filter(Location.id == wrp['id'])]
        if len(check) == 0:
            loc =  Location(lat = lp['lat'] , lon = lp['lon'], city = lp['city'] , state = lp['state'])
            wea = Weather(date = wrp['date'], loc = loc)
            wea.set_temperature(wrp['temperature'])
            # adding data to database
            db.session.add(loc)
            db.session.add(wea)
            # Commit Operation Perfomerd Here
            db.session.commit()
            return make_response(jsonify({"status": "OK","message":"Data Added Successfully ."}),201)
        return make_response(jsonify({"status": "OK","message":"Data Already Exists ."}),400)


###########################################################################################
#############################################################################################
###############################################################################################
###############################################################################################
###############################################################################################
class WeatherErase(Resource):

    def delete(self):
        wep =  WeatherEraseParser.parse_args()
        if wep['start']!= None and wep['end']!= None and wep['lat']!=None and wep['lon']!=None:
            start = wep['start'].strftime("%Y-%m-%d")
            end = wep['end'].strftime("%Y-%m-%d")
            lat = wep['lat']
            lon = wep['lon']
            #Retrive the rows which is need to be deleted 
            erase_data = db.session.query(Location).filter(Location.lat==lat ,Location.lon == lon).join(Weather).filter(Weather.date.between(start,end))
            if len([i.id for i in erase_data])==0:
                return make_response(jsonify([]),400)
            for dd in erase_data:
                Location.query.filter(Location.id == dd.id ).delete()
                Weather.query.filter(Weather.locations == dd.id ).delete()
            db.session.commit()
            dg = Weather.query.all()
            
            return make_response(jsonify({"status":"deleted","weather":len(dg)}),200)
        db.session.query(Location).delete()
        db.session.query(Weather).delete()
        db.session.commit()
        return make_response(jsonify({"status":"deleted"}),200)

###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
class LocationTemp(Resource):

    def get(self):
        responses=[]
        #Fetching data from Below Parser
        tgp = TemperatureGetParser.parse_args()
        # Converting Date value into Stirng Format
        start = tgp['start'].strftime("%Y-%m-%d")
        end = tgp['end'].strftime("%Y-%m-%d")
        #Fetching All the Records form Location table
        #Making A list of cities using List Comprehension
        #For getting Unique Value of City We are Converting into Set
        #After that We are Sorting the list in Alphabetical Order
        all_city =sorted(list(set([(temp.city,temp.state) for temp in db.session.query(Location).all()])))
        print(all_city)
        #Here We are Looping On all the city 
        
        for city in all_city:
            all_temperature = []
            #for Making Response We need lat,lon,city,state of particular city
            city_data = db.session.query(Location).filter(Location.city == city[0],Location.state == city[1]).first()
            response = {"lat": city_data.lat, "lon": city_data.lon, "city": city_data.city, "state": city_data.state}
            #print(response)
            #Below line of Code Fetch all the row from Location by City
            #Natural Join with Weather Table and then fetching those row which statisfy the given 
            #date rabge
            city_all_temp = db.session.query(Location).filter(Location.city == city[0],Location.state ==city[1]).join(Weather).filter(Weather.date.between(start,end))
            #getting the Count of Row
            city_count = len(list(city_all_temp))
            #if city Count is not 0 then we need to return a normal Responese with high and low temp value of each city
            if city_count != 0:
                for temp in city_all_temp:
                    all_temperature.extend([float(i) for i in temp.weathers[0]._temperature.split(";")])
                all_temperature = list(set(all_temperature))
            
                response["lowest"] = min(all_temperature) 
                response["highest"] = max(all_temperature)
            else:
                response["message"] = "There is no weather data in the given date range"
            #appending Response
            responses.append(response)
        
        
        return make_response(jsonify(responses),200)
###########################################################################################
#############################################################################################
###############################################################################################
###############################################################################################
class PreferredLocationsAPI(Resource):

    def get(self):
        responses = []
        plp = PreferredLocationsParser.parse_args()
        date = plp['date'].strftime("%Y-%m-%d")
        lat = plp['lat']
        lon = plp['lon']
        
        given_state = db.session.query(Location).filter(Location.lat == lat , Location.lon ==lon ).join(Weather).filter(Weather.date == date).first()
        print(given_state.state)
        state = given_state.state
        temp24 = [float(i) for i in  given_state.weathers[0]._temperature.split(';')]
        #mediantemp24 = tfhours(temp24)
        #print(mediantemp24)


        get_all_city =list(set([(city.city,city.state) for city in db.session.query(Location).filter(Location.state != state ).all() ]))
        #print(get_all_city)
        
        for city in get_all_city:
            data = db.session.query(Location).filter(Location.city == city[0],Location.state ==city[1]).join(Weather).filter(Weather.date > date).limit(3).all()
            temp024 =[float(i) for i in  data[0].weathers[0]._temperature.split(';')]
            temp2448 =[float(i) for i in  data[1].weathers[0]._temperature.split(';')]
            temp4872 =[float(i) for i in  data[2].weathers[0]._temperature.split(';')]
            temp72 = extendlist(temp024,temp2448,temp4872)

            if preferlocCondition(temp24,temp72) ==1:
                distance = haversine(lat,lon,data[0].lat,data[0].lon)
                response ={"lat":data[0].lat, "lon": data[0].lon , "city": data[0].city , "state": data[0].state ,"distance":distance,"median_temperature":sthours(temp72)}
                responses.append(response)

            responses = sorted(responses, key = lambda i: (i['distance'], i['median_temperature'],i['city'],i['state']))
        #print(responses)
            


        #print(get_all_city)
        
        return make_response(jsonify(responses),200)




api.add_resource(WeatherList,'/weather' ,'/weather/')
api.add_resource(WeatherErase,'/erase')
api.add_resource(LocationTemp,'/weather/temperature')
api.add_resource(PreferredLocationsAPI, '/weather/locations')

if __name__ == "__main__":
    ''' code by me '''
    db.create_all()
    ''' code by me end '''
    app.run(debug=True)
