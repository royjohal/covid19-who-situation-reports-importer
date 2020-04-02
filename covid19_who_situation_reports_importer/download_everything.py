from pathlib import Path
import sys
from who_covid_scraper import WHOCovidScraper

def download_everything(
    url='https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports',
    pdf_save_location='./data/pdf',
    csv_save_location='./data/csv'
    ):
  scraper = WHOCovidScraper()
  downloaded_files = scraper.download_everything(folder=pdf_save_location)
  for file in downloaded_files:
      file_csv = Path(csv_save_location, Path(file).stem).with_suffix('.csv').as_posix()
      if not Path(file_csv).is_file():
          print('generating {}...'.format(file_csv))
          job = scraper.send_document_to_parsr(file)
          data = scraper.assemble_data(job['server_response'])
          if data is not None:
              data.to_csv(file_csv, sep='\t', encoding='utf-8', index=False)
          else:
              print('{} contains no tabular data..'.format(file))
      else:
          print('{} already exists. skipping...'.format(file_csv))


def main():
  download_everything()
  print('download finished..')

if __name__ == "__main__":
  main()