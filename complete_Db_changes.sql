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

08/01/2016
ALTER TABLE  `course_location_semester_detail` CHANGE  `assigned_count`  `assigned_count` INT( 11 ) NOT NULL DEFAULT  '0'

ALTER TABLE  `course_location_semester_detail` ADD  `accepted_count` INT( 11 ) NOT NULL DEFAULT  '0'



13/01/2016  GF PLAN TABLES

DROP TABLE IF EXISTS `application_users`;
CREATE TABLE IF NOT EXISTS `application_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `application_name` varchar(50) NOT NULL,
  `user` varchar(255) NOT NULL,
  `role_name` varchar(225) NOT NULL,
  `role_parameters` varchar(225) NOT NULL,
  `created_on` datetime NOT NULL,
  `created_by` varchar(50) NOT NULL,
  `last_updated_on` datetime NOT NULL,
  `last_updated_by` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=71 ;

-- --------------------------------------------------------

--
-- Table structure for table `buffer_type`
--

DROP TABLE IF EXISTS `buffer_type`;
CREATE TABLE IF NOT EXISTS `buffer_type` (
  `buffer_calc_id` int(11) NOT NULL AUTO_INCREMENT,
  `buffer_percentage` decimal(10,2) NOT NULL,
  `buffer_name` varchar(20) NOT NULL,
  PRIMARY KEY (`buffer_calc_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=14 ;

-- --------------------------------------------------------

--
-- Table structure for table `current_semester`
--

DROP TABLE IF EXISTS `current_semester`;
CREATE TABLE IF NOT EXISTS `current_semester` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `currentsemester_id` int(11) NOT NULL,
  `created_on_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `currentsemester_id` (`currentsemester_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=37 ;

-- --------------------------------------------------------

--
-- Table structure for table `guest_faculty_planning_numbers`
--

DROP TABLE IF EXISTS `guest_faculty_planning_numbers`;
CREATE TABLE IF NOT EXISTS `guest_faculty_planning_numbers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `program_coordinator_id` int(11) NOT NULL,
  `location_id` int(11) NOT NULL,
  `course_id` varchar(10) NOT NULL,
  `program_id` int(11) NOT NULL,
  `semester_id` int(11) NOT NULL,
  `discipline_id` int(11) NOT NULL,
  `version_number` int(11) NOT NULL,
  `buffer_type_id` int(11) NOT NULL,
  `current_plan_flag` tinyint(1) NOT NULL,
  `plan_status` varchar(15) NOT NULL,
  `total_faculty_required` int(11) NOT NULL,
  `faculty_in_database` int(11) NOT NULL,
  `faculty_to_be_recruited` int(11) DEFAULT NULL,
  `buffer_number` int(11) DEFAULT NULL,
  `to_be_recruited_with_buffer` int(11) DEFAULT NULL,
  `planning_comments` varchar(2000) DEFAULT NULL,
  `created_by_id` int(11) NOT NULL,
  `created_on` datetime NOT NULL,
  `last_updated_on` datetime DEFAULT NULL,
  `updated_by_id` int(11) DEFAULT NULL,
  `approver_comments` varchar(2000) DEFAULT NULL,
  `approved_rejected_by_id` int(11) DEFAULT NULL,
  `approved_rejected_on` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_guest_faculty_planning_numbers_coordinator1_idx` (`program_coordinator_id`),
  KEY `fk_guest_faculty_planning_numbers_location1_idx` (`location_id`),
  KEY `fk_guest_faculty_planning_numbers_course1_idx` (`course_id`),
  KEY `fk_guest_faculty_planning_numbers_program1_idx` (`program_id`),
  KEY `fk_guest_faculty_planning_numbers_semester1_idx` (`semester_id`),
  KEY `fk_guest_faculty_planning_numbers_discipline1_idx` (`discipline_id`),
  KEY `fk_guest_faculty_planning_numbers_buffer_type1_idx` (`buffer_type_id`),
  KEY `	fk_guest_faculty_planning_numbers_create_user1_idx` (`created_by_id`),
  KEY `fk_guest_faculty_planning_numbers_update_user1_idx` (`updated_by_id`),
  KEY `	fk_guest_faculty_planning_numbers_approve_user1_idx` (`approved_rejected_by_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=252 ;

-- --------------------------------------------------------

--
-- Table structure for table `planning_window_status`
--

DROP TABLE IF EXISTS `planning_window_status`;
CREATE TABLE IF NOT EXISTS `planning_window_status` (
  `planning_id` int(11) NOT NULL AUTO_INCREMENT,
  `semester_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `status` varchar(15) NOT NULL,
  `updated_by_id` int(11) NOT NULL,
  `last_updated_date` datetime NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  PRIMARY KEY (`planning_id`,`semester_id`,`program_id`),
  KEY `fk_planning_window_status_semester1_idx` (`semester_id`),
  KEY `fk_planning_window_status_program1_idx` (`program_id`),
  KEY `fk_planning_window_status_by1_idx` (`updated_by_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=73 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `current_semester`
--
ALTER TABLE `current_semester`
  ADD CONSTRAINT `current_semester_ibfk_1` FOREIGN KEY (`currentsemester_id`) REFERENCES `semester` (`semester_id`);

--
-- Constraints for table `guest_faculty_planning_numbers`
--
ALTER TABLE `guest_faculty_planning_numbers`
  ADD CONSTRAINT `guest_faculty_planning_numbers_ibfk_4` FOREIGN KEY (`program_coordinator_id`) REFERENCES `coordinator` (`coordinator_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_guest_faculty_planning_numbers_buffer_type1` FOREIGN KEY (`buffer_type_id`) REFERENCES `buffer_type` (`buffer_calc_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_guest_faculty_planning_numbers_course1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_guest_faculty_planning_numbers_discipline1` FOREIGN KEY (`discipline_id`) REFERENCES `discipline` (`discipline_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_guest_faculty_planning_numbers_location1` FOREIGN KEY (`location_id`) REFERENCES `location` (`location_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_guest_faculty_planning_numbers_program1` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_guest_faculty_planning_numbers_semester1` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`semester_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `guest_faculty_planning_numbers_ibfk_1` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `guest_faculty_planning_numbers_ibfk_2` FOREIGN KEY (`updated_by_id`) REFERENCES `auth_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `guest_faculty_planning_numbers_ibfk_3` FOREIGN KEY (`approved_rejected_by_id`) REFERENCES `auth_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `planning_window_status`
--
ALTER TABLE `planning_window_status`
  ADD CONSTRAINT `planning_window_status_ibfk_2` FOREIGN KEY (`updated_by_id`) REFERENCES `auth_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_planning_window_status_program1` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_planning_window_status_semester1` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`semester_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

  
===================================================
--- Removed constraints of Program/Location/Status from this
ALTER TABLE  `gfaculty`.`guest_faculty_course_offer` DROP INDEX  `un_course_location_semester1_idx` ,
ADD UNIQUE  `un_course_location_semester1_idx` (  `course_id` ,  `guest_faculty_id` ,  `semester_id` )





========================================================================20/01/2016
ALTER TABLE `semester_timetable_edit_window` 
CHANGE `timetable_owner_id` `timetable_owner_id` int(11) NULL AFTER `location_id`,
COMMENT='';

ALTER TABLE `semester_milestone_plan_master`
CHANGE `alternate_owner_id` `alternate_owner_id` int(11) NULL AFTER `milestone_plan_owner_id`,
COMMENT='';

=========================================================================21/01/2016

ALTER TABLE `semester_timetable_edit_window`
ADD UNIQUE `semester_id_program_id_location_id` (`semester_id`, `program_id`, `location_id`);

========================================================================22/01/2016

ALTER TABLE `semester_milestone_plan_master`
CHANGE `milestone_plan_owner_id` `milestone_plan_owner_id` int(11) NULL AFTER `discipline_id`,
COMMENT='';


ALTER TABLE `semester_milestone_plan_detail`
CHANGE `created_date` `created_date` datetime NULL AFTER `created_by`,
COMMENT=''; -- 0.260


=================================================================================6/02/2016


ALTER TABLE `semester_milestone_plan_detail`
CHANGE `start_date` `start_date` datetime NULL AFTER `semester_milestone_id`,
CHANGE `end_date` `end_date` datetime NULL AFTER `start_date`,
CHANGE `event_date` `event_date` datetime NULL AFTER `end_date`,
COMMENT=''; -- 0.394 s
=====================================================================================08/02/2016
ALTER TABLE `semester_milestone_plan_detail`
ADD `is_milestone` tinyint(1) NOT NULL AFTER `date_editable`,
COMMENT=''; -- 0.305 s
========================================================================================10/02/2016
ALTER TABLE `coordinator`
CHANGE `coordinator_id` `coordinator_id` int(11) NULL FIRST,
COMMENT=''; -- 0.253 s
====================================================================
ALTER TABLE `coordinator`
ADD INDEX (`coordinator_id`),
DROP INDEX `PRIMARY`; -- 0.252 s

=====================================================================16/02/2016===============================
ALTER TABLE `semester_milestone_plan_master`
CHANGE `semester_plan_name` `semester_plan_name` varchar(200) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `version_number`,
COMMENT=''; -- 0.276 s

=======================================================================19/02/2016=================



ALTER TABLE `semester_milestone_plan_master`
DROP FOREIGN KEY `semester_milestone_plan_master`,
ADD FOREIGN KEY (`alternate_owner_id`) REFERENCES `coordinator` (`coordinator_id`) ON DELETE RESTRICT ON UPDATE RESTRICT; 


ALTER TABLE `semester_milestone_plan_master`
DROP INDEX `alternate_owner_id`;


select CONSTRAINT_NAME,COLUMN_NAME from INFORMATION_SCHEMA.KEY_COLUMN_USAGE where TABLE_NAME = 'semester_milestone_plan_master';

ALTER TABLE semester_milestone_plan_master DROP FOREIGN KEY `semester_milestone_plan_master_ibfk_10`;


ALTER TABLE `semester_milestone_plan_master`
DROP FOREIGN KEY `semester_milestone_plan_master_ibfk_10`;


alter table semester_milestone_plan_master drop foreign key alternate_owner_id


DELETE FROM semester_milestone_plan_master

ALTER TABLE `semester_milestone_plan_master`
CHANGE `alternate_owner_id` `secondary_owner_id` int(11) NULL AFTER `milestone_plan_owner_id`,
COMMENT='';


ALTER TABLE `semester_milestone_plan_master`
ADD INDEX `secondary_owner_id` (`secondary_owner_id`);


ALTER TABLE `semester_milestone_plan_master`
ADD FOREIGN KEY (`secondary_owner_id`) REFERENCES `coordinator` (`coordinator_id`);



=========================================================================24/02/2016=====================impp
ALTER TABLE candidate_evaluation CHANGE assessment_score assessment_score DECIMAL(10,2)






ALTER TABLE `guest_faculty_qualification`
CHANGE `percent_marks_cpi_cgpa` `percent_marks_cpi_cgpa` decimal(10,0) NULL AFTER `highest_qualification`,
CHANGE `max_marks_cpi_cgpa` `max_marks_cpi_cgpa` decimal(10,0) NULL AFTER `percent_marks_cpi_cgpa`,
CHANGE `normalized_marks_cpi_cgpa` `normalized_marks_cpi_cgpa` decimal(10,0) NULL AFTER `inserted_date`,
COMMENT=''; -- 0.244 s




Update guest_faculty set nature_of_current_job_id = NULL


ALTER TABLE `ara_application`
CHANGE `country` `country` int(11) NOT NULL AFTER `email`,
COMMENT='';



==========================================================18/03/2016=====================

CREATE TABLE `nature_of_current_job` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE guest_faculty
CHANGE `nature_of_current_job` `nature_of_current_job_id` int(11) NULL AFTER `industry_exp_in_months`,
COMMENT=''; -- 0.274 s


ALTER TABLE guest_faculty
ADD FOREIGN KEY (`nature_of_current_job_id`) REFERENCES `nature_of_current_job` (`id`); -- 0.217 s

ALTER TABLE guest_faculty
ADD INDEX `nature_of_current_job_id` (`nature_of_current_job_id`); -- 0.172 s



===========================================================================================================22/03/2016==========================

alter table guest_faculty_qualification  MODIFy highest_qualification  decimal(10,0) null;
alter table guest_faculty_qualification  MODIFy normalized_marks_cpi_cgpa  decimal(10,0) null;
alter table guest_faculty_qualification  MODIFy max_marks_cpi_cgpa  decimal(10,0) null;   
alter table guest_faculty_qualification  MODIFY completed tinyint(1)  NULL;

alter table candidate_qualification  MODIFY max_marks_cpi_cgpa decimal(10,0)  NULL;
alter table candidate_qualification  MODIFY normalized_marks_cpi_cgpa decimal(10,0)  NULL;
alter table candidate_qualification  MODIFY completed tinyint(1)  NULL;





alter table guest_faculty_candidate MODIFY months_in_curr_org int(11)  NULL;
alter table guest_faculty_candidate MODIFY total_experience_in_months int(11) DEFAULT NULL;
alter table guest_faculty_candidate MODIFY total_experience_in_months int(11)  NULL;

====================================25/03/16/=====================================================================================
 alter table semester_milestone_plan_detail  MODIFy milestone_comments varchar(45) null;

==========================================================================================30/03/2016=================================
ALTER TABLE `guest_faculty_qualification`
CHANGE `percent_marks_cpi_cgpa` `percent_marks_cpi_cgpa` decimal(10,2) NULL AFTER `highest_qualification`,
COMMENT=''; -- 0.340 s

==========================================1/4/2016============================================================================================
ALTER TABLE `guest_faculty_course_offer`
ADD `honorarium_amount_paid` double(10,2) NULL AFTER `honorarium_payment_mode`,
ADD `honorarium_pay_date` datetime NULL AFTER `honorarium_amount_paid`,
COMMENT='';


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++4/04/2016/=======================================================
ALTER TABLE `auth_user`
ADD `pan_number` varchar(10) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `last_name`,
COMMENT=''; -- 0.293 s

ALTER TABLE `auth_user`
ADD `pan_number` varchar(10) COLLATE 'latin1_swedish_ci' NULL AFTER `email`,
COMMENT=''; 
=============================================================================================================

ALTER TABLE `guest_faculty_course_offer`
ADD INDEX `sequence_number` (`sequence_number`);


ALTER TABLE `guest_faculty_course_offer`
DROP INDEX `sequence_number`; -- 0.145 s



========================================================================================11/04/2016===================================


select CONSTRAINT_NAME,COLUMN_NAME from INFORMATION_SCHEMA.KEY_COLUMN_USAGE where TABLE_NAME = 'guest_faculty_course_offer';


ALTER TABLE `guest_faculty_course_offer` ADD UNIQUE `course_id_guest_faculty_id_semester_id_sequence_number` (`course_id`, `guest_faculty_id`, `semester_id`, `sequence_number`), DROP INDEX `un_course_location_semester1_idx`;

delete from guest_faculty_course_offer;


select * from guest_faculty_course_offer where CONSTRAINT_TYPE='UNIQUE';

SET NAMES utf8;

DROP TABLE IF EXISTS `guest_faculty_course_offer`;
CREATE TABLE `guest_faculty_course_offer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` varchar(10) NOT NULL,
  `semester_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `guest_faculty_id` int(11) NOT NULL,
  `location_id` int(11) NOT NULL,
  `course_offer_status` varchar(10) NOT NULL,
  `sequence_number` int(11) NOT NULL,
  `program_coordinator_id` int(11) NOT NULL,
  `offer_to_faculty_date` datetime NOT NULL,
  `number_students_in_class` int(11) NOT NULL,
  `section` varchar(20) DEFAULT NULL,
  `honorarium_given` tinyint(1) DEFAULT NULL,
  `honorarium_text` varchar(1000) DEFAULT NULL,
  `hon_issued_on_date` datetime DEFAULT NULL,
  `hon_issued_by` varchar(200) DEFAULT NULL,
  `honorarium_payment_mode` varchar(45) DEFAULT NULL,
  `honorarium_amount_paid` double(10,2) DEFAULT NULL,
  `honorarium_pay_date` datetime DEFAULT NULL,
  `insert_datetime` datetime NOT NULL,
  `update_datetime` datetime NOT NULL,
  `max_faculty_count_reached` tinyint(1) NOT NULL DEFAULT '0',
  `assessment_score` decimal(10,2) DEFAULT NULL,
  `feedback` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_id_guest_faculty_id_semester_id_sequence_number` (`course_id`,`guest_faculty_id`,`semester_id`,`sequence_number`),
  KEY `fk_guest_faculty_has_course_course1_idx` (`course_id`),
  KEY `fk_guest_faculty_has_course_semester1_idx` (`semester_id`),
  KEY `fk_guest_faculty_course_offer_program1_idx` (`program_id`,`program_coordinator_id`),
  KEY `fk_guest_faculty_course_offer_location1_idx` (`location_id`),
  KEY `fk_guest_faculty_course_offer_guest_faculty1_idx` (`guest_faculty_id`),
  KEY `fk_guest_faculty_course_offer_coordinator1_idx` (`program_coordinator_id`),
  CONSTRAINT `fk_guest_faculty_course_offer_location1` FOREIGN KEY (`location_id`) REFERENCES `location` (`location_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_guest_faculty_has_course_course1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_guest_faculty_has_course_semester1` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`semester_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `guest_faculty_course_offer_ibfk_3` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `guest_faculty_course_offer_ibfk_4` FOREIGN KEY (`guest_faculty_id`) REFERENCES `guest_faculty` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `guest_faculty_course_offer_ibfk_6` FOREIGN KEY (`program_coordinator_id`) REFERENCES `coordinator` (`coordinator_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
============================================================================
ALTER TABLE `guest_faculty`
CHANGE `updated_by` `updated_by` int(11) NULL AFTER `inserted_date`,
COMMENT=''; -- 0.326 s
============================================11/04/16===========================================================================
ALTER TABLE `semester_timetable_edit_window`
CHANGE `exam_date` `exam_date` datetime NULL AFTER `deadline_approval_date`,
COMMENT=''; -- 0.330 s
ALTER TABLE `semester_timetable_edit_window`
CHANGE `days_before_exam` `days_before_exam` int NULL AFTER `exam_date`,
COMMENT='';
ALTER TABLE `semester_milestone`
CHANGE `max_duration_in_days` `max_duration_in_days` int(11) NULL AFTER `active`,
COMMENT=''; -- 0.535 s
=====================================================================18/4/2016/=========================================================================================
"""""changes im programtable""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
ALTER TABLE `program`
ADD `program_code` varchar(20) NOT NULL AFTER `program_id`,
CHANGE `program_coordinator_id` `program_coordinator_id` int(11) NULL AFTER `client_organization`,
COMMENT=''; -- 0.665 s


==========================================================================02/05/2016==============================================================

ALTER TABLE `semester_milestone_plan_detail` CHANGE `event_date` `event_date` date NULL AFTER `end_date`,COMMENT='';

=============================================================================================================================03/05/2016========================

ALTER TABLE `coordinator`
CHANGE `email` `email` varchar(254) COLLATE 'latin1_swedish_ci' NULL AFTER `mobile`,
COMMENT=''; -- 0.374 s

=============================================================================================16/05/2016=====================================

ALTER TABLE `candidate_qualification`
CHANGE `percent_marks_cpi_cgpa` `percent_marks_cpi_cgpa` decimal(10,2);
ALTER TABLE `candidate_qualification`
CHANGE `normalized_marks_cpi_cgpa` `normalized_marks_cpi_cgpa` decimal(10,2);
ALTER TABLE `candidate_qualification`
CHANGE `max_marks_cpi_cgpa` `max_marks_cpi_cgpa` decimal(10,2);
=========================================
ALTER TABLE `program`
CHANGE `program_code` `program_code` varchar(20);
=====================================================================17/05/2016================================================================
LTER TABLE `guest_faculty`
CHANGE `recruitment_location_id` `recruitment_location_id` int(11) NULL AFTER `uploaded_cv_file_name`,
COMMENT=''; -- 0.345 s
=========================================================================17/05/2016===================================================
ALTER TABLE `semester_milestone_plan_master`
ADD `program_code1` varchar(225) NOT NULL AFTER `id`,
COMMENT='';
===============================================================================18/05/2016===================================
ALTER TABLE `coordinator`
ADD INDEX `key` (`coordinator_id`),
DROP INDEX `key`;

alter table `coordinator` add unique key `key` (`coordinator_id`);
alter table `coordinator` drop primary key;


ALTER TABLE `coordinator`
ADD `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST,
COMMENT=''; -- 0.394 s
========================================================================================================23/05/2016===========================

ALTER TABLE `guest_faculty_course_offer`
CHANGE `number_students_in_class` `number_students_in_class` int(11) NULL AFTER `offer_to_faculty_date`,
COMMENT='';


============================================================================================================03/06/2016=================================

CREATE TABLE `faculty_bucket_master` (
  `bucket_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `bucket_name` varchar(55) NOT NULL,
  `active_bucket_flag` tinyint(1) NOT NULL,
  `lower_tech_interval_gap` int(11) NOT NULL,
  `upper_tech_interval_gap` int(11) NOT NULL,
  `inactive_faculty_flag` tinyint(1) NOT NULL,
  `current_faculty_flag` tinyint(1) NOT NULL,
  `lower_bound_year` int(11) NOT NULL,
  `lower_bound_sem_nbr` int(11) NOT NULL,
  `upper_bound_year` int(11) NOT NULL,
  `upper_bound_sem_nbr` int(11) NOT NULL,
  `created_on` datetime NOT NULL,
  `created_by` varchar(40) NOT NULL,
  `updated_on` datetime NOT NULL,
  `updated_by` varchar(40) NOT NULL
) COMMENT=''; -- 0.125 s



ALTER TABLE `faculty_bucket_master`
CHANGE `created_by` `created_by` varchar(40) COLLATE 'latin1_swedish_ci' NULL AFTER `created_on`,
CHANGE `updated_by` `updated_by` varchar(40) COLLATE 'latin1_swedish_ci' NULL AFTER `updated_on`,
COMMENT='';


ALTER TABLE `faculty_bucket_master`
CHANGE `lower_tech_interval_gap` `lower_tech_interval_gap` int(11) NULL AFTER `active_bucket_flag`,
CHANGE `upper_tech_interval_gap` `upper_tech_interval_gap` int(11) NULL AFTER `lower_tech_interval_gap`,
CHANGE `lower_bound_year` `lower_bound_year` int(11) NULL AFTER `current_faculty_flag`,
CHANGE `lower_bound_sem_nbr` `lower_bound_sem_nbr` int(11) NULL AFTER `lower_bound_year`,
CHANGE `upper_bound_year` `upper_bound_year` int(11) NULL AFTER `lower_bound_sem_nbr`,
CHANGE `upper_bound_sem_nbr` `upper_bound_sem_nbr` int(11) NULL AFTER `upper_bound_year`,
COMMENT='';



ALTER TABLE `guest_faculty_bucket`
ADD FOREIGN KEY (`faculty_bucket_id`) REFERENCES `faculty_bucket_master` (`bucket_id`); 

ALTER TABLE `guest_faculty_bucket`
ADD FOREIGN KEY (`guest_faculty_id`) REFERENCES `guest_faculty` (`id`); -- 0.210 s

ALTER TABLE `guest_faculty_bucket`
DROP FOREIGN KEY `guest_faculty_bucket_ibfk_2`,
ADD FOREIGN KEY (`guest_faculty_id`) REFERENCES `guest_faculty` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION; 

ALTER TABLE `guest_faculty_bucket`
DROP FOREIGN KEY `guest_faculty_bucket_ibfk_1`,
ADD FOREIGN KEY (`faculty_bucket_id`) REFERENCES `faculty_bucket_master` (`bucket_id`) ON DELETE NO ACTION ON UPDATE NO ACTION; -- 0.205 s


ALTER TABLE `guest_faculty_bucket`
ADD `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST,
COMMENT=''; -- 0.208 s


ALTER TABLE `guest_faculty_bucket`
ADD FOREIGN KEY (`faculty_bucket_id`) REFERENCES `faculty_bucket_master` (`bucket_id`);
ALTER TABLE `guest_faculty_bucket`
ADD FOREIGN KEY (`guest_faculty_id`) REFERENCES `guest_faculty` (`id`);


===========================================================================
CREATE TABLE `guest_faculty_bucket` (
  `faculty_bucket_id` int(11) NOT NULL,
  `guest_faculty_id` int(11) NOT NULL,
  `bucket_assigned_on` datetime NOT NULL
) COMMENT=''; -- 0.115 s



===================================================================================
CREATE TABLE `current_gf_teaching_semester` (
  `current_semester_id` int(11) NOT NULL
) COMMENT=''; -- 0.098 s

ALTER TABLE `current_gf_teaching_semester`
ADD FOREIGN KEY (`current_semester_id`) REFERENCES `semester` (`semester_id`); -- 0.236 s


ALTER TABLE `current_gf_teaching_semester`
DROP FOREIGN KEY `current_gf_teaching_semester_ibfk_1`,
ADD FOREIGN KEY (`current_semester_id`) REFERENCES `semester` (`semester_id`) ON DELETE NO ACTION ON UPDATE NO ACTION; -- 0.208 s



===========================================================================8/06/2016=================================
ALTER TABLE `guest_faculty`
ADD `inactive_flag` tinyint(1) NULL,
COMMENT=''; -- 0.368 s



ALTER TABLE `faculty_bucket_master`
CHANGE `inactive_faculty_flag` `inactive_faculty_flag` tinyint(1) NULL AFTER `upper_tech_interval_gap`,
CHANGE `current_faculty_flag` `current_faculty_flag` tinyint(1) NULL AFTER `inactive_faculty_flag`,
COMMENT=''; -- 0.254 s



ALTER TABLE `guest_faculty_bucket`
CHANGE `faculty_bucket_id` `faculty_bucket_id` int(11) NULL AFTER `id`,
CHANGE `guest_faculty_id` `guest_faculty_id` int(11) NULL AFTER `faculty_bucket_id`,
CHANGE `bucket_assigned_on` `bucket_assigned_on` datetime NULL AFTER `guest_faculty_id`,
COMMENT='';











==================================================16/06/2016=================================================


CREATE TABLE `assessment_question` (
  `question_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `question_description` varchar(80) NOT NULL
) COMMENT=''; -- 0.110 s


+++++++++++++++++++++++++++++++++++++++++++++++++++


CREATE TABLE `gf_assessment_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `guest_faculty_id` varchar(40) NULL,
  `assessment_identifier` varchar(40) NULL,
  `question_id` int(11) NULL,
  `assessment_score` decimal(10,2) NULL,
  `key_observations` varchar(225) NOT NULL,
  `recommendations` varchar(225) NOT NULL,
  `created_on` datetime NOT NULL,
  `last_updated_on` datetime NOT NULL,
  `last_updated_by` varchar(50) NULL
) COMMENT=''; -- 0.090 s



ALTER TABLE `gf_assessment_details`
CHANGE `assessment_identifier` `assessment_identifier_id` varchar(40) COLLATE 'latin1_swedish_ci' NULL AFTER `guest_faculty_id`,
COMMENT='';

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



CREATE TABLE `gf_assessment_summary` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `guest_faculty_id` varchar(40) NULL,
  `assessment_identifier` varchar(40) NULL,
  `assessment_date` datetime NULL,
  `assessment_location_id` int(11) NULL,
  `overall_score` decimal(10,2) NOT NULL,
  `normalized_score` decimal(10,2) NOT NULL,
  `gf_strength` varchar(225) NOT NULL,
  `gf_weaknesses` varchar(225) NOT NULL,
  `recommendations_comments` varchar(225) NULL,
  `assessor1_name` varchar(100) NULL,
  `assessor2_name` varchar(100) NULL,
  `assessor3_name` varchar(100) NULL,
  `sme1_name` varchar(100) NULL,
  `sme2_name` varchar(100) NULL,
  `coordinator_id` varchar(40) NULL,
  `created_on` datetime NOT NULL,
  `last_updated_on` datetime NOT NULL,
  `last_updated_by` varchar(50) NULL
) COMMENT=''; -- 0.099 s


ALTER TABLE `gf_assessment_summary`
CHANGE `overall_score` `overall_score` decimal(10,2) NULL AFTER `assessment_location_id`,
CHANGE `normalized_score` `normalized_score` decimal(10,2) NULL AFTER `overall_score`,
CHANGE `gf_strength` `gf_strength` varchar(225) COLLATE 'latin1_swedish_ci' NULL AFTER `normalized_score`,
CHANGE `gf_weaknesses` `gf_weaknesses` varchar(225) COLLATE 'latin1_swedish_ci' NULL AFTER `gf_strength`,
COMMENT='';


++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

ALTER TABLE `gf_assessment_summary`
CHANGE `coordinator_id` `coordinator_id` int(11) NOT NULL AFTER `sme2_name`,
COMMENT='';


ALTER TABLE `gf_assessment_summary`
CHANGE `coordinator_id` `coordinator_id` int(11) NULL AFTER `sme2_name`,
COMMENT='';

ALTER TABLE `gf_assessment_summary`
ADD FOREIGN KEY (`coordinator_owner_id`) REFERENCES `coordinator` (`coordinator_id`);







ALTER TABLE `gf_assessment_summary`
CHANGE `coordinator_id` `coordinator_owner_id` int(11) NULL AFTER `sme2_name`,
COMMENT='';

ALTER TABLE `gf_assessment_summary`
DROP FOREIGN KEY `gf_assessment_summary_ibfk_1`;











ALTER TABLE `gf_assessment_summary`
CHANGE `guest_faculty_id` `guest_faculty_id` varchar(40) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `id`,
CHANGE `assessment_identifier` `assessment_identifier` varchar(40) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `guest_faculty_id`,
CHANGE `assessment_date` `assessment_date` datetime NOT NULL AFTER `assessment_identifier`,
CHANGE `overall_score` `overall_score` decimal(10,2) NOT NULL AFTER `assessment_location_id`,
COMMENT='';












ALTER TABLE `gf_assessment_summary`
CHANGE `assessment_date` `assessment_date` datetime  NULL AFTER `assessment_identifier`,






ALTER TABLE `gf_assessment_summary`
CHANGE `created_on` `created_on` datetime NULL AFTER `coordinator_id`,
CHANGE `last_updated_on` `last_updated_on` datetime NULL AFTER `created_on`,
COMMENT='';



ALTER TABLE `gf_assessment_summary`
ADD FOREIGN KEY (`coordinator_id`) REFERENCES `coordinator` (`coordinator_id`);




ALTER TABLE `gf_assessment_summary`
ADD FOREIGN KEY (`assessment_location_id`) REFERENCES `location` (`location_id`); -- 0.242 s




ALTER TABLE `gf_assessment_summary`
CHANGE `coordinator_owner_id` `coordinator_owner_id` int(11) NOT NULL AFTER `sme2_name`,
COMMENT='';







select CONSTRAINT_NAME,COLUMN_NAME from INFORMATION_SCHEMA.KEY_COLUMN_USAGE where TABLE_NAME = 'gf_assessment_summary';







ALTER TABLE `gf_assessment_summary`
DROP FOREIGN KEY `gf_assessment_summary_ibfk_1`; -- 0.232 s

ALTER TABLE `gf_assessment_summary`
CHANGE `coordinator_owner_id` `coordinator_id` int(11) NOT NULL AFTER `sme2_name`,
COMMENT='';










ALTER TABLE `gf_assessment_summary`
CHANGE `coordinator_id` `coordinator_id` int(11) NULL AFTER `sme2_name`,
COMMENT=''; -- 0.260 s




=================================================================23/06/2016=======================================






ALTER TABLE `gf_assessment_summary`
ADD UNIQUE `guest_faculty_id_assessment_identifier` (`guest_faculty_id`, `assessment_identifier`); -- 0.186 s















===================================24/06/2016==================================================================
python manage.py collectstatic --noinput --clear





==================================================29/06/16================================================
CREATE TABLE `honorarium_category_value_master` (
  `value_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `category_value` varchar(70) NOT NULL
) COMMENT=''; -- 0.181 s


=====================
CREATE TABLE `honorarium_category_master` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `category_name` varchar(75) NOT NULL
) COMMENT=''; -- 0.093 s

====================
CREATE TABLE `honorarium_rate_master` (
  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `category_id` int(11) NULL,
  `active_flag` tinyint(1) NOT NULL,
  `category1_value_id` int(11) NULL,
  `category2_value_id` int(11) NULL,
  `honorarium_rate` decimal(10,2) NULL,
  `honorarium_amount` decimal(10,2) NULL,
  `created_on` datetime NULL,
  `last_updated_on` datetime NULL,
  `last_updated_by` varchar(60) NULL
) COMMENT=''; -- 0.113 s

=============================
CREATE TABLE `honorarium__field_key_words` (
  `key_value` varchar(50) NULL,
  `field_name` varchar(50) NULL
) COMMENT=''; -- 0.127 s
=================================

================================================

CREATE TABLE `additional_course_offer_attributes` (
  `course_id` varchar(11) NULL,
  `semester_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `guest_faculty_id` varchar(11) NOT NULL,
  `course_type` varchar(30) NOT NULL,
  `mid_sem_weightage` decimal(2,2) NOT NULL,
  `compre_weightage` decimal(2,2) NOT NULL,
  `assignment_weightage` decimal(2,2) NOT NULL,
  `number_of_students` int(11) NOT NULL,
  `number_of_lectures` int(11) NOT NULL,
  `faculty_role` varchar(30) NOT NULL,
  `mid_sem_evaluated_flag` tinyint(1) NULL,
  `assignment_evaluated_flag` tinyint(1) NULL,
  `compre_evaluated_flag` tinyint(1) NULL,
  `qp_work_done` varchar(30) NOT NULL,
  `course_location_section_detail` varchar(60) NOT NULL,
  `mid_sem_exam_students_count` int(11) NOT NULL,
  `dissertation_role` varchar(60) NOT NULL,
  `dissertation_students_count` int(11) NOT NULL,
  `assignment_student_count` int(11) NOT NULL,
  `compre_exams_students_count` int(11) NOT NULL,
  `honorarium_calculated_flag` tinyint(1) NULL,
  `last_updated_on_datetime` datetime NULL,
  `created_on_datetime` datetime NULL,
  `last_updated_by` varchar(60) NULL
) COMMENT=''; -- 0.111 s




=====================================
ALTER TABLE `additional_course_offer_attributes`
ADD `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST,
COMMENT=''; -- 0.207 s

========================================
CREATE TABLE `guest_faculty_honorarium` (
  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `course_id` varchar(10) NOT NULL,
  `semester_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `guest_faculty_id` varchar(10) NOT NULL,
  `lecture_rate_used` decimal(10,2) NOT NULL,
  `lecture_honorarium` decimal(10,2) NOT NULL,
  `mid_sem_qp_rate_used` decimal(10,2) NOT NULL,
  `compre_qp_rate_used` decimal(10,2) NOT NULL,
  `qp_honorarium` varchar(60) NOT NULL,
  `mid_sem_eval_rate_used` decimal(10,2) NOT NULL,
  `compre_eval_rate_used` decimal(10,2) NOT NULL,
  `assignment_eval_rate_used` decimal(10,2) NOT NULL,
  `evaluation_honorarium` decimal(10,2) NOT NULL,
  `dissertation_rate_used` decimal(10,2) NOT NULL,
  `dissertation_honorarium` decimal(10,2) NOT NULL,
  `course_type_section_location_honorarium` decimal(10,2) NOT NULL,
  `manualy_calculated_flag` tinyint(1) NOT NULL,
  `course_type_rate_used` decimal(10,2) NOT NULL,
  `total_honorarium` decimal(10,2) NOT NULL,
  `created_on_datetime` datetime NOT NULL,
  `last_updated_datetime` datetime NOT NULL,
  `last_updated_by` varchar(60) NOT NULL,
  `additional_teaching_honorarium` decimal(10,2) NOT NULL
) COMMENT=''; -- 0.124 s


===============================30/06/16=======================
ALTER TABLE `additional_course_offer_attributes`
CHANGE `mid_sem_evaluated_flag` `mid_sem_evaluated_flag` tinyint(1) NOT NULL AFTER `faculty_role`,
CHANGE `assignment_evaluated_flag` `assignment_evaluated_flag` tinyint(1) NOT NULL AFTER `mid_sem_evaluated_flag`,
CHANGE `compre_evaluated_flag` `compre_evaluated_flag` tinyint(1) NOT NULL AFTER `assignment_evaluated_flag`,
CHANGE `honorarium_calculated_flag` `honorarium_calculated_flag` tinyint(1) NOT NULL AFTER `compre_exams_students_count`,
COMMENT=''; -- 0.281 s
================================================
ALTER TABLE `additional_course_offer_attributes`
CHANGE `mid_sem_weightage` `mid_sem_weightage` decimal(10,2) NOT NULL AFTER `course_type`,
CHANGE `compre_weightage` `compre_weightage` decimal(10,2) NOT NULL AFTER `mid_sem_weightage`,
CHANGE `assignment_weightage` `assignment_weightage` decimal(10,2) NOT NULL AFTER `compre_weightage`,
COMMENT=''; -- 0.236 s
============================================================1/06/16==================================
ALTER TABLE `additional_course_offer_attributes`
CHANGE `course_id` `course_id` varchar(11) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `id`,
COMMENT=''; -- 0.254 s
============================================
ALTER TABLE `honorarium_rate_master`
CHANGE `category_id` `category_id` int(11) NOT NULL AFTER `id`,
CHANGE `category1_value_id` `category1_value_id` int(11) NOT NULL AFTER `active_flag`,
CHANGE `category2_value_id` `category2_value_id` int(11) NOT NULL AFTER `category1_value_id`,
COMMENT=''; -- 0.247 s
================================================
ALTER TABLE `honorarium__field_key_words`
ADD `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST,
ALTER TABLE `honorarium__field_key_words`
CHANGE `key_value` `key_value` varchar(50) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `id`,
CHANGE `field_name` `field_name` varchar(50) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `key_value`,
COMMENT=''; -- 0.196 s
COMMENT=''; -- 0.213 s

=================================================5/06/16===========================================
ALTER TABLE `additional_course_offer_attributes`
ADD FOREIGN KEY (`semester_id`) REFERENCES `semester` (`semester_id`); -- 0.250 s

ALTER TABLE `additional_course_offer_attributes`
ADD FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`); -- 0.255 s

ALTER TABLE `additional_course_offer_attributes`
ADD FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`); -- 0.235 s


========================================================================================================================new changes==================================
ALTER TABLE `guest_faculty`
CHANGE `inactive_flag` `inactive_flag` tinyint(1) NULL DEFAULT '0' AFTER `past_organizations`,
COMMENT=''; -- 0.268 s

ALTER TABLE `guest_faculty`
CHANGE `inactive_flag` `inactive_flag` tinyint(1) NULL DEFAULT '0' AFTER `past_organizations`,
COMMENT=''; -- 0.245 s


ALTER TABLE `guest_faculty`
CHANGE `inactive_flag` `inactive_flag` tinyint(1) NOT NULL DEFAULT '0' AFTER `past_organizations`,
COMMENT='';






UPDATE `faculty_bucket_master` SET
`bucket_id` = '-1',
`bucket_name` = 'No Buckets Assigned	',
`active_bucket_flag` = '1',
`lower_tech_interval_gap` = '0',
`upper_tech_interval_gap` = '0',
`inactive_faculty_flag` = '0',
`current_faculty_flag` = '0',
`lower_bound_year` = '0',
`lower_bound_sem_nbr` = '0',
`upper_bound_year` = '0',
`upper_bound_sem_nbr` = '0',
`created_on` = '2016-06-16 12:45:27',
`created_by` = NULL,
`updated_on` = '2016-06-16 10:38:35',
`updated_by` = '1'
WHERE `bucket_id` = '6'; -- 0.044 s















ALTER TABLE `guest_faculty_bucket`
CHANGE `faculty_bucket_id` `faculty_bucket_id` int(11) NULL AFTER `id`,
COMMENT='';


ALTER TABLE `guest_faculty_bucket`
ADD FOREIGN KEY (`faculty_bucket_id`) REFERENCES `faculty_bucket_master` (`bucket_id`); -- 0.201 s

======================================07/07/16===================
CREATE TABLE `student` (
  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(225) NULL,
  `mobile` int(11) NULL
) COMMENT='' ENGINE='InnoDB'; -- 0.116 s
===============================================
ALTER TABLE `student`
CHANGE `mobile` `mobile` varchar(12) NOT NULL AFTER `name`,
COMMENT=''; -- 0.213 s
=============================
ALTER TABLE `student`
CHANGE `joining_date` `joining_date` datetime NULL AFTER `address`,
COMMENT=''; -- 0.247 s
======================
ALTER TABLE `student_info`
RENAME TO `studentinfo`,
COMMENT=''; -- 0.121 s
================================
CREATE TABLE `facultyname` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `computers` varchar(225) NOT NULL,
  `mathematics` varchar(225) NOT NULL,
  `electronics` varchar(225) NOT NULL,
  `address` varchar(225) NOT NULL,
  `phno` int(11) NOT NULL,
  `email` varchar(225) NOT NULL
) COMMENT='' ENGINE='InnoDB'; -- 0.077 s

=========================================08/07/2016=======================

CREATE TABLE `employee_details` (
  `emp_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `emp_name` varchar(225) NOT NULL,
  `mobile` int(11) NOT NULL,
  `email` varchar(225) NOT NULL,
  `emp_city` varchar(225) NOT NULL,
  `emp_state` varchar(225) NOT NULL,
  `pincode` int(11) NOT NULL
) COMMENT='' ENGINE='InnoDB'; -- 0.110 s


ALTER TABLE `employee_details`
CHANGE `mobile` `mobile` varchar(225) NOT NULL AFTER `emp_name`,
COMMENT=''; -- 0.212 s

ALTER TABLE `employee_details`
ADD `semester_id` int(11) NOT NULL AFTER `emp_name`,
COMMENT=''; -- 0.242 s

==========================11/6/06======================

CREATE TABLE `gfnewtable` (
  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(225) NOT NULL,
  `email` varchar(225) NOT NULL,
  `mobile` varchar(225) NOT NULL
) COMMENT='' ENGINE='InnoDB'; -- 0.252 s


CREATE TABLE `gfplanexample` (
  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(225) NOT NULL,
  `mobilenum` varchar(225) NOT NULL,
  `email` varchar(225) NOT NULL,
  `location` varchar(225) NOT NULL,
  `designation` varchar(225) NOT NULL
) COMMENT='' ENGINE='InnoDB'; -- 0.100 s


CREATE TABLE `gfdesignation` (
  `dept_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(225) NOT NULL,
  `company_name` varchar(225) NOT NULL,
  `role` varchar(225) NOT NULL
) COMMENT='' ENGINE='InnoDB'; -- 0.095 s



==================================================================================

*********************Assessment_master 12/07/2016**********************************
CREATE TABLE `assessment_master` (
  `assessment_id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `assessment_identifier` varchar(225) NOT NULL
) COMMENT=''; -- 0.089 s
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
===========================12/07/06========

CREATE TABLE `Design_resource` (
  `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` varchar(225) NOT NULL,
  `description` varchar(225) NOT NULL
) COMMENT='' ENGINE='InnoDB'; -- 0.116 s

ALTER TABLE `Design_resource`
RENAME TO `design_resource`,
COMMENT=''; -- 0.116 s

ALTER TABLE `design_resource`
DROP `description`,
COMMENT=''; -- 0.232 s


==========================================================13/07/16===================

ALTER TABLE `honorarium_rate_master`
ADD FOREIGN KEY (`category1_value_id`) REFERENCES `honorarium_category_value_master` (`value_id`); -- 0.254 s

ALTER TABLE `honorarium_rate_master`
ADD FOREIGN KEY (`category2_value_id`) REFERENCES `honorarium_category_value_master` (`value_id`); -- 0.240 s

======================================================
ALTER TABLE `guest_faculty_honorarium`
ADD FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;(cannot create gfaculty.#sql-2296_f343) err no 150 in production)


ALTER TABLE `guest_faculty_honorarium`
ADD FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`); -- 0.239 s(still pending) (can't create gfaculty.#sql-2296_f343) err no 150 in production)

ALTER TABLE `guest_faculty_honorarium`
DROP FOREIGN KEY `guest_faculty_honorarium_ibfk_5`;

ALTER TABLE `guest_faculty_honorarium`
ADD FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`); -- 0.282 s(error 150)


ALTER TABLE `guest_faculty_honorarium`
DROP FOREIGN KEY `guest_faculty_honorarium_ibfk_1`,
ADD FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE RESTRICT ON UPDATE RESTRICT; -- 0.255 s(error 150)

ALTER TABLE `guest_faculty_honorarium`
ADD FOREIGN KEY (`semester_id`) REFERENCES `semester` (`semester_id`); -- 0.250 s

ALTER TABLE `guest_faculty_honorarium`
ADD FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`); -- 0.242 s

ALTER TABLE `guest_faculty_honorarium`
CHANGE `guest_faculty_id` `guest_faculty_id` int(11) NOT NULL AFTER `program_id`,
COMMENT=''; -- 0.240 s

ALTER TABLE `guest_faculty_honorarium`
ADD FOREIGN KEY (`guest_faculty_id`) REFERENCES `guest_faculty` (`id`); -- 0.245 s

============================================================
ALTER TABLE `additional_course_offer_attributes`
CHANGE `guest_faculty_id` `guest_faculty_id` int NOT NULL AFTER `program_id`,
COMMENT=''; -- 0.295 s

ALTER TABLE `additional_course_offer_attributes`
ADD FOREIGN KEY (`guest_faculty_id`) REFERENCES `guest_faculty` (`id`); -- 0.271 s

==================================15/07/2016==========   ****** remaining  in UAT  *******

ALTER TABLE `honorarium__field_key_words`
RENAME TO `honorarium_field_key_words`,
COMMENT=''; -- 0.100 s


ALTER TABLE `honorarium_field_key_words`
CHANGE `key_value` `key_value_id` varchar(50) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `id`,
COMMENT=''; -- 0.660 s


ALTER TABLE `honorarium__field_key_words`
CHANGE `field_name` `field_name_id` varchar(50) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `key_value_id`,(doesnot exist)
COMMENT=''; -- 0.247 s

ALTER TABLE `honorarium__field_key_words`
CHANGE `key_value` `key_value_id` varchar(50) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `key_value_id`,
COMMENT=''; -- 0.247 s


===========================================================18/07/16==============================
ALTER TABLE `additional_course_offer_attributes`
CHANGE `program_id` `program_id` int(11) NULL AFTER `semester_id`,
CHANGE `mid_sem_exam_students_count` `mid_sem_exam_students_count` int(11) NULL AFTER `course_location_section_detail`,
CHANGE `assignment_student_count` `assignment_student_count` int(11) NULL AFTER `dissertation_students_count`,
CHANGE `compre_exams_students_count` `compre_exams_students_count` int(11) NULL AFTER `assignment_student_count`,
COMMENT=''; -- 0.391 s

===================================================================19/07/16========================
ALTER TABLE `additional_course_offer_attributes`
CHANGE `faculty_role` `faculty_role_id` int(11) NOT NULL AFTER `number_of_lectures`,
CHANGE `qp_work_done` `qp_work_done_id` int(11) NOT NULL AFTER `compre_evaluated_flag`,
CHANGE `dissertation_role` `dissertation_role_id` int(11) NOT NULL AFTER `mid_sem_exam_students_count`,
COMMENT=''; -- 0.229 s
========================================================22/07/16========================
ALTER TABLE `additional_course_offer_attributes`
ADD FOREIGN KEY (`faculty_role_id`) REFERENCES `honorarium_category_value_master` (`value_id`); -- 0.243 s

ALTER TABLE `additional_course_offer_attributes`
ADD FOREIGN KEY (`qp_work_done_id`) REFERENCES `honorarium_category_value_master` (`value_id`); -- 0.258 s

ALTER TABLE `additional_course_offer_attributes`
ADD FOREIGN KEY (`dissertation_role_id`) REFERENCES `honorarium_category_value_master` (`value_id`); -- 0.211 s

===========================================16-08-2016==================================
ALTER TABLE `additional_course_offer_attributes`
CHANGE `mid_sem_exam_students_count` `mid_sem_exam_students_count` int(11) NULL DEFAULT '0' AFTER `course_location_section_detail`,
CHANGE `dissertation_students_count` `dissertation_students_count` int(11) NOT NULL DEFAULT '0' AFTER `dissertation_role_id`,
CHANGE `assignment_student_count` `assignment_student_count` int(11) NULL DEFAULT '0' AFTER `dissertation_students_count`,
CHANGE `compre_exams_students_count` `compre_exams_students_count` int(11) NULL DEFAULT '0' AFTER `assignment_student_count`,
COMMENT=''; -- 0.520 s
========================================
ALTER TABLE `additional_course_offer_attributes`
CHANGE `mid_sem_exam_students_count` `mid_sem_exam_students_count` int(11) NOT NULL DEFAULT '0' AFTER `course_location_section_detail`,
CHANGE `assignment_student_count` `assignment_student_count` int(11) NOT NULL DEFAULT '0' AFTER `dissertation_students_count`,
CHANGE `compre_exams_students_count` `compre_exams_students_count` int(11) NOT NULL DEFAULT '0' AFTER `assignment_student_count`,
COMMENT=''; -- 0.277 s
=======================
ALTER TABLE `additional_course_offer_attributes`
CHANGE `mid_sem_exam_students_count` `mid_sem_exam_students_count` int(11) NULL DEFAULT '0' AFTER `course_location_section_detail`,
CHANGE `assignment_student_count` `assignment_student_count` int(11) NULL DEFAULT '0' AFTER `dissertation_students_count`,
CHANGE `compre_exams_students_count` `compre_exams_students_count` int(11) NULL DEFAULT '0' AFTER `assignment_student_count`,
COMMENT=''; -- 0.290 s
=================================
ALTER TABLE `additional_course_offer_attributes`
CHANGE `mid_sem_exam_students_count` `mid_sem_exam_students_count` int(11) NULL DEFAULT '0' AFTER `course_location_section_detail`,
CHANGE `assignment_student_count` `assignment_student_count` int(11) NULL DEFAULT '0' AFTER `dissertation_students_count`,
CHANGE `compre_exams_students_count` `compre_exams_students_count` int(11) NULL DEFAULT '0' AFTER `assignment_student_count`,
COMMENT=''; -- 0.282 s
================================================

23-08-2016(aug 08)

ALTER TABLE `guest_faculty`
CHANGE `inactive_flag` `inactive_flag` tinyint(1) NULL DEFAULT '0' AFTER `past_organizations`
=================

24-08-2016

ALTER TABLE `gf_assessment_details`
CHANGE `guest_faculty_id` `guest_faculty_id` varchar(20) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `id`,
COMMENT=''; -- 0.369 s
=====================================25/08/16================

=====================================02-09-2016

create or replace view gfdegreediscipline as
SELECT gf.id,gf.guest_faculty_id,gf.name,l.location_name,gfd.areas_of_expertise,q.qualification_name,
gfd.courses_can_handle,degree_full_name,discipline_long_name,q.qualification_id,d.degree_id,
gfq.qualification_discipline_id,gf.current_location_id

from guest_faculty gf
left join guest_faculty_qualification gfq on gf.id = gfq.guest_faculty_id
left join location l on gf.current_location_id = l.location_id
left join qualification q on gfq.qualification_id = q.qualification_id
left join gf_interested_in_discipline gfd on gf.id = gfd.guest_faculty_id 
left join degree d on gfq.degree_id = d.degree_id
left join discipline dis on gfq.qualification_discipline_id = dis.discipline_id;
================================================================================
06-09-2016===========================


create or replace view gfdegreediscipline as

SELECT  gf.id,gf.guest_faculty_id,gf.name,l.location_name,gfd.areas_of_expertise,q.qualification_name,
gfd.courses_can_handle,degree_full_name,discipline_long_name,q.qualification_id,d.degree_id,
gfq.qualification_discipline_id,gf.current_location_id

from guest_faculty gf

left join guest_faculty_qualification gfq on gf.id = gfq.guest_faculty_id
left join location l on gf.current_location_id = l.location_id
left join qualification q on gfq.qualification_id = q.qualification_id
left join gf_interested_in_discipline gfd on gf.id = gfd.guest_faculty_id
left join degree d on gfq.degree_id = d.degree_id
left join discipline dis on gfd.discipline_id= dis.discipline_id 
group by gf.id,discipline_long_name
 ;
=============================================================22/09/2016==========================
ALTER TABLE `guest_faculty_candidate`
CHANGE `uploaded_cv_file_name` `uploaded_cv_file_name` varchar(200) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `applying_for_discipline_id`,
CHANGE `nature_of_current_job_id` `nature_of_current_job_id` int(11) NOT NULL AFTER `industry_exp_in_months`,
CHANGE `areas_of_expertise` `areas_of_expertise` varchar(2000) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `nature_of_current_job_id`,
CHANGE `certifications` `certifications` varchar(1000) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `areas_of_expertise`,
CHANGE `awards_and_distinctions` `awards_and_distinctions` varchar(1000) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `certifications`,
CHANGE `publications` `publications` varchar(2000) COLLATE 'latin1_swedish_ci' NOT NULL AFTER `awards_and_distinctions`,
COMMENT=''; -- 0.678 s

================================================
ALTER TABLE `candidate_evaluation`
ADD `interview_venue_conformed` tinyint(1) NULL AFTER `selected_letter_sent`,
COMMENT=''; -- 0.352 s
================================================
create or replace view gfinterview as
SELECT distinct gfc.application_id,gfc.name,gfc.current_location_id,
ce.evaluation_venue,ce.evaluation_time_slot,ce.evaluator_names_list,ce.interview_venue_conformed,
ce.evaluation_result,ce.assessment_score,l.location_id,l.location_name

from guest_faculty_candidate gfc 
left join candidate_evaluation ce on gfc.application_id = ce.application_id
left join location l on gfc.current_location_id = l.location_id;
================================================================================
create or replace view gfinterview as
SELECT distinct gfc.application_id,gfc.application_number,gfc.name,gfc.current_location_id,
ce.evaluation_venue,ce.evaluation_time_slot,ce.evaluator_names_list,ce.interview_venue_conformed,
ce.evaluation_result,ce.assessment_score,l.location_id,l.location_name, ce.evaluation_type

from guest_faculty_candidate gfc 
left join candidate_evaluation ce on gfc.application_id = ce.application_id
left join location l on gfc.current_location_id = l.location_id
where ce.evaluation_type ='interview' ;

===============================17/11/16
ALTER TABLE `guest_faculty`
CHANGE `updated_by` `updated_by` varchar(200) NULL AFTER `inserted_date`,
COMMENT=''; -- 0.564 s
=======================================
ALTER TABLE `guest_faculty`
ADD `active_flag` tinyint(1) NULL,
COMMENT=''; -- 0.418 s


-----------------------------
5-12-2016

ALTER TABLE `candidate_evaluation`
CHANGE `evaluation_date` `evaluation_date` date NULL AFTER `evaluation comments`,
COMMENT=''; -- 0.362 s
-----------------














