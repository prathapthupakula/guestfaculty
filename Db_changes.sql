SET FOREIGN_KEY_CHECKS=0;
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1;

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
