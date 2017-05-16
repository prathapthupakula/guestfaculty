import mysql.connector

cnx = mysql.connector.connect(user='gfuser', password='gfuser123',
                              host='127.0.0.1',
                              database='gfaculty')
print cnx
cur = cnx.cursor()
source_table = 'location'
target_table = 'employee'
cur.execute("SELECT location_id from location ")
data = cur.fetchall()
for row in data:
    print 'location_id:' ,row[0]
    r1=row[0]
    stmt = ("INSERT INTO employee (employee_id,employee_name,location_id) values ('%s','%s','%s')"  %('2','suma',r1))
    cur.execute(stmt)
    cnx.commit()
cur.close()
