# COVID-19 WHO Situation Reports Importer

This python script (and notebook) fetches [situation reports on the Covid-19 outbreak from the World Health Organisation](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports) and renders the report into Markdown, and its data tables into CSVs.

Feel free to use it as a launchpad for any further analysis that would help your visualisations/projects of the currently ongoing pandemic.

## Dataset

All the WHO situation reports in PDF, MD and CSV format are automatically uploaded [here](https://github.com/aarohijohal/Covid19-WHO-Situation-Reports).
New reports are added as they come.

## Download all reports / update the dataset

Requirement: [Python Poetry](https://github.com/python-poetry/poetry)

	poetry install
	cd covid19_who_situation_reports_importer
	poetry run python download_everything.py

By default, reports will be extracted in the folder `data` in the repository root unless differently configured in `download_everything.py`.

## Notebook usage

Requirement: [Python Poetry](https://github.com/python-poetry/poetry)

	poetry install
	poetry run jupyter-lab covid19_who_situation_reports_importer/notebook.ipynb
