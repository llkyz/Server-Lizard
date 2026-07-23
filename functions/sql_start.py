import mysql.connector
import os
from dotenv import load_dotenv

class SQL(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(SQL, cls).__new__(cls)
    return cls.instance

  def __init__(self):
    self.connectSQL()

  def connectSQL(self):
    load_dotenv()
    self.sqlDb = mysql.connector.connect(
      host=os.getenv('SQL_HOST'),
      user=os.getenv('SQL_USER'),
      password=os.getenv('SQL_PASSWORD'),
      database=os.getenv('SQL_DATABASE'),
      port=os.getenv('SQL_PORT')
    )

    self.sqlCursor = self.sqlDb.cursor(buffered=True)
    print("Connected SQL")

  def execute(self, sql, val=None):
    if val is None:
      self.sqlCursor.execute(sql)
    else:
      self.sqlCursor.execute(sql,val)

  def fetchall(self):
    return self.sqlCursor.fetchall()
  
  def fetchone(self):
    return self.sqlCursor.fetchone()

  def commit(self):
    self.sqlDb.commit()

SQLObject = SQL()
