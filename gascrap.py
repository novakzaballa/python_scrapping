from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import string
import json

ga_base_url = "https://givingassistant.org"
sitemap_path = "/sitemap/"
coupons_path = "/coupon-codes/"


def get_similar(hostname):
    """
    Get list of stores similar to hostname
    Parameters
        hostname: string. A store hostname. 
    Outcome
        This function will find and return stores in Giving Asssitance site 
        that are similar to the hostname provided as input. The result is 
        an array of 'hostname' and 'title' key value pairs in JSON format.
    """
    all_stores = get_stores()
    similar = []
    total = len(all_stores)
    count = 0
    if (total):
        for store in all_stores:
            printProgressBar(count, total, length=50, suffix=store['hostname'])
            store_page = get_url(
                ga_base_url + coupons_path + store['hostname'])
            if store_page:
                html = BeautifulSoup(store_page, 'html.parser')
                similar_h3_tag = html.find('h3', text='Similar Store Coupons')
                if similar_h3_tag:
                    for link in similar_h3_tag.parent.find_all('a'):
                        if link.get('href') == coupons_path + hostname:
                            similar.append(store)
                            break
            count += 1
        printProgressBar(count, total, length=50, suffix='completed')

    return json.dumps(similar)


def get_stores():
    """
    Returns list of stores in Giving Assitance store pages
    """
    urls = []
    # ['list','a','b',...'z']
    initials = ['list'] + list(string.ascii_lowercase)
    for i in initials:
        print('Processing ' + i + ' page...')
        stores_page = get_url(ga_base_url + sitemap_path + i)
        html = BeautifulSoup(stores_page, 'html.parser')
        div = html.find('div', class_="stores")
        if div:
            for link in div.find_all('a'):
                if link.get('href').startswith(coupons_path):
                    urls.append({'hostname': link.get('title'),
                                 'title': link.get_text()})
    return urls


def get_url(url):
    """
    Try to download HTML page
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if response_is_valid(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def response_is_valid(resp):
    """
    returns True if resp is valid HTML
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
