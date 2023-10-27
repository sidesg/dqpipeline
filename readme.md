# DQ Pipeline

Simple tool to update file in a list of CKAN resources on Données Québec.

Needs the following files/folders:

- `./updates.yml`: List of key: value pairs where each key is the resource's ID and the value is the name of the file in `data` folder, e.g., `1234-abcd: datafile.csv`.
- `./data`: data files to be uploaded, documented in `updates.yml`.
- `./.creds/apikey.txt`: plain text file containing the Données Québec API key.