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

	def __init__(self,data_uber,location):
		self.data_uber = data_uber
		self.location = location
		

	@property
	def serialize(self):
		return{
			'id' : self.id,
			'location' : self.location,
			'data_uber' : self.data_uber,
		}

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

		response = client.get_products(lat_lng.latlng[0],lat_lng.latlng[1])
		products = response.json.get('products')
		product_id = products[0].get('product_id')
		
		entry = Dataa(product_id,city_conv,place)
		db.session.add(entry)
		db.session.commit()

		return  '{“saved”:true}'
	except:
		return 'Enter valid city'

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