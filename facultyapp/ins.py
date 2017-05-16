source_table = 'table1'
target_table = 'test_table1'

stmt = "SELECT * FROM %s" % source_table

cursor.execute(stmt)
data = cursor.fetchall()

for row in data:
    stmt = "insert into %s values " % target_table + str(row)
    stmt = stmt.replace("u'", '"')
    stmt = stmt.replace("'", '"')
    stmt = stmt.replace(' None', ' Null')
    cursor.execute(stmt)
    connection.commit()

connection.close()
