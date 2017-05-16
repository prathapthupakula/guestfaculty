import mysql.connector

cnx = mysql.connector.connect(user='gfuser', password='gfuser123',
                              host='127.0.0.1',
                              database='gfaculty')
print cnx
cur = cnx.cursor()
cur.execute("SELECT location_id from location ")
cur.fetchall()
for row in cur.fetchall():
    print "location_id: ",row[0]
    cur.execute()
    res=cur.fetchall()
for row in res:
    employee_id = row[0]
    employee_name = row[1]
    insertstmt=("INSERT INTO employee (employee_id,employee_name) values (%d,%s)")
    cur.execute(insertstmt)
    print row[0],row[1]
cnx.commit()
cnx.close()
