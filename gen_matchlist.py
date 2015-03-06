import csv
import sys

from jinja2 import Environment, FileSystemLoader
import requests

URL = 'http://www.thebluealliance.com/api/v2/event/{}/matches'
HEADERS = {'X-TBA-App-Id': 'frc295:matchdisplay:v01'}

if len(sys.argv) is not 3:
	print('Usage: python get_tba_schedule.py <eventcode> <team>')
	print('Example: python gen_matchlist.py 2014cama 295')
	sys.exit()

req = requests.get(URL.format(sys.argv[1]), headers=HEADERS)
matches = req.json()

data = []
for m in matches:
	if str(m['comp_level']) != 'qm': continue
	md = {'num': m['match_number']}
	for a in ['red', 'blue']:
		md[a] = [int(str(t[3:])) for t in m['alliances'][a]['teams']]
	data.append(md)
data = filter(lambda d: int(sys.argv[2]) in d['red']
		or int(sys.argv[2]) in d['blue'], data)
data = sorted(data, key=lambda d: d['num'])

env = Environment(loader=FileSystemLoader('assets'))
template = env.get_template('base.html')

with open('{}_{}.html'.format(sys.argv[1], sys.argv[2]), 'wb') as f:
	f.write(template.render(matches=data, event=sys.argv[1], ourteam=int(sys.argv[2])))

