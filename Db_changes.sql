--- Removed constraints of Program/Location/Status from this
ALTER TABLE  `gfaculty`.`guest_faculty_course_offer` DROP INDEX  `un_course_location_semester1_idx` ,
ADD UNIQUE  `un_course_location_semester1_idx` (  `course_id` ,  `guest_faculty_id` ,  `semester_id` )