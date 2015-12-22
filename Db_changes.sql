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
