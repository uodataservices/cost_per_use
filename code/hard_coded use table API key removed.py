# packages

import requests # for API calls
import xml.etree.ElementTree as ET # to parse XML
import pandas as pd  # to convert XML to dataframes
import time # to add timestamp to csv file names

# define a function to save data from the api call
def extract_rows_from_xml(root, column_xml):
    """
    Extracts rows from an XML tree based on column specifications and returns a list of rows.

    Args:
        root (Element): The root element of the XML tree.
        column_xml (List[str]): A list of strings specifying the column names in the XML tree.

    Returns:
        List[List[str]]: A list of rows, where each row is a list of strings representing the cell values.
    """
    rows = []
    for row in root.findall('.//rowset:Row', {'rowset': 'urn:schemas-microsoft-com:xml-analysis:rowset'}):
        row_values = []
        for col in column_xml:
            cell = row.find(f'.//rowset:{col}', {'rowset': 'urn:schemas-microsoft-com:xml-analysis:rowset'})
            if cell is None:
                row_values.append(None)
            else:
                row_values.append(cell.text)
        rows.append(row_values)
    return rows

# define function to print error messages
def print_error_message(root):
    """
    Prints error messages from the API response.

    Args:
        root (Element): The root element of the XML tree.
    """
    print("Error: ", response.status_code)
    for error_code in root.iter('{http://com/exlibris/urm/general/xmlbeans}errorCode'):
        error_code_output = error_code.text # added this one to test
        print("Error code:", error_code_output)
    for error in root.iter('{http://com/exlibris/urm/general/xmlbeans}errorMessage'):
        print("Error message:", error.text)
    for tracking in root.iter('{http://com/exlibris/urm/general/xmlbeans}trackingId'):
        print("Error tracking id:", tracking.text)

# To run for debugging purposes, set debug = True
debug = False

# Set your Alma Analytics API URL
url = "INSERT ROOT URL HERE"

# Set your Alma Analytics API key
api_key = "INSERT KEY HERE"

# Set your Alma Analytics report path. The requests library adds URL encoding automatically.
path = "INSERT REPORT PATH HERE"

# Set the number of rows to retrieve per API call
page_size = 1000

# Initialize the IsFinished flag to false (notice that the values in XML is a string)
is_finished = "false"

params = {
        "path": path,
        "limit": page_size,
        "apikey": api_key
    }

 # Make the first API call using the requests library
response = requests.get(url, params=params)

# Extract the xml data from the response using Element Tree
root = ET.fromstring(response.content)

# raise errors if the API call was not successful
if response.status_code != 200:
    print_error_message(root)

# Extract the resumption token from the data
for token in root.iter('ResumptionToken'):
    resumption_token = token.text

# Extract the column names from the data
# Get the schema namespace (would it be better to pull this from the xml itself?)
ns = {'xsd': 'http://www.w3.org/2001/XMLSchema',
      'saw-sql': 'urn:saw-sql'}

# Get the column headers (human-readable names) and 
# names (the XML tag names) from the schema as a list
column_names = [elem.attrib['{urn:saw-sql}columnHeading']
                for elem in root.findall('.//xsd:element', ns)]
column_xml = [elem.attrib['name'] # elem.attrib doesn't have 'saw-sql' b/c not in xml
                for elem in root.findall('.//xsd:element', ns)]

# Call function defined at top of document to extract rows from the xml
rows = extract_rows_from_xml(root, column_xml)

# define and append the results to the main row list
results_list = []
results_list.extend(rows)

# Track number of API calls for error investigation/tracking
# Initialize the number of API calls to 1 (counts first call above)
no_of_api_calls = 1

# Loop until IsFinished equals "true"
while is_finished == "false":

    # Track number of API calls for error investigation/tracking
    # Add 1 for each API call
    no_of_api_calls += 1

    # Set the query parameters
    params = {
        "path": path,
        "limit": page_size,
        "token": resumption_token,
        "apikey": api_key
    }

    # Make the API call using the requests library
    response = requests.get(url, params=params)
    if debug == True:
        print(response.request.url)
        print(response.status_code)

    # Extract and parse the xml data from the response
    root = ET.fromstring(response.content)

    # Check if the response was successful and print the error if it wasn't
    if response.status_code != 200:
        print_error_message(root)
        break

    # Extract the IsFinished flag from the data
    for finished in root.iter('IsFinished'):
        is_finished = finished.text

    # Extract and save data from the response
    rows = extract_rows_from_xml(root, column_xml)

    # append the results to the main row list
    results_list.extend(rows)

# Create a dataframe from the rows and column names
df = pd.DataFrame(results_list, columns=column_names)

if debug == True:
    print("Number of API calls:", no_of_api_calls)
    print("Number of rows in list:", len(results_list), 
      "Number of rows in df:", len(df))
    print(response.request.body)
    print(response.request.headers)
    print(response.headers)

timestamp = time.strftime('%Y%m%d-%H%M%S')
filename = f'../data/test_{timestamp}.csv'

# print the DataFrame to the CSV file
# df.to_csv(filename, index=False)

# add print statement to export to Power BI
print(df)
