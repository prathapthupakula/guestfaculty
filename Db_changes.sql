ALTER TABLE `auth_user`
CHANGE `username` `username` varchar(254) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `is_superuser`,
COMMENT='';


ALTER TABLE `coordinator`
CHANGE `email` `email` varchar(254) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `mobile`,
COMMENT=''; 


ALTER TABLE `guest_faculty`
CHANGE `email` `email` varchar(254) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `date_of_birth`,
COMMENT='';


ALTER TABLE `guest_faculty_candidate`
CHANGE `email` `email` varchar(254) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `date_of_birth`,
COMMENT='';


23/12/2015

ALTER TABLE `guest_faculty_feedback_results`
ADD `id` int(11) NOT NULL AUTO_INCREMENT UNIQUE FIRST,
COMMENT='';


ALTER TABLE `guest_faculty_feedback_results`
ADD UNIQUE `guest_faculty_pan_number` (`guest_faculty_pan_number`, `semester_id`, `program_id`, `course_id`, `survey_id`, `survey_version_id`, `survey_question_id`),
ADD INDEX `id` (`id`),
DROP INDEX `PRIMARY`,
DROP INDEX `id`;


ALTER TABLE `guest_faculty_feedback_results`
ADD PRIMARY KEY `id` (`id`),
DROP INDEX `id`;
