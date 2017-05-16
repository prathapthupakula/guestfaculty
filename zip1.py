import mysql.connector

cnx = mysql.connector.connect(user='gfuser', password='gfuser123',
                              host='127.0.0.1',
                              database='gfaculty')
print cnx
cur = cnx.cursor()
cur.execute("select * from location")
for row in cur.fetchall():
    print row[0]
    print row[1]
cnx.close()
