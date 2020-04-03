from pathlib import Path
import sys
from who_covid_scraper import WHOCovidScraper

def download_everything(
		url='https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports',
		pdf_save_location='../data/pdf',
		csv_save_location='../data/csv',
		md_save_location='../data/md'
		):
	scraper = WHOCovidScraper()
	Path(pdf_save_location).mkdir(parents=True, exist_ok=True)
	Path(csv_save_location).mkdir(parents=True, exist_ok=True)
	Path(md_save_location).mkdir(parents=True, exist_ok=True)
	downloaded_files = scraper.download_everything(folder=pdf_save_location)
	for file in downloaded_files:
		print('-> for file : {}...'.format(file))
		csv_filename = Path(csv_save_location, Path(file).stem).with_suffix('.csv').as_posix()
		md_filename = Path(md_save_location, Path(file).stem).with_suffix('.md').as_posix()
		if not Path(csv_filename).is_file() or not Path(md_filename):
			job = scraper.send_document_to_parsr(file)

			if not Path(csv_filename).is_file():
				print('-> -> generating csv : {}...'.format(csv_filename))
				table_data = scraper.get_table_data(job['server_response'])
				if table_data is not None:
						table_data.to_csv(csv_filename, sep='\t', encoding='utf-8', index=False)
				else:
						print('{} contains no tabular data..'.format(file))
			else:
				print('{} already exists. skipping...'.format(csv_filename))

			if not Path(md_filename).is_file():
				print('-> -> generating md : {}...'.format(md_filename))
				md_data = scraper.get_md_data(job['server_response'])
				if isinstance(md_data, str):
					with open(md_filename, "w") as md_file:
						print(f"{md_data}", file=md_file)
				else:
						print('{} did not return a suitable MD output type: {}'.format(file, type(md_data)))
			else:
				print('{} already exists. skipping...'.format(md_filename))
		else:
			print('md and csv already exist. skipping...')


def main():
	download_everything()
	print('download finished..')

if __name__ == "__main__":
	main()