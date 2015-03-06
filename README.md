# matchdisplay

FRC Team 295

A tool to retrieve match schedules from The Blue Alliance and generate a webpage for display in the pits.

## Requirements

- Python (testes with Python 2.7)
- pip packages (install using `pip install -r requirements.txt`)
	- requests
	- Jinja2
	- MarkupSafe

## Usage

`$ python gen_matchlist.py <eventkey> <team>`

- `eventkey` is the year and eventcode of the event [as described on The Blue Alliance API documentation](http://www.thebluealliance.com/apidocs#event-request)
- `team` is the team number that should be used to filter the matches and should be highlighted in the output

