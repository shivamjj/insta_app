# -*- coding: utf-8 -*
import geocoder
from flask import Flask, render_template, jsonify
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from flask_sqlalchemy import SQLAlchemy
import urllib2
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql12204982:wsI8rv8qKM@sql12.freemysqlhosting.net:3306/sql12204982'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Dataa(db.Model):
	__tablename__ = 'table_data'
	id = db.Column('id', db.Integer, primary_key=True)
	data_uber = db.Column('data_uber',db.String(300))
	location = db.Column('location',db.String(300))
	data_four = db.Column('data_four',db.String(300))

	def __init__(self,data_uber,location,data_four):
		self.data_uber = data_uber
		self.location = location
		self.data_four = data_four

	@property
	def serialize(self):
		return{
			'id' : self.id,
			'location' : self.location,
			'data_uber' : self.data_uber,
			'data_four' : self.data_four,
		}
@app.route('/')
def default():
	return 'Enter city with format /delhi or /delhi/json.'

@app.route('/<string:city>')
def map_func(city):

	try:
		session = Session(server_token="RQeZpU7s-YGa0UOvE-snkpIEQ0Wb4vxStK1nhlGC")
		client = UberRidesClient(session)
	 
		city_conv = str(city)
		#print type(cit)
		
		items = Dataa.query.all()
		for x in items:
			if(x.location==city_conv):
				return '{“saved”:true}'

		lat_lng=geocoder.google(city_conv)
		#print lat_lng.latlng
		url = 'https://api.foursquare.com/v2/venues/search?near='+city+'&client_id=ZJI0H5P2ZLUB1FY2PZHQKI1Y40QCMRUDBZ1AYINMTJOPRUS5&client_secret=FPTTNGZNI3TYLS4QEC2RF2MTUOLJ101Y3F41ENHK0B54BGXA&v=20170101'
		obj = urllib2.urlopen(url)
		data = json.load(obj)
		for j in data['response']['venues']:
			place=j['name']
			break


		response = client.get_products(lat_lng.latlng[0],lat_lng.latlng[1])
		products = response.json.get('products')
		product_id = products[0].get('product_id')
		
		entry = Dataa(product_id,city_conv,place)
		db.session.add(entry)
		db.session.commit()

		return  '{“saved”:true}'
	except:
		return 'Enter a valid city'

@app.route('/<string:city>/json')
def func(city):
	flag =0
	cit = str(city)
	items = Dataa.query.all()
	for x in items:
		if(x.location==cit):
			flag = 1
			return jsonify(location=[x.serialize])
	
	if(flag==0):
		return 'Data not present in DB'


if __name__ == '__main__':
    app.run()