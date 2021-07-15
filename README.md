% Azure File Store Data Catalogger

Connects to specified azure file shares and gathers metadata including file path, size, type, created date and modified date. It will also identify current, new and deleted files since the last run.

Recommend scheduling the script to run daily to keep an up to date summary of all your Azure files. Use the "run_catalogger.bat" file as a template.

main.py requires inputs of file share paths and credentials and also the save path for all output files.


![](Screeshots_for_readme/output_example_current_files.png?raw=true "Output Example")
![](Screeshots_for_readme/output_example_sheets.png?raw=true)
