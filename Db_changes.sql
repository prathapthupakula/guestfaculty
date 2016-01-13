CREATE TABLE `application_users` (
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `current_semester` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `currentsemester_id` int(11) NOT NULL,
  `created_on_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `currentsemester_id` (`currentsemester_id`),
  CONSTRAINT `current_semester_ibfk_1` FOREIGN KEY (`currentsemester_id`) REFERENCES `semester` (`semester_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;