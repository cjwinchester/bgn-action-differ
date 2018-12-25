# Board on Geographic Names action list tracker
The U.S. Geological Survey's [Board on Geographic Names](https://geonames.usgs.gov/) is a public body whose job is to "to maintain uniform geographic name usage throughout the Federal Government." The board also rules on requests by the public to rename geographic features, including those with [offensive names](https://politics.myajc.com/news/state--regional-govt--politics/feds-still-await-georgia-request-change-name-runaway-negro-creek/9P20jHWusJmrFnxPSTQoXO/).

This repo contains some Python that does three things:
1. Download the latest version of [the BGN's "Action list" Excel file with name change proposals](https://geonames.usgs.gov/domestic/quarterly_list.htm), which also includes board actions within the past 12 months.
2. Find and print any diffs between that file and the most recently downloaded version of the file.
3. Incrementally add records to a CSV that keeps track of board actions.

## Running the script
I'm managing my dependencies -- `requests`, `BeautifulSoup`, `pandas` and `xlrd` -- with `pipenv`, but do whatever makes sense for your setup.

- Clone or download this repo
- `cd` into the directory and run `pipenv install` (or whatever your dependency management setup is)
- `pipenv run python bgn_action.py` (or whatever etc.)