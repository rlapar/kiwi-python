#!/usr/bin/python3

import click
import re
import sys
import json
import datefinder
import requests

import pprint

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
	flight = getFlight(date, f, t, bags, ret, cheapest, fastest, oneway)
	
	
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

def getFlight(date, f, t, bags, ret, cheapest, fastest, oneway):
	params = dict(
		dateFrom=date,
		dateTo=None,
		flyFrom=f,
		to=t,
		typeFlight=None,
		sort=None
	)
	params['typeFlight'] = 'oneway' if oneway else 'round'
	params['sort'] = 'price' if cheapest else 'duration'
	#BAGS??

	res = requests.get('https://api.skypicker.com/flights', params=params)
	print(res.url)
	data = json.loads(res.text)
	print(len(data))


if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		sys.stderr.write('Error: {}\n'.format(str(e)))
		print(0)
		sys.exit(0)

"""
ADD SETUPTOOLS
"""