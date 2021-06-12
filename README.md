# Weather-API
A Flask based Weather API.

- This is a Python Flask Api based project .We can perform (Get, Post, Put ,Delete) Operation using location ,latitude, longitude, daterange etc.

- The WeatherAPI service should be able to add new weather data to a server and provide requested weather information to the user.

- WeatherAPI contain the following four resources.
	- WeatherList
	- WeatherErase 
	- LocationTemp 
	- PreferredLocations 

- WeatherList:

      Adding new weather data: The service  able to add a new weather data by the POST request at /weather.

      Returning all the weather data: The service  able to return the JSON array of all the weather data by the GET request at /weather.

      Returning the weather data filtered by the location coordinates: The service  able to return the JSON array of all the weather data that are associated with the given latitude and longitude by the GET request at /weather?lat={latitude}&lon={longitude}

- WeatherErase:

      Erasing all the weather data: The service able to erase all the weather data by the DELETE request at /erase. 

      Erasing all the weather data by the date range inclusive and the location coordinates: The service should be able to erase all the weather data by the date range inclusive, and the location coordinates by the DELETE request at /erase?start={startDate}&end={endDate}&lat={latitude}&lon={longitude}. 

- LocationTemp:

      LocationTemp Resource  Return the lowest and highest temperature for all the cities in the given date range.

      The service  be able to return the JSON array.

      Each JSON object of returned JSON array  contain the information of the lowest and highest temperature of a location in the given date range specified by start date and end date inclusive, by the GET request at /weather/temperature?start={startDate}&end={endDate}.


- PreferredLocations:

      PreferredLocations Resource must Return the preferred locations information with respect to given date and location.

      The service should be able to return the JSON array.
      Each JSON object of JSON array should contain the information of the preferred location, the distance between the preferred location and given location and the median temperature of the preferred location in next 72 hours excluding the given date by the GET request at /weather/locations?date={date}&lat={latitude}&lon={longitude}.
    
    
- Technology Used: 
    - Python Flask
    - Python Flask Mail
    - Json 
