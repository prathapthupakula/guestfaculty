import mysql.connector

cnx = mysql.connector.connect(user='gfuser', password='gfuser123',
                              host='127.0.0.1',
                              database='gfaculty')
print cnx
cur = cnx.cursor()
cur.execute("SELECT * FROM location where location_id = 20")
print cur.execute
