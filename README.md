# COVID-19 WHO Situation Reports Importer

This python notebook fetches [situation reports on the Covid-19 outbreak from the World Health Organisation](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports) and renders the data tables as Pandas Dataframes.

Feel free to use it as a launchpad for any further analysis that would help your visualisations/projects of the currently ongoing pandemic.

## Dataset

All the WHO situation reports (in PDF) are available [here](https://github.com/aarohijohal/covid19-who-situation-reports-importer/tree/master/data/pdf) and the extracted tabular data from each report [here](https://github.com/aarohijohal/covid19-who-situation-reports-importer/tree/master/data/csv).

New reports are added as they come.

## Download all reports / update the dataset

Requirement: [Python Poetry](https://github.com/python-poetry/poetry)

	poetry install
	poetry run python covid19_who_situation_reports_importer/download_everything.py

## Notebook usage

Requirement: [Python Poetry](https://github.com/python-poetry/poetry)

	poetry install
	poetry run jupyter-lab covid19_who_situation_reports_importer/notebook.ipynb
