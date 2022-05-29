"""
Python modules to define and run the Flask app
Contians the APIs for :
1) Uploading the CSV file and index data to the database
2) Query end point where filter based searches can be fetched
"""

# Importing helper resources
from env_lib import *
from setup import *
from pharmaHelper import *

# Root URL to load the CSV file upload page
@app.route('/')
def index():
    return render_template('index.html')   # Setting the upload HTML template '\templates\index.html'

# Get the uploaded files, parse it and index to the database
@app.route("/", methods=['POST'])
def uploadFiles():
    logger.info("CSV upload module initiated!")
    uploaded_file = request.files['file']   # Get the uploaded file
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)   # Set file path
        uploaded_file.save(file_path)    # Save the file
        parseCSVAndAddData(file_path)    # Parses the CSV file and uploads to the database
    logger.info("CSV successfully parsed and indexed to the database!")
    return redirect(url_for('index'))   # Redirects the UI to the upload CSV page

# API end point to fetch pharma and supplier data based on the filters - POST method
@app.route('/getStockForSupplier')
def getStockForSupplier():
    logger.info("Query initiated for fetching data!")
    # Defining the base SQL query
    query = "SELECT DISTINCT code as \"PRODUCT CODE\", name as \"PRODUCT NAME\", supplier as \"SUPPLIER\", DATE_FORMAT(exp,\"%M %d %Y\") as \"EXPIRY DATE\" FROM " + tableName
    filters = []    # To add WHERE clause filters

    # Check for SUPPLIER filter in the POST method
    if('supplier' in request.args):
        supplierList = request.args.get('supplier').split(',')
        supplierQuery = ""
        for sup in supplierList:
            supplierQuery += supplierQuery + ",'" + sup + "'"
        supplierQuery = supplierQuery[1:]
        filters.append("supplier in (" + supplierQuery + ")")    # Adding filter for WHERE clause

    # Check for search parameter filter in the POST method
    if('searchParam' in request.args):
        searchParam = request.args.get('searchParam')
        filters.append("name like '%" + searchParam +"%'")      # Adding filter for WHERE clause

    # Check for expiry date flag in the POST method
    if('expiryFlag' in request.args and request.args['expiryFlag'] == 'True'):
        filters.append("exp > CURDATE()")       # Adding filter for WHERE clause

    # Add WHERE clause filters to the main SQL query
    if(len(filters) > 0):
        filterStr = " AND ".join(filters)
        query += " WHERE " + filterStr

    # Add ORDER clause for ordering the results based on SUPPLIER
    query += " ORDER BY supplier;"

    # ADD Pagination logic to the base query
    if ('page' in request.args):
        pageNum = request.args.get('page')    # Get page index form POST request
        perPage = 20    # Setting the page size
        startsAt = int(pageNum) * int(perPage)    # Setting the start index
        query = query[:-1] + " LIMIT " + str(startsAt) + " , " + str(perPage) + ";"
    logger.info("Query: " + query)
    response = runQuery(query)    # Run the query on the indexed data
    logger.info("Query successfully executed!")
    return render_template('results.html', Jinja_list=response)

# Main function to activate the flask app
if (__name__ == "__main__"):
    logger.info("Initiating the FLASK app!")
    app.run(port=5000)   # Activate the flask app
