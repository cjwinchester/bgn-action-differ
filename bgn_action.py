import datetime
import glob
import os

import requests
from bs4 import BeautifulSoup
import pandas as pd


CSV_FILE = 'latest.csv'


def get_xl_link():
    '''
    Parse the BGN page to get a link to the latest action list file.

    Returns:
        A tuple with the updated date and a link to the Excel file.
     '''

    URL = 'https://geonames.usgs.gov/apex/f?p=geonames_web:review_lists'

    # grab the page
    r = requests.get(URL)

    # turn it into soup
    soup = BeautifulSoup(r.text, 'html.parser')

    # find the correct link
    link = soup.find('a', text='Action List')

    # grab the container span with the date info
    span = link.parent.text.split(':')[1].strip().rstrip(')')

    # parse out the date in iso format
    updated_date = datetime.datetime.strptime(
        span,
        '%B %d, %Y').date().isoformat()

    # return a tuple with the date and the link
    return (updated_date, 'https://geonames.usgs.gov/apex/' + link['href'])


def download_latest_xl(updated, link):
    '''
    Given an updated date and a link, download the latest Excel file.

    Returns:
        The absolute path to the downloaded file.
    '''

    # format the filename with the updated date, joined to raw dir
    filepath = os.path.join('raw', f'{updated}-bgn-action-list.xls')

    # if this file doesn't exist already
    if not os.path.isfile(filepath):

        # fetch the link
        r = requests.get(link)

        # and write the contents to file
        with open(filepath, 'wb') as f:
            for block in r.iter_content(1024):
                f.write(block)

    # return absolute path to the file
    return os.path.abspath(filepath)


def diff_latest_and_write():
    '''
    1. Find the differences between the most recent file and the next
       most recent file
    2. Write out a CSV file with the latest unique records

    Returns:
        A list of dictionaries of new records.
    '''

    # get a sorted list of existing Excel files
    XLS_FILES = sorted(glob.glob('raw/*.xls'))

    # get name of latest file
    latest_file = XLS_FILES[-1]

    # read latest file into a data frame
    df_latest = pd.read_excel(latest_file)

    # if main CSV doesn't exist already
    if not os.path.exists(CSV_FILE):

        # write out the latest data frame to file
        df_latest.to_csv(CSV_FILE, index=False)

    # if it exists already
    else:
        # read the CSV into a data frame
        main_df = pd.read_csv(CSV_FILE)

        # combine it with the latest data frame
        new_main_df = pd.concat([df_latest, main_df], axis=1)

        # drop duplicate records
        new_main_df.drop_duplicates()

        # write back out to main CSV
        new_main_df.to_csv(CSV_FILE, index=False)

    # bail if there's only one file in the directory
    if len(XLS_FILES) == 1:
        print('I only found one file.')
        return None

    # but if there are multiple files
    else:
        # grab the name of the second most recent file
        next_latest_file = XLS_FILES[-2]

        # read it into a data frame
        df_next_latest = pd.read_excel(next_latest_file)

        # combine it with the latest file in a new data frame
        # drop duplicates and keep none of them
        diff = pd.concat(
            [df_latest, df_next_latest]
        ).drop_duplicates(keep=False)

        # return diff records as a list of dictionaries
        return diff.to_dict('records')


if __name__ == '__main__':

    # grab the link
    latest = get_xl_link()

    # download the latest file
    download_latest_xl(*latest)

    # find the diffs and write out to file
    diffs = diff_latest_and_write()

    # print diffs
    print(diffs)
