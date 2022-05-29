"""
Python modules to enable the Fask app and backend API logic
"""

from env_lib import *
from setup import *

# Module to validate the date from "exp"
def validDate(date):
    dateRegex = "^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$"    # regex pattern to check for DD/MM/YYYY format
    if re.search(dateRegex, date):
        return True
    else:
        return False

# Module to read the CSV file, parse it and index to database
def parseCSVAndAddData(filePath):
    logger.info("Parsing the CSV file!")
    columnNames = ['code', 'name', 'batch', 'stock', 'deal', 'free', 'mrp', 'rate', 'exp', 'company', 'supplier']     # CSV Column Names
    csvData = pd.read_csv(filePath, names=columnNames, header=None)       # Use Pandas to parse the CSV file
    csvData.drop([0], axis=0, inplace=True)     # Drop the column names' row
    # Loop through the Rows
    for i, row in csvData.iterrows():
        value = ()
        validCols = ""      # For each row, this will store the valid columns in the row
        formatting = ""     # For formatting purpose of the final query

        for col in columnNames:
            val = row[col]
            if not pd.isnull(val):
                if col == "exp":
                    if not validDate(val):
                        continue
                    else:
                        val = datetime.datetime.strptime(val, "%d/%m/%Y").strftime("%Y-%m-%d")      # Reformat the date to YYYY-MM-DD

                value += (val,)
                validCols += str(col) + ","
                formatting += "%s,"

        validCols = validCols[:-1]
        formatting = formatting[:-1]
        query = "INSERT INTO " + tableName + " (" + validCols + ") VALUES (" + formatting + ")"     # SQL query to add data to the databse table
        runQuery(query, value)
    return

# Converts list to tuple
def convert(list):
    tup = tuple()
    for item in list:
        temp_tup = (item,)
        tup = tup + temp_tup
    return tup

# Executes query on the database
def runQuery(query, value=None):
    if(value is None):
        cursorDB.execute(query)
    else:
        cursorDB.execute(query, value)
    pharmaDB.commit()
    return cursorDB

