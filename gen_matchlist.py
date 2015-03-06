import os
import sys

from jinja2 import Environment, FileSystemLoader

USAGE_STRING = '''Usage: python gen_matchlist.py [csv <filename> | tba <eventcode>] <team>
Example: python gen_matchlist.py csv compschedule.csv 295
Example: python gen_matchlist.py tba 2013cama 295'''

def get_from_csv(filename):
	'''
	Get data from a csv file.
	Rows should have the following format:

	matchnum,red1,red2,red3,blue1,blue2,blue3
	'''
	import csv
	data = []

	# Read csv file into list
	with open(filename, 'rb') as f:
		rows = list(csv.reader(f))
	
	# Add data to match data list (casted to integers)
	for r in rows:
		num = int(r[0])
		red  = [int(team) for team in r[1:4]]
		blue = [int(team) for team in r[4:7]]
		data.append({'num': num, 'red': red, 'blue': blue})

	return data


def get_from_tba(event):
	'''
	Get data from The Blue Alliance's Event API.
	'''
	import requests

	# API endpoint and required identification header
	URL = 'http://www.thebluealliance.com/api/v2/event/{}/matches'.format(event)
	HEADERS = {'X-TBA-App-Id': 'frc295:matchdisplay:v01'}

	# GET request to endpoint
	req = requests.get(URL, headers=HEADERS)
	matches = req.json()

	# Check for 404 error (e.g. no such event)
	if isinstance(matches, dict) and matches['404']:
		sys.exit('404: {}'.format(matches['404']))

	data = []
	# Response is JSON array of matches
	for m in matches:
		# Only get qualification matches
		if str(m['comp_level']) != 'qm': continue

		# Initialize match data dict with match number
		md = {'num': m['match_number']}

		for a in ['red', 'blue']:
			# For each alliance, add to match data: key is alliance,
			# value is array of team numbers
			md[a] = [int(str(t[3:])) for t in m['alliances'][a]['teams']]
		# Add match data to list of data
		data.append(md)

	# No matches (no schedule available)
	if len(data) == 0:
		sys.exit('No matches received')

	return data


def main():
	# Ensure correct number of arguments
	if len(sys.argv) != 4:
		sys.exit(USAGE_STRING)

	ourteam = int(sys.argv[3])
	event = sys.argv[2]

	# Check input type argument
	if sys.argv[1] == 'tba':
		data = get_from_tba(event)
	elif sys.argv[1] == 'csv':
		data = get_from_csv(event)
	else:
		sys.exit(USAGE_STRING)

	# Only keep matches in which our team participates
	data = filter(lambda d: ourteam in d['red'] or ourteam in d['blue'], data)

	# Sort matches by match number
	data = sorted(data, key=lambda d: d['num'])

	# Initialize Jinja engine
	env = Environment(loader=FileSystemLoader('assets'), trim_blocks=True,
			lstrip_blocks=True)
	template = env.get_template('base.html')

	# Get bare filename (no path, no file extension)
	event = ''.join(event.split(os.path.sep)[-1].split('.')[:-1])

	# Render template to file
	with open(os.path.join('output', '{}_{}.html').format(event, ourteam), 'wb') as f:
		f.write(template.render(matches=data, event=event, ourteam=ourteam))


if __name__ == '__main__': main()

