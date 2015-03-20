# matchdisplay

FRC Team 295

A tool to retrieve match schedules from The Blue Alliance or a given `.csv` file and generate a webpage for display in the pits.

Also includes a script to generate a schedule `.csv` file from The Blue Alliance for an event.

## Requirements

- Python (tested with Python 2.7)
- pip packages (install using `pip install -r requirements.txt`)
	- requests
	- Jinja2
	- MarkupSafe

## Usage

### `gen_matchlist`

`$ python gen_matchlist.py [csv <filename> | tba <eventkey>] <team>`

- `eventkey` is the year and eventcode of the event [as described on The Blue Alliance API documentation](http://www.thebluealliance.com/apidocs#event-request)
- `team` is the team number that should be used to filter the matches and should be highlighted in the output

### `tba2csv`

`$ python tba2csv.py <eventkey>`

- `eventkey`: see above

## Output

The main script, `gen_matchlist`, generates a webpage that contains a table of upcoming matches for a team. Clicking on a match row will remove it, so that elapsed matches can be hidden. To restore them, refresh the page.

Note: The webpage is only tested on Google Chrome, but may work on other browsers.

