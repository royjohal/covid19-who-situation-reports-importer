# COVID-19 WHO Situation Reports Importer

This python notebook fetches [situation reports on the Covid-19 outbreak from the World Health Organisation](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports) and renders the data tables as Pandas Dataframes.

Feel free to use it as a launchpad for any further analysis that would help your visualisations/projects of the currently ongoing pandemic.


## Usage

Requirement: [Python Poetry](https://github.com/python-poetry/poetry)

To install the packages and open the notebook, execute inside the root folder:

	poetry install
	poetry run jupyter-lab covid19_who_situation_reports_importer/notebook.ipynb
