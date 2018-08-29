#!/usr/bin/python
import MySQLdb
import os

try:
    db = MySQLdb.connect(host=os.environ['MYSQL_CONTAKTO_PORT_3306_TCP_ADDR'], 
                          user=os.environ['CONTAKTO_DB_USER'], 
                          passwd=os.environ['CONTAKTO_DB_PASSWORD'], 
                          db=os.environ['CONTAKTO_DB_NAME'])
    cursor = db.cursor()        
    cursor.execute("SELECT VERSION()")
    results = cursor.fetchone()
    print "cool", results             
except MySQLdb.Error:
    print "ERROR IN CONNECTION"