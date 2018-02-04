#!/usr/bin/python3

import click
import re
import sys
import json
import datefinder
import requests
from requests.exceptions import RequestException

USER = {
	'firstName': 'Chris',
	'lastName': 'Pratt',
	'birthday': '1979-06-21',
	'documentID': '42',
	'email': 'pratt@yahoo.com',
	'title': 'Mr'
}

class ArgumentException(Exception):
	pass

class NoFlightException(Exception):
	pass

@click.command()
@click.option('--date', required=True, help='Date of departure.')
@click.option('--from', 'f', required=True, help='IATA code from.')
@click.option('--to', 't', required=True, help='IATA code to.')
@click.option('--bags', type=int, help='Luggage quantity.')
@click.option('--return', 'ret', type=int, help='Nights in destination.')
@click.option('--cheapest', is_flag=True, help='Book the cheapest flight.')
@click.option('--fastest', is_flag=True, help='Book the fastest flight.')
@click.option('--one-way', 'oneway', is_flag=True, help='Book one way ticket.')
@click.option('--warn / --no-warn', default=True, help='Show warning and error messages.')
def main(date, f, t, bags, ret, cheapest, fastest, oneway, warn):	
	try:
		date, oneway, cheapest = checkInputs(date, f, t, bags, ret, cheapest, fastest, oneway)
		flight = getFlight(date, f, t, ret, cheapest, fastest, oneway)
		if not flight:
			raise NoFlightException('No flight found!')
		bookId = bookFlight(flight, bags)
		print(bookId)
	except ArgumentException as e:
		if warn: sys.stderr.write('Input Error: {}\n'.format(str(e)))
		print(0)
		sys.exit(1)
	except NoFlightException as e:
		if warn: sys.stderr.write('Booking Error: {}\n'.format(str(e)))
		print(0)
		sys.exit(1)
	except RequestException as e:
		if warn: sys.stderr.write('Request Error: {}\n'.format(str(e)))
		print(0)
		sys.exit(1)
	except Exception as e:
		if warn: sys.stderr.write('Unexpected Error: {}\n'.format(str(e)))
		print(0)
		sys.exit(1)
	
def checkInputs(date, f, t, bags, ret, cheapest, fastest, oneway):
	"""Check input arguments, modify date to desired format and set default flags --one-way and --cheapest if not specified.

	Throws:
		ArgumentException: If some argument is not valid

	Returns:
		modified tuple (date, oneway, cheapest)
	"""

	date = next(datefinder.find_dates(date), None)
	if not date:
		raise ArgumentException('Invalid date!')
	date = date.strftime('%d/%m/%Y')

	if not (len(f) == 3 and re.match(r'[A-Z]{3}', f)):
		raise ArgumentException('Invalid \'from\' option format!')

	if not (len(t) == 3 and re.match(r'[A-Z]{3}', t)):
		raise ArgumentException('Invalid \'to\' option format!')		

	if not oneway and not ret: 
		oneway = True

	if oneway and ret:
		raise ArgumentException('Ambiguous option one-way/return! Please specify only one.')

	if ret and ret < 0:
		raise ArgumentException('Option \'return\' cannot be negative!')		

	if bags and bags < 0:
		raise ArgumentException('Option \'bags\' cannot be negative!')		

	if not cheapest and not fastest: 
		cheapest = True

	if cheapest and fastest:
		raise ArgumentException('Ambiguous option cheapest/fastest! Please specify only one.')	

	return date, oneway, cheapest

def getFlight(date, f, t, ret, cheapest, fastest, oneway):
	"""Get the best flight from skypicker api.

	Returns:
		the best flight or None if no flight found
	"""

	params = {
		'dateFrom': date,
		'daysInDestinationFrom': (ret if ret else None),
		'flyFrom': f,
		'to': t,
		'typeFlight': ('oneway' if oneway else 'round'),
		'sort': ('price' if cheapest else 'duration')
	}
	data = requests.get('https://api.skypicker.com/flights', params=params).json()
	return data['data'][0] if data.get('data') else None

def bookFlight(flight, bags):
	"""Books given flight.

	Returns:
		'pnr' of booked flight
	"""

	url = 'http://128.199.48.38:8080/booking'
	data = {
		'booking_token': flight['booking_token'],
		'currency': list(flight['conversion'].keys())[0],
		'passengers': [USER],
		'bags': bags if bags else 1
	}
	booking = requests.post(url, json=data).json()
	return booking['pnr']

if __name__ == '__main__':
	main()	
