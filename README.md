[![DOI](https://zenodo.org/badge/733708191.svg)](https://zenodo.org/doi/10.5281/zenodo.10426230)

# Cost Per Use Project
This repository is associated with a project UO Libraries to build a Cost Per Use dashboard in Power BI. Kristin Buxton, Lydia Harlan, and Gabriele Hayden are project authors. This project involves automating a pathway to ingest, store, and visualize cost per use data for continuing resources. Our associated paper presents a pipeline for using Alma, SUSHI, COUNTER5, Python, and Power BI to create a tool for data-driven decision making. By establishing this pipeline, we shift the time investment from manually harvesting usage statistics to interpreting the data and sharing it with stakeholders. The resulting visualizations and collected data will assist in making informed, collaborative decisions.  

This repository includes two things:
   1. The template (`pbit`) for our Power BI code, which includes an embedded Python file that queries the Alma API.
   2. Code and documentation for the Python query to Alma API that we originally built separately from Power BI in order to enable testing and troubleshooting.

## Power BI Template
- The Power BI template (`pbit`) is a zipped/compressed file folder consisting of several underlying code files. If you would prefer to explore the underlying data, you can unzip it and open the files as plain text in your IDE/text reader of choice. The DataModelSchema is a json file that contains information about the final tables using a Tabular Object Model schema (https://learn.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions). For information on extracting the Power Query (M) code without using Power BI, you might try https://querypower.com/2017/03/22/extracting-power-queries-in-m/.
- If you would like to read the `.pbit` file in Power BI, note that it will ask you for four parameters before it will allow you to open the file. If you have Alma reports already configured and access to an Alma API key, feel free to enter those. However, you can also just enter "test" into all of the parameter fields. The resulting template will display many loud error codes, but you will still be able to explore the data structure and see all of the data cleaning and processing steps we made.
- Note that code for our project can be found in two places within this Power BI template. If you are exploring the template from within Power BI Desktop, you can find that code
    1. in Power Query, which you can access by selecting "Transform Data" from the main menu, and
    2. in DAX, which you can explore by looking at the "Data view" in the main Power BI interface.

## Python Code Templates
There are three python files in the `code` folder, which we include here in order to allow you to troubleshoot your Python API queries separately from your use of the entire Power BI template:

1. `alma_api_use_query_using_config.py` is a template for writing a version-controlled python query that uses a `config.ini` file kept only in our local repositories and listed in our `.gitignore` file. See `configsample.txt` for instructions on how to built your own `config.ini` file. This is written expecting to write data into a data folder, as in our structure in this repository.
2. `alma_api_cost_query_hard_coded_secrets_removed.py` and `alma_api_use_query_hard_coded_secrets_removed.py` are hard-coded versions of Python queries to our Cost and Use reports in Alma with our paths, report names, and API key removed. These are also written expecting to write data into a data folder, as in our structure in this repository.
   
If you upload this query to Power BI, we recommend that you remove any commands to save dataframes to files (these commands will likely be ignored in any case). It is our understanding that Power BI will recognize any dataframes created in a Python script even if they are not returned or printed by the script. However, we wrote the final, Power BI version of our code following a template that ended with a `print(df)` command at the very end.

When you first add your Python script to Power BI after testing, include the API key and paths hard-coded within the script. However, we recommend that you then change those elements in the script to Power Query "parameters." The basic syntax to do this is to replace your hard coded API key, which might look something like `"98gdg7e89gbo98"` with `"& parameter_name &"`. If you use this syntax, be sure to enter your parameters into Power BI as text strings wrapped in double quotes. See also https://datakuity.com/2021/01/05/power-bi-pass-parameter-value-to-python-script/, which suggests slightly different syntax to arrive at the same result (parameter being correctly read as a string within the Python script).

## Managing Secrets
For the version of our Python script that we can actually run from this repository, secrets are managed in a `config.ini` file that is kept only in our local repositories and listed in our `.gitignore` file. See `configsample.txt` for instructions on how to build your `config.ini` file.

Notebook output sometimes includes urls (and therefore secrets). In case we want to use Jupyter Notebooks in the future, we have added some checks to make sure that only notebooks whose output has been cleared will be added to the repository. We are following the instructions here: https://www.julianklug.com/posts/jupyter-notebook-leak, which include a suggestion to add the GitHub Action Workflow at https://github.com/marketplace/actions/ensure-clean-jupyter-notebooks that is included with this repository.
