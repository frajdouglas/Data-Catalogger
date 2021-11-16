# Data Catalogger

This script will produce a summary excel spreadsheet for your file metadata. It is capable of collating data from your local files or your Azure File Share.

Metadata includes file path, size, type, created date and modified date. It will also identify current, new and deleted files since the last run.

Scheduling the script to run daily will keep an up to date summary of all your files. Use the "run_catalogger.bat" file as a template.

## Example Outputs

![](Screenshots_for_readme/output_example_current_files.png?raw=true "Output Example")
![](Screenshots_for_readme/output_example_sheets.png?raw=true)

## Instructions for Setup

The minimum version of Python required is: 3.0.

main.py requires inputs of file share paths and credentials and also the save path for all output files.

Copy the bash terminal commands below to complete the setup for this project: ( NEEDS UPDATING )

```
git clone https://github.com/frajdouglas/reddit_clone.git

npm install -D

touch .env.development

echo PGDATABASE=nc_news >> .env.development

touch .env.test

echo PGDATABASE=nc_news_test >> .env.test

npm run setup-dbs

npm run seed

npm test

```

## Process Flow (For azure file catalogging)
![](Screenshots_for_readme/process_flow.png?raw=true)
