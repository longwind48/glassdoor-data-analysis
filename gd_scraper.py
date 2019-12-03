import ast
import logging
import time
from datetime import datetime, timedelta
import re
import numpy as np
import pandas as pd
import regex
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

_HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0'}
# {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def handle_exceptions(func):
    """decorator for handling exceptions
    Usage:
    @handle_exceptions
    def function_to_handle():
    """
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.warning(e)
            return dict()

    return func_wrapper

def get_position_link(url):

    links = []
    header = _HEADER

    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')

    a = soup.find_all('a', class_='jobLink')
    for i in a:
        links.append('https://www.glassdoor.com' + i.get('href'))

    return links


def get_all_links(num_page, url):

    link = []
    i = 1
    print('Collecting links....')
    while i <= num_page:
        try:
            url_main = url[:-4] + '_IP{}.htm'.format(i) + '.htm'
            link.append(get_position_link(url_main))
            i = i + 1
            time.sleep(1)
        except:
            print('No more pages found.')
    return link

@handle_exceptions
def scrap_job_page(url):
    '''
    This function collects all data we are asking for and store the result in a dictionary.

    Args:
            url: a single url of a job application.

    return: Python dictionary
            dictionary returning data we asked the crawler to collect for us.


    '''
    dic = dict()
    raw_json, body = get_gd_json(url)
    dic["url"] = url
    dic["title"] = find_title(raw_json)
    dic["company"] = find_company(raw_json)
    dic["date_posted"] = find_date(raw_json)
    dic['geo_coord'] = find_geo(raw_json)
    dic['industry'] = find_industry(raw_json)

    #     Job description
    job_des = body.find('div', class_='jobDesc')
    dic['job_description'] = job_des

    return dic

def get_gd_json(url):
    header = _HEADER
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.find('body')
    json = str(soup.find_all("script",type="application/ld+json"))
    return json, body

def find_date(somejson):
    try:
        date = re.findall(r'''"datePosted"\s*:\s*"([^"]*)"''', somejson, re.I)[0]
    except:
        date = 'empty'
    return date

def find_geo(somejson):
    try:
        geo_tuple = (re.findall(r'''"latitude"\s*:\s*"([^"]*)"''', somejson, re.I)[0],
                    re.findall(r'''"longitude"\s*:\s*"([^"]*)"''', somejson, re.I)[0])
    except:
        geo_tuple = ('empty', 'empty')

    return geo_tuple

def find_title(somejson):
    try:
        title = re.findall(r'''"title"\s*:\s*"([^"]*)"''', somejson, re.I)[0]
    except:
        title = 'empty'
    return title

def find_industry(somejson):
    try:
        industry = re.findall(r'''"industry"\s*:\s*"([^"]*)"''', somejson, re.I)[0]
    except:
        industry = 'empty'
    return industry

def find_company(somejson):
    try:
        company = re.findall(r'''"name"\s*:\s*"([^"]*)"''', somejson, re.I)[0]
    except:
        company = 'empty'
    return company

if __name__ == '__main__':
    num_pages = 29
    links = get_all_links(
        num_pages, 'https://www.glassdoor.sg/Job/singapore-business-analyst-jobs-SRCH_IL.0,9_IC3235921_KO10,26.htm')
    # da 'https://www.glassdoor.sg/Job/singapore-data-analyst-jobs-SRCH_IL.0,9_IC3235921_KO10,22.htm'
    # ba 'https://www.glassdoor.sg/Job/singapore-business-analyst-jobs-SRCH_IL.0,9_IC3235921_KO10,26.htm'
    # ds 'https://www.glassdoor.sg/Job/singapore-data-scientist-jobs-SRCH_IL.0,9_IC3235921_KO10,24.htm'
    # 30, 'https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14_IP')
    # print(links)
    for page in links:
        print(len(set(page)))

    flatten_list = list(set([item for sublist in links for item in sublist]))
    list_result = []

    for page in tqdm(flatten_list):
        list_result.append(scrap_job_page(page))
        time.sleep(0.3)

    # Save the dictionary into a dataframe
    list_result = [x for x in list_result if x]
    df_glass = pd.DataFrame.from_records(list_result)
    df_glass = df_glass[df_glass['title'] != 'empty']

    df_glass.to_csv('ba_glassdoor_p{}_{}.csv'.format(num_pages, datetime.now().date()))
