import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
sqlDb = mysql.connector.connect(
  host=os.getenv('SQL_HOST'),
  user=os.getenv('SQL_USER'),
  password=os.getenv('SQL_PASSWORD'),
  database=os.getenv('SQL_DATABASE'),
  port=os.getenv('SQL_PORT')
)

sqlCursor = sqlDb.cursor(buffered=True)