import mysql.connector

cnx = mysql.connector.connect(user='gfuser', password='gfuser123',
                              host='127.0.0.1',
                              database='gfaculty')
print cnx
cur = cnx.cursor()
cur.execute("SELECT hrm.honorarium_rate FROM honorarium_rate_master hrm, honorarium_category_value_master hcvm, guest_faculty_course_offer gfco, honorarium_category_value_master hcvm1, honorarium_category_master hcm, honorarium_field_key_words hfkw, additional_course_offer_attributes acoa WHERE hrm.category1_value_id = hcvm.value_id AND hrm.category2_value_id = hcvm1.value_id AND hcm.category_id = hrm.category_id AND hcm.category_name = hfkw.key_value_id AND hfkw.field_name = 'lecture_rate_used' AND hrm.active_flag = 1 AND acoa.faculty_role_id = hcvm.category_value AND acoa.course_id = gfco.course_id AND acoa.semester_id = gfco.semester_id AND acoa.guest_faculty_id = gfco.guest_faculty_id")
for row in cur.fetchall():
    print row[1]
cnx.close()
