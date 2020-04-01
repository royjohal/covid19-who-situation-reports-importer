from urllib.request import urlopen
from shutil import copyfileobj
from requests import get
from requests.utils import default_headers
from bs4 import BeautifulSoup
from datetime import datetime
from pandas import DataFrame
from dateparser import parse as dateparse
from os.path import exists

def get_filename_from_link(link):
    return link.rsplit('/', 1)[-1].rsplit('?',1)[0]

def get_data(url='https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports'):
    headers = default_headers()
    soup = BeautifulSoup(get(url).content, 'html.parser')
    links = ['https://www.who.int' + link.get('href') for link in soup.find_all('a', href=True) if link.get('href').find('.pdf') > -1]
    dates = [datetime.strptime(get_filename_from_link(link).rsplit('-')[0], '%Y%m%d') for link in links]
    reportid = [get_filename_from_link(link).rsplit('-')[2] for link in links]
    list_of_tuples = list(zip(reportid, dates, links))
    return DataFrame(list_of_tuples, columns = ['Report_ID', 'Date', 'Link'])

def download_for_date(datearg,
                      url='https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports'):
    df = get_data(url)
    dt = dateparse(datearg)
    if dt is None:
        print('the date {} couldnt be parsed'.format(datearg))
        return []
    else:
        link = list(df.loc[df['Date'] == dt]['Link'])
        if len(link) == 0:
            print('no record for the date {} found'.format(dt.strftime("%Y/%m/%d")))
            return []
        else:
            link = link[0]
            filename = get_filename_from_link(link)
            if not exists(filename):
                with urlopen(link) as response, open(filename, 'wb') as out_file:
                    copyfileobj(response, out_file)
                    print('file for date {} downloaded at {}'.format(dt.strftime("%Y/%m/%d"), filename))
                    return [dt, filename]
            else:
                print("file for the date {} already exists at {}. didn't re-download".format(dt.strftime("%Y/%m/%d"), filename))
                return [dt, filename]