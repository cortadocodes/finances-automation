# Finances automation

[![CircleCI](https://circleci.com/gh/cortadocodes/finances-automation/tree/master.svg?style=svg)](https://circleci.com/gh/cortadocodes/finances-automation/tree/master)

## Installation
### Pull and start the database container
To pull and start the persistent `postgres` database container, run
```bash
POSTGRES_DB=postgres POSTGRES_USER=postgres POSTGRES_PASSWORD=<password> \
docker run -d -p 5433:5432 \
-v <absolute_path_to_desired_data_location_on_host>:/var/lib/postgresql/data \ 
--name postgres-finances-automation postgres:11
```
where `<password>` is your choice of password for the database, and `<absolute_path_to_desired_data_location_on_host>`
is the location in which to store the database cluster on your machine. The database password can be stored locally by 
setting it as an environment variable, or declared with each command run.

After the database has been pulled and started for the first time, it can be stopped by
```bash
docker stop postgres-finances-automation
```
and started again by
```bash
docker start postgres-finances-automation
```
The database container must be running for any of the below commands to work properly.

### Install the package
```bash
pip3 install -e .[development]
```
or
```bash
pip3 install setup.py
```

## Configuration/initialisation
The configuration for the database, tables, categories and more is included in `finances_automation/configuration.py`.
To initialise the database with the tables from the configuration file, run
```bash
python3 finances_automation/initialise_database.py
```
from the repository root.

## Usage
From the repository root and with the `POSTGRES_PASSWORD` set, run
```bash
finances-automation --help
```

The output will look like this:
```
usage: finances-automation [-h] {parse,categorise,analyse,view_latest} ...

Automate your finances analysis.

optional arguments:
  -h, --help            show this help message and exit

Subcommands:
  {parse,categorise,analyse,view_latest}
    parse               Parse a UTF-8 .csv financial statement.
    categorise          Categorise transactions from a transactions table.
    analyse             Analyse transactions from a transactions table.
    view_latest         View the latest entries to a table.
```

## Running tests
From the repository root, run:
```bash
pytest
```

## Aims
The aim of this project is to automate the manual review of my finances I carry out each month in Excel. The 
project will involve:
* Automating the ingestion of financial statements in `.csv` or `.xlsx` format
* Creating a database for financial data
* Automating the categorisation of each transaction into e.g. `travel`, `food` etc. This will require some machine 
learning, although will initially be carried out manually by asking the user to label each transaction. This manual 
method will still be quicker and easier than the current method, and has the secondary use of creating a labelled 
dataset for a model to be trained on
* Calculating the expenditure in each category and producing summary statistics related to a pre-defined budget. This
 will include e.g. average expenditures (monthly, yearly etc.) and a forecast based on previous months/years.
* Creating a dashboard displaying these statistics in an elegant and insightful fashion (I'll probably use `seaborn` 
here). The interface will allow the user to see statistics for different date ranges and bank accounts.
* Providing a command line interface to the above
