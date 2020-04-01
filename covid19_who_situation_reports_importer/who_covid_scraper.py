from urllib.request import urlopen
from shutil import copyfileobj
from requests import get
from requests.utils import default_headers
from bs4 import BeautifulSoup
from datetime import datetime
from pandas import DataFrame
from dateparser import parse as dateparse
from os.path import exists, join
from pathlib import Path
from pandas import concat as pdconcat

from parsr_client import ParserClient

class WHOCovidScraper(object):
	def __init__(self, url='https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports'):
		self.url = url
		self.df = self.__get_data(self.url)

	def get_filename_from_link(self, link:str) -> str:
			return link.rsplit('/', 1)[-1].rsplit('?',1)[0]

	def __get_data(self, url:str) -> DataFrame:
			headers = default_headers()
			soup = BeautifulSoup(get(self.url).content, 'html.parser')
			links = ['https://www.who.int' + link.get('href') for link in soup.find_all('a', href=True) if link.get('href').find('.pdf') > -1]
			dates = [datetime.strptime(self.get_filename_from_link(link).rsplit('-')[0], '%Y%m%d') for link in links]
			reportid = [self.get_filename_from_link(link).rsplit('-')[2] for link in links]
			list_of_tuples = list(zip(reportid, dates, links))
			return DataFrame(list_of_tuples, columns = ['Report_ID', 'Date', 'Link'])

	def download_everything(self, folder:str='./') -> dict:
		all_files = []
		for link in self.df.Link.unique():
			Path(folder).mkdir(parents=True, exist_ok=True)
			filename = join(folder, self.get_filename_from_link(link))
			all_files.append(filename)
			if not exists(filename):
					with urlopen(link) as response, open(filename, 'wb') as out_file:
							copyfileobj(response, out_file)
							print('report downloaded at {}'.format(filename))
			else:
					print("report {} already exists. didn't re-download".format(filename))
		return all_files

	def download_for_date(self, datearg:str, folder:str='./') -> dict:
		dt = dateparse(datearg)
		if dt is None:
				print('the date {} couldnt be parsed'.format(datearg))
				return {}
		else:
				link = list(self.df.loc[self.df['Date'] == dt]['Link'])
				if len(link) == 0:
						print('no record for the date {} found'.format(dt.strftime("%Y/%m/%d")))
						return {}
				else:
						link = link[0]
						Path(folder).mkdir(parents=True, exist_ok=True)
						filename = join(folder, self.get_filename_from_link(link))
						if not exists(filename):
								with urlopen(link) as response, open(filename, 'wb') as out_file:
										copyfileobj(response, out_file)
										print('report for date {} downloaded at {}'.format(dt.strftime("%Y/%m/%d"), filename))
										return {'file': filename, 'data': dt}
						else:
								print("report for the date {} already exists at {}. didn't re-download".format(dt.strftime("%Y/%m/%d"), filename))
								return {'file': filename, 'data': dt}

	def assemble_data(self, request_id:str, parsr_url:str='localhost:3001'):
		parsr = ParserClient(parsr_url)
		table_info = parsr.get_tables_info(request_id)

		dfs = list([parsr.get_table(request_id=request_id,page=table_info[0][0],table=table_info[0][1])])
		columns = dfs[0].columns
		dfs += [parsr.get_table(request_id=request_id,page=i[0],table=i[1],column_names=columns) for i in table_info[1:]]

		return pdconcat(dfs, ignore_index=True)

	def send_document_to_parsr(self, filename:str, parsr_url:str='localhost:3001', config:str='defaultConfig.json', wait_till_finished:bool=True):
		parsr = ParserClient(parsr_url)
		return parsr.send_document(
			file=filename,
			config=config,
			wait_till_finished=wait_till_finished,
		)