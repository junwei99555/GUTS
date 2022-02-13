from flask import Flask, render_template, jsonify
import requests
import os
import pytz
from datetime import datetime
from GoogleNews import GoogleNews
import random

app = Flask(__name__)

api_key = '4de7780b7f6e73aff0493515d4f648f5'

@app.route("/api/getMorningData",methods=['GET'])
def getMorning():
    with open("./mmsg.txt","r") as file:
        allText = file.read()
        lines = list(map(str,allText.split('\n')))

        line_1 = random.choice(lines)
        line_2 = random.choice(lines)

        while line_2 == line_1:
            line_2 = random.choice(lines)
        
        line_3 = random.choice(lines)
        while line_3 == line_1 or line_3 == line_2:
            line_3 = random.choice(lines)
        
        output = [line_1,line_2,line_3]

        return jsonify(output)

@app.route("/api/getWeatherData",methods=['GET'])
def apiGetWeather():
    location = "Europe"

    complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+api_key
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()

    #create python object to store data
    data = {
        "temp": "%0.2f" % ((api_data['main']['temp']) - 273.15),
        "desc": api_data['weather'][0]['description'],
        "hmdt": "%0.2f" % (api_data['main']['humidity']),
        "wind_speed": "%0.2f" % (api_data['wind']['speed']),
        "date_time": datetime.now(pytz.timezone('GMT'))
    }

    # convert into JSON:
    return jsonify(data)

@app.route("/api/getNewsData",methods=['GET'])
def apiGetNews():
    news = GoogleNews(period='1d')
    news.get_news('UK')
    result = news.result()

    result = result[0:6]

    # convert into JSON:
    return jsonify(result)

@app.route("/")
def home():
    return render_template("index.html")

app.run(debug=True,host="0.0.0.0")