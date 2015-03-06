import csv
import os
import sys

from jinja2 import Environment, FileSystemLoader
import requests

# API endpoint and required identification header
URL = 'http://www.thebluealliance.com/api/v2/event/{}/matches'
HEADERS = {'X-TBA-App-Id': 'frc295:matchdisplay:v01'}

# Usage
if len(sys.argv) != 3:
	print('Usage: python get_tba_schedule.py <eventcode> <team>')
	print('Example: python gen_matchlist.py 2014cama 295')
	sys.exit()

# GET request to endpoint, using event code from argv
req = requests.get(URL.format(sys.argv[1]), headers=HEADERS)
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

# Only keep matches in which our team participates
data = filter(lambda d: int(sys.argv[2]) in d['red']
		or int(sys.argv[2]) in d['blue'], data)

# Sort matches by match number
data = sorted(data, key=lambda d: d['num'])

# No matches (no schedule available)
if len(data) == 0:
	sys.exit('No matches received')

# Initialize Jinja engine
env = Environment(loader=FileSystemLoader('assets'), trim_blocks=True,
		lstrip_blocks=True)
template = env.get_template('base.html')

# Render template to file
with open(os.path.join('output', '{}_{}.html').format(sys.argv[1], sys.argv[2]), 'wb') as f:
	f.write(template.render(matches=data, event=sys.argv[1], ourteam=int(sys.argv[2])))

