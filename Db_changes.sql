SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `batch`;
CREATE TABLE `batch` (
  `batch_id` int(11) NOT NULL AUTO_INCREMENT,
  `batch_name` varchar(45) NOT NULL,
  `admission_year` year(4) NOT NULL,
  `expected_grad_year` year(4) NOT NULL,
  `duration` int(11) NOT NULL,
  `total_admission_strength` int(11) NOT NULL,
  `admittted_semester_id` int(11) NOT NULL,
  PRIMARY KEY (`batch_id`),
  KEY `fk_batch_semester2_idx` (`admittted_semester_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `organization`
--

DROP TABLE IF EXISTS `organization`;
CREATE TABLE `organization` (
  `organization_id` int(11) NOT NULL AUTO_INCREMENT,
  `organization_name` varchar(100) NOT NULL,
  `organization_long_name` varchar(200) NOT NULL,
  `association_duration_in_months` int(11) NOT NULL,
  `start_year` int(11) NOT NULL,
  PRIMARY KEY (`organization_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `semester_milestone`
--

DROP TABLE IF EXISTS `semester_milestone`;
CREATE TABLE `semester_milestone` (
  `milestone_id` int(11) NOT NULL AUTO_INCREMENT,
  `milestone_short_name` varchar(45) NOT NULL,
  `milestone_long_name` varchar(200) NOT NULL,
  `milestone_type` varchar(45) NOT NULL,
  `is_duration_milestone` tinyint(1) NOT NULL,
  `is_editable_by_owner` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `max_duration_in_days` int(11) NOT NULL,
  PRIMARY KEY (`milestone_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `semester_milestone_plan_detail`
--

DROP TABLE IF EXISTS `semester_milestone_plan_detail`;
CREATE TABLE `semester_milestone_plan_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `semester_milestone_plan_master_id` int(11) NOT NULL,
  `version_number` int(11) NOT NULL,
  `semester_milestone_id` int(11) NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `event_date` datetime NOT NULL,
  `date_editable` tinyint(1) NOT NULL,
  `system_populated_date` tinyint(1) NOT NULL,
  `created_by` varchar(45) NOT NULL,
  `created_date` datetime NOT NULL,
  `milestone_comments` varchar(45) NOT NULL,
  `last_updated_by` varchar(45) NOT NULL,
  `last_updated_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `semester_milestone_id` (`semester_milestone_id`),
  KEY `semester_milestone_plan_master_id` (`semester_milestone_plan_master_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `semester_milestone_plan_master`
--

DROP TABLE IF EXISTS `semester_milestone_plan_master`;
CREATE TABLE `semester_milestone_plan_master` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `version_number` int(11) NOT NULL,
  `semester_plan_name` varchar(45) NOT NULL,
  `created_date` datetime NOT NULL,
  `last_updated_date` datetime NOT NULL,
  `last_update_by` varchar(100) NOT NULL,
  `timetable_status` varchar(45) NOT NULL,
  `current_version_flag` tinyint(1) NOT NULL,
  `timetable_comments` varchar(200) NOT NULL,
  `location_id` int(11) NOT NULL,
  `degree_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `semester_id` int(11) NOT NULL,
  `batch_id` int(11) NOT NULL,
  `client_organization_id` int(11) NOT NULL,
  `discipline_id` int(11) NOT NULL,
  `milestone_plan_owner_id` int(11) NOT NULL,
  `alternate_owner_id` int(11) NOT NULL,
  `mode_of_delivery` varchar(100) NOT NULL,
  `registration_completed_in_wilp` tinyint(1) NOT NULL,
  `student_strength` int(11) NOT NULL,
  `approved_rejected_date` datetime NOT NULL,
  `approved_rejected_by` varchar(100) NOT NULL,
  `approval_rejection_comments` varchar(200) NOT NULL,
  `escalated_on_date` datetime NOT NULL,
  `escalated_by` varchar(200) NOT NULL,
  `escalation_comments` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `location_id` (`location_id`),
  KEY `degree_id` (`degree_id`),
  KEY `program_id` (`program_id`),
  KEY `semester_id` (`semester_id`),
  KEY `batch_id` (`batch_id`),
  KEY `discipline_id` (`discipline_id`),
  KEY `client_organization_id` (`client_organization_id`),
  KEY `milestone_plan_owner_id` (`milestone_plan_owner_id`),
  KEY `alternate_owner_id` (`alternate_owner_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `semester_timetable_edit_window`
--

DROP TABLE IF EXISTS `semester_timetable_edit_window`;
CREATE TABLE `semester_timetable_edit_window` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `semester_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL,
  `location_id` int(11) NOT NULL,
  `timetable_owner_id` int(11) NOT NULL,
  `status` varchar(45) NOT NULL,
  `last_updated_on` datetime NOT NULL,
  `last_updated_by` varchar(45) NOT NULL,
  `dealine_creation_date` datetime NOT NULL,
  `daeadline_submission_date` datetime NOT NULL,
  `deadline_approval_date` datetime NOT NULL,
  `exam_date` datetime NOT NULL,
  `days_before_exam` int(11) NOT NULL,
  PRIMARY KEY (`id`,`semester_id`,`program_id`,`location_id`),
  KEY `semester_id` (`semester_id`),
  KEY `program_id` (`program_id`),
  KEY `location_id` (`location_id`),
  KEY `last_updated_by` (`last_updated_by`),
  KEY `timetable_owner_id` (`timetable_owner_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `batch`
--
SET FOREIGN_KEY_CHECKS=0;
ALTER TABLE `batch`
  ADD CONSTRAINT `batch_ibfk_1` FOREIGN KEY (`admittted_semester_id`) REFERENCES `semester` (`semester_id`);

--
-- Constraints for table `semester_milestone_plan_detail`
--
ALTER TABLE `semester_milestone_plan_detail`
  ADD CONSTRAINT `semester_milestone_plan_detail_ibfk_3` FOREIGN KEY (`semester_milestone_id`) REFERENCES `semester_milestone` (`milestone_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `semester_milestone_plan_detail_ibfk_4` FOREIGN KEY (`semester_milestone_plan_master_id`) REFERENCES `semester_milestone_plan_master` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `semester_milestone_plan_master`
--
ALTER TABLE `semester_milestone_plan_master`
  ADD CONSTRAINT `semester_milestone_plan_master_ibfk_18` FOREIGN KEY (`milestone_plan_owner_id`) REFERENCES `coordinator` (`coordinator_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `semester_milestone_plan_master_ibfk_10` FOREIGN KEY (`alternate_owner_id`) REFERENCES `coordinator` (`coordinator_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `semester_milestone_plan_master_ibfk_11` FOREIGN KEY (`location_id`) REFERENCES `location` (`location_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `semester_milestone_plan_master_ibfk_12` FOREIGN KEY (`degree_id`) REFERENCES `degree` (`degree_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `semester_milestone_plan_master_ibfk_13` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `semester_milestone_plan_master_ibfk_14` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`semester_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `semester_milestone_plan_master_ibfk_15` FOREIGN KEY (`batch_id`) REFERENCES `batch` (`batch_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `semester_milestone_plan_master_ibfk_16` FOREIGN KEY (`discipline_id`) REFERENCES `discipline` (`discipline_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `semester_milestone_plan_master_ibfk_17` FOREIGN KEY (`client_organization_id`) REFERENCES `organization` (`organization_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Constraints for table `semester_timetable_edit_window`
--
ALTER TABLE `semester_timetable_edit_window`
  ADD CONSTRAINT `semester_timetable_edit_window_ibfk_8` FOREIGN KEY (`timetable_owner_id`) REFERENCES `coordinator` (`coordinator_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `semester_timetable_edit_window_ibfk_4` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`semester_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `semester_timetable_edit_window_ibfk_5` FOREIGN KEY (`program_id`) REFERENCES `program` (`program_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `semester_timetable_edit_window_ibfk_6` FOREIGN KEY (`location_id`) REFERENCES `location` (`location_id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
