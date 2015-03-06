import csv
import os
import sys

import gen_matchlist as gen

USAGE_STRING = 'Usage: python tba2csv.py <eventcode>'

if len(sys.argv) != 2: sys.exit(USAGE_STRING)
event = sys.argv[1]

# Get matches and sort
matches = gen.get_from_tba(event)
matches = sorted(matches, key=lambda m: m['num'])

with open(os.path.join('schedules', '{}.csv'.format(event)), 'wb') as f:
	writer = csv.writer(f)
	for m in matches:
		row = [m['num']] + m['red'] + m['blue']
		writer.writerow(row)

