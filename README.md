# Finances automation

[![CircleCI](https://circleci.com/gh/cortadocodes/finances-automation/tree/master.svg?style=svg)](https://circleci.com/gh/cortadocodes/finances-automation/tree/master)

## Usage
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
