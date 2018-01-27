#!/usr/bin/python3

import click
import re
import sys
import json
import datefinder
import requests

import pprint

USER = {
	'firstName': 'Chris',
	'lastName': 'Pratt',
	'birthday': '1979-06-21',
	'documentID': '42',
	'email': 'pratt@yahoo.com',
	'title': 'Mr'
}

@click.command()
@click.option('--date', required=True, help='Date of departure.')
@click.option('--from', 'f', required=True, help='IATA code from.')
@click.option('--to', 't', required=True, help='IATA code to.')
@click.option('--bags', type=int, help='Luggage quantity.')
@click.option('--return', 'ret', type=int, help='Nights in destination.')
@click.option('--cheapest', is_flag=True, help='Book the cheapest flight.')
@click.option('--fastest', is_flag=True, help='Book the fastest flight.')
@click.option('--one-way', 'oneway', is_flag=True, help='Book one way ticket')
def main(date, f, t, bags, ret, cheapest, fastest, oneway):	
	date, oneway, cheapest = checkInputs(date, f, t, bags, ret, cheapest, fastest, oneway)
	flight = getFlight(date, f, t, ret, cheapest, fastest, oneway)
	if not flight:
		raise Exception('No flight found!')
	bookId = bookFlight(flight, bags)
	print(bookId)
	
	
def checkInputs(date, f, t, bags, ret, cheapest, fastest, oneway):
	date = next(datefinder.find_dates(date), None)
	if not date:
		raise Exception('Invalid date!')
	date = date.strftime('%d/%m/%Y')
	if not (len(f) == 3 and re.match(r'[A-Z]{3}', f)):
		raise Exception('Invalid \'from\' option format!')
	if not (len(t) == 3 and re.match(r'[A-Z]{3}', t)):
		raise Exception('Invalid \'to\' option format!')		
	if not oneway and not ret: oneway = True
	if oneway and ret:
		raise Exception('Ambiguous option one-way/return! Please specify only one.')
	if ret and ret < 0:
		raise Exception('Option \'return\' cannot be negative!')		
	if bags and bags < 0:
		raise Exception('Option \'bags\' cannot be negative!')		
	if not cheapest and not fastest: cheapest = True
	if cheapest and fastest:
		raise Exception('Ambiguous option cheapest/fastest! Please specify only one.')	

	return date, oneway, cheapest

def getFlight(date, f, t, ret, cheapest, fastest, oneway):
	params = dict(
		dateFrom = date,
		daysInDestinationFrom = ret if ret else None,
		flyFrom = f,
		to = t,
		typeFlight = 'oneway' if oneway else 'round',
		sort = 'price' if cheapest else 'duration'
	)
	data = requests.get('https://api.skypicker.com/flights', params=params).json()
	return data['data'][0] if data['data'] else None

def bookFlight(flight, bags):
	url = 'http://128.199.48.38:8080/booking'
	data = {
		'booking_token': flight['booking_token'],
		'currency': next(iter(flight['conversion'])),
		'passengers': [USER],
		'bags': bags if bags else 1
	}
	booking = requests.post(url, json=data).json()
	return booking['pnr']

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		sys.stderr.write('Error: {}\n'.format(str(e)))
		print(0)
		sys.exit(0)

"""
ADD SETUPTOOLS
ADD TESTS
"""