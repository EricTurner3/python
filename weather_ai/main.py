import json
import requests
import numpy
import pandas as pd
import os

#import the apikey from file (so GitHub does not get my key)
with open('weatherapi.key', 'r') as key:
    apikey = key.read()

print("API Key: " + apikey)

response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Indianapolis&units=imperial&lang=en&appid=" + apikey)
# View an example of the weather output in the file weathermap.json
weather = json.loads(response.text)

current_weather = weather

# grab the current temp in Fahrenheit
current_temperature = current_weather['main']['temp']
current_humidity = current_weather['main']['humidity']

current_windspeed = current_weather['wind']['speed']

current_forecast = {"id":current_weather['weather'][0]['id'], "main": current_weather['weather'][0]['main'], "desc": current_weather['weather'][0]['description']}

"""
print(current_temperature)
print(current_humidity)
print(current_windspeed)
print(current_forecast)
"""

def beaufortWindScale(wind_mph):
    """
    Input: the raw wind speed (in mph) 
    Return: Beaufort Wind Scale classification and score value from 0.0 (poor) to 0.5 (perfect)
    """
    # determine the ranking on the Beaufort Wind Scale (https://www.spc.noaa.gov/faq/tornado/beaufort.html)
    # the wind comes to us as "xx mph" so we need to parse out the actual number and then divide by 1.151 to get Knots
    wind_knots = float(wind_mph) / 1.151

    # default values (will be changed in below logic)
    wind_force = 0
    wind_classification = "Calm"
    wind_score = 0.50

    # Force 11 and 12 are not experienced on land so are not included in the function
    if 0 <= wind_knots <= 1.99:
        wind_force = 0
        wind_classification = "Calm"
        wind_score = 0.50
    elif 1 <= wind_knots <= 3.99:
        wind_force = 1
        wind_classification = "Light Air"
        wind_score = 0.45
    elif 4 <= wind_knots <= 6.99:
        wind_force = 2
        wind_classification = "Light Breeze"
        wind_score = 0.40
    elif 7 <= wind_knots <= 10.99:
        wind_force = 3
        wind_classification = "Gentle Breeze"
        wind_score = 0.35
    elif 11 <= wind_knots <= 16.99:
        wind_force = 4
        wind_classification = "Moderate Breeze"
        wind_score = 0.30
    elif 17 <= wind_knots <= 21.99:
        wind_force = 5
        wind_classification = "Fresh Breeze"
        wind_score = 0.25
    elif 22 <= wind_knots <= 27.99:
        wind_force = 6
        wind_classification = "Strong Breeze"   
        wind_score = 0.20     
    elif 28 <= wind_knots <= 33.99:
        wind_force = 7
        wind_classification = "Near Gale"    
        wind_score = 0.15
    elif 34 <= wind_knots <= 40.99:
        wind_force = 8
        wind_classification = "Gale"     
        wind_score = 0.10 
    elif 41 <= wind_knots <= 47.99:
        wind_force = 9
        wind_classification = "Strong Gale"  
        wind_score = 0.05
    elif 48 <= wind_knots <= 55.99:
        wind_force = 10
        wind_classification = "Storm" 
        wind_score = 0.00

    return {"wind_force": wind_force, "wind_classification": wind_classification, "wind_score": wind_score}

# lookup the outlook score to return, based on the weather codes and weather_scoring algoritm I developed
def outlookScore(outlook):
    """
    Input: raw outlook data from OpenWeatherMap API
    
    Return: A score based on the current weather conditions
    """
    # list of weather codes and conditions here: https://openweathermap.org/weather-conditions
    # here is a list of the IDs and the appropriate score to lookup
    # the scores were generated from weather_scoring.py
    scores = {
        200: 0.04, 
        201: 0.10, 
        202: 0.03, 
        210: 0.10, 
        211: 0.30, 
        212: 0.07, 
        221: 0.09, 
        230: 0.04, 
        231: 0.12, 
        232: 0.03, 
        300: 0.13, 
        301: 0.40, 
        302: 0.08, 
        310: 0.05, 
        311: 0.14, 
        312: 0.03, 
        313: 0.05, 
        314: 0.01, 
        321: 0.15, 
        500: 0.12, 
        501: 0.10, 
        502: 0.07, 
        503: 0.05, 
        504: 0.02, 
        511: 0.10, 
        520: 0.04, 
        521: 0.13, 
        522: 0.03, 
        531: 0.04, 
        600: 0.10, 
        601: 0.28, 
        602: 0.07, 
        611: 0.28, 
        612: 0.04, 
        615: 0.03, 
        616: 0.10, 
        620: 0.04, 
        621: 0.10, 
        622: 0.03, 
        701: 0.42, 
        711: 0.26, 
        721: 0.26, 
        731: 0.06, 
        741: 0.45, 
        751: 0.23, 
        761: 0.23, 
        762: 0.17, 
        771: 0.15, 
        781: 0.05, 
        800: 0.50, 
        801: 0.43, 
        802: 0.42, 
        803: 0.40, 
        804: 0.39
    }
    
    outlook_score = scores[outlook['id']]

    return outlook_score

# use the temperature and the humidity and this guide (page 6) to determine the comfort score
# Guide: http://www.dartmouth.edu/~cushman/courses/engs44/comfort.pdf
# Image: temp_comfort_zone.png
def temperatureScore(temperature, humidity):
    """
    Input: Temperature (in F) and Humidity (%)
    Return: Classified Zone and a Score from 0 (poor) to 0.5 (perfect)
    """
    # According to the comfort zone, we can be in 7 possible zones
    
    #Humid           - Above 80% humidity, and between 68.00 degrees F and 75 degrees F
    #Cold & Humid    - Between 100% humidity and 30% humidity and below 67.99 degrees F
    #Hot & Humid     - Between 100% humidity and 30% humidity and above 78.00 degrees F
    #Cold & Dry      - Between 29% humidity and 0% humidity and below 77.99 degrees F
    #Dry             - Below 19% humidity and between 68 degrees and 78 degrees
    #Hot & Dry       - Below 29% humidity and above 78 degrees
    #Comfort Zone    - Else


    #Cold & Hot are 0.25 modifers (so add up the other score and divide by 2 for the average)
    

    if humidity < 20: # if the humidity is less than 20%
        if temperature < 78:
            zone = "Dry"
            score = 0.35
    elif humidity < 30: # if the humidity is greater than 20% but less than 30%
        if temperature < 68:
            zone = "Cold and Dry"
            score = 0.30
        elif 68 <= temperature <= 78:
            zone = "Comfort Zone"
            score = 0.5
        elif temperature > 78:
            zone = "Hot and Dry"
            score = 0.30
    elif humidity < 50: # if the humidity is greater than 30% but less than 50%
        if temperature < 68:
            zone = "Cold and Humid"
            score = 0.30
        elif 68 <= temperature <= 78:
            zone = "Comfort Zone"
            score = 0.5
        elif temperature > 78: 
            zone = "Hot and Humid"
            score = 0.30
    elif humidity < 60: # if the humidity is greater than 50% but less than 60%
        if temperature < 68:
            zone = "Cold and Humid"
            score = 0.30
        elif 68 <= temperature <= 76:
            zone = "Comfort Zone"
            score = 0.5
        elif temperature > 76:
            zone = "Hot and Humid"
            score = 0.30
    elif humidity < 80: # if the humidity is greater than 60% but less than 80%
        if temperature < 68:
            zone = "Cold and Humid"
            score = 0.30
        elif 68 <= temperature <= 75:
            zone = "Comfort Zone"
            score = 0.5
        elif temperature > 75:
            zone = "Hot and Humid"
            score = 0.30
    elif humidity > 80: # if the humidity is greater than 80%
        if temperature < 68:
            zone = "Cold and Humid"
            score = 0.30
        elif temperature < 74:
            zone = "Humid"
            score = 0.35
        elif temperature > 74:
            zone = "Hot and Humid"
            score = 0.30
    return {"zone": zone, "score": score}

def clothing_prediction(normalized_wind, normalized_temp, normalized_outlook):
    """
    Final Stage: Pass in the normalized values and return out the prediction for clothing
    """
    # TODO: Create an algorithm and return a prediction
    # Stages: 
    # 0.333 is the MAX for the normalized values which is PERFECT
    # 0.264 is 80% of the value which is GREAT
    # 0.198 is 60% of the value which is GOOD
    # 0.132 is 40% of the value which is POOR
    # 0.066 is 20% of the value which is BAD
    # 0.000 is 0% of the value which is AWFUL
    perfect = 0.333
    great = perfect * 0.80
    good = perfect * 0.60
    bad = perfect * 0.40
    awful = 0

    if great <= normalized_wind <= perfect:
        wind_prediction = "Wind is ideal. No jacket is necessary."

    return "<<>>"

# this is what analyzes the current weather and then tries to make a prediction
def weatherAlgorithm(temperature, humidity, wind, outlook):
    # run the algorithms to determine scores
    wind_info = beaufortWindScale(wind)
    outlook_score = outlookScore(outlook)
    temperature_score = temperatureScore(temperature, humidity)
    # clear the console screen
    os.system('cls' if os.name=='nt' else 'clear')
    # some printing to the console
    print("==============================================")
    print("*** Status ***")
    print("Current Outlook: "+ outlook['desc'])
    print("Current Temperature: "+ str(temperature) + "°F")
    print("Current Humidity: "+ str(humidity) + "%")
    print("Current Comfort Zone: "+ str(temperature_score['zone']))
    print("Current Wind Speed: "+ str(wind) + " mph")
    print("Current Wind Classifcation: "+ str(wind_info['wind_classification']))
    print("==============================================")
    print("\n==============================================")
    # scores are ranked from 0.00 (poor) to 0.50 (perfect)
    # to normalize, we can multiply each score by 2/3 (times 2 to get the 0.5 max to a 1, and then divided by 3 for the three options)
    normalization_value = (2/3)
    print("*** Scores ***")
    normalized_wind = float("{0:.3f}".format(wind_info['wind_score'] * normalization_value))
    normalized_outlook = float("{0:.3f}".format(outlook_score * normalization_value))
    normalized_temp = float("{0:.3f}".format(temperature_score['score'] * normalization_value))
    print("Wind Score: " + str(normalized_wind) + ' / 0.33')
    print("Outlook Score: " + str(normalized_outlook) + ' / 0.33')
    print("Temperature Score: " + str(normalized_temp) + ' / 0.33')
    print("Total Score: " + str("{0:.3f}".format(normalized_wind + normalized_outlook + normalized_temp)) + ' / 1.00')
    print("==============================================")
    
    prediction = clothing_prediction(normalized_wind, normalized_temp, normalized_outlook)
    print("\n==============================================")
    print("*** Prediction ***")
    print(prediction)
    print("==============================================")

    

# call the weatherAlgorithm function with the information from the OpenWeatherMap API to run the other algorithms
weatherAlgorithm(current_temperature, current_humidity, current_windspeed, current_forecast)
# test for comfort zone
#print(str(temperatureScore(72.00, 30)['zone']))