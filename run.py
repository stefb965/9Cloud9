from flask import Flask, request, redirect
import twilio.twiml
from pyzipcode import ZipCodeDatabase
import pyowm

app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def echo():
 	
	owm = pyowm.OWM('186b60225f98470ed49394971d95e5f4')
	zcdb = ZipCodeDatabase()

	body = request.values.get('Body', None)
	message = ""
	try:
		zipcode = zcdb[body]
		lat = zipcode.latitude
		lon = zipcode.longitude
		observation = owm.weather_at_coords(lat,lon)
		w = observation.get_weather()
		status = w.get_weather_icon_name()

		if status == '01d' or status =='01n':#sunny
			message = u"\U00002600"
		elif status == '09d' or status == '09n' or status == '10d' or status == '10n':#rain
			message = u"\U0001F327"
		elif status == '11d' or status == '11n' :#thunder
			message = u"\U0001F329"
		elif status == '04d' or status == '04n':#cloudy
			message = u"\U00002601"
		elif status == '02d' or status == '02n': #partly cloudy
			message = u"\U0001F324"
		elif status == '13d' or status == '13n':#snowy
			message = u"\U0001F328"
		elif status == '03d' or status == '03n':#mostly cloudy
			message = u"\U0001F325"
		elif status == '50d' or status == '50n':#mist
			message = u"\U0001F301"
		else: message = u"\U00002757" #Question Mark
	except:
		print("Error caught: user entered -->"+body)
		message = u"\U00002757"+"(please enter a zipcode)"
	resp = twilio.twiml.Response()
	resp.message(message)
 
	return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)