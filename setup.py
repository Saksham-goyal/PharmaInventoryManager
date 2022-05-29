"""
Python code to define the Flask app and Database conection
"""

from env_lib import *

# Define the database connection
pharmaDB = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="pharmaStock"
)

tableName = "pharmaStock"   # Table name in the database
cursorDB = pharmaDB.cursor(buffered=True)
app = Flask(__name__)   # Define the flask app
app.config["DEBUG"] = True    # enable debugging mode
UPLOAD_FOLDER = 'static/files'    # file saving location
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create and configure logger
logging.basicConfig(filename="data/APILogs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)