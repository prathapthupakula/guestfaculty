import pymysql.cursors
import pymysql

cnx=pymysql.connect(user='gfuser', password='gfuser123',
                              host='127.0.0.1',
                              database='gfaculty')
cur = cnx.cursor()
cur.execute("select * from location")
for row in cur.fetchall():
    print row[0]
    print row[1]
conn.close()
