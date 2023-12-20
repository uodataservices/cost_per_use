# Cost Per Use Project
This repository includes two things:
   1. The template (`pbit`) for our Power BI code, which includes an embedded Python file that queries the Alma API.
   2. Code and documentation for the Python query to Alma API that we originally built separately from Power BI in order to enable testing and troubleshooting.

## Power BI Template
- The Power BI template (`pbit`) is a zipped/compressed file folder consisting of several underlying code files. If you would prefer to explore the underlying data, you can unzip it and open the files as plain text in your IDE/text reader of choice. The DataModelSchema is a json file that contains information about the final tables. For information on extracting the Power Query (M) code without using Power BI, see https://querypower.com/2017/03/22/extracting-power-queries-in-m/.
- If you would like to read the `.pbit` file in Power BI, note that it will ask you for four parameters before it will allow you to open the file. If you have Alma reports already configured and access to an Alma API key, feel free to enter those. However, you can also just enter "test" into all of the parameter fields. The resulting template will display many loud error codes, but you will still be able to explore the data structure and see all of the data cleaning and processing steps we made.
- Note that code for our project can be found in two places within this Power BI template. If you are exploring the template from within Power BI Desktop, you can find that code
    1. in Power Query, which you can access by selecting "Transform Data" from the main menu, and
    2. in DAX, which you can explore by looking at the "Data view" in the main Power BI interface.

## Python Code Templates
There are three python files in the `code` folder, which we include her in order to allow you to troubleshoot your Python API queries separately from your use of the entire Power BI template:
    1. One is a template for writing a version-controlled python query that uses a `config.ini` file kept only in our local repositories and listed in our `.gitignore` file. See `configsample.txt` for instructions on how to built your own `config.ini` file. This is written expecting to write data into a data folder, as in our structure in this repository.
    2. Two are hard-coded files with our paths, report names, and API key removed. These are written expecting to write data into a data folder, as in our structure in this repository.
If you would like to modify the Python code and then add it to a new Power BI query, be aware that you can need to either include the API key and paths hard-coded within the script, or (we recommend) change those elements in the script to Power Query "parameters."

## Managing Secrets
Secrets are managed in a `config.ini` file that is kept only in our local repositories and listed in our `.gitignore` file. See `configsample.txt` for instructions on how to build your `config.ini` file.

The initial commit didn't include the Jupyter Notebook that the code started with, because the Notebook output sometimes includes urls (and therefore secrets). In case we want to use Jupyter Notebooks in the future, we have added some checks to make sure that only notebooks whose output has been cleared will be added to the repository. We are following the instructions here: https://www.julianklug.com/posts/jupyter-notebook-leak, which include a suggestion to add the GitHub Action Workflow at https://github.com/marketplace/actions/ensure-clean-jupyter-notebooks that is included with this repository.

If we go further with this at some point we may want to ask how our colleagues manage their secrets and follow their protocols. 
