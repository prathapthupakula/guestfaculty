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

--
-- Constraints for dumped tables
--

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
