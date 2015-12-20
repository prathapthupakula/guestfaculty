# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class BufferType(models.Model):
    buffer_calc_id = models.IntegerField(primary_key=True)
    buffer_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    buffer_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'buffer_type'


class CandidateEvaluation(models.Model):
    application = models.ForeignKey('GuestFacultyCandidate')
    evaluation_id = models.IntegerField()
    evaluation_seq_no = models.IntegerField()
    evaluation_type = models.CharField(max_length=50)
    evaluator_names_list = models.CharField(max_length=200)
    evaluation_comments = models.CharField(db_column='evaluation comments', max_length=1000)  # Field renamed to remove unsuitable characters.
    evaluation_date = models.DateTimeField(blank=True, null=True)
    evaluation_venue = models.CharField(max_length=200, blank=True, null=True)
    evaluation_time_slot = models.CharField(max_length=45, blank=True, null=True)
    evaluation_result = models.CharField(max_length=45, blank=True, null=True)
    letter_for_evaluation_rnd_sent = models.IntegerField(blank=True, null=True)
    assessment_score = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    evaluation_location = models.ForeignKey('Location', blank=True, null=True)
    regret_letter_sent = models.IntegerField()
    selected_letter_sent = models.IntegerField()
    insert_datetime = models.DateTimeField()
    update_datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'candidate_evaluation'
        unique_together = (('application', 'evaluation_id'),)


class CandidateQualification(models.Model):
    application = models.ForeignKey('GuestFacultyCandidate')
    qualification = models.ForeignKey('Qualification')
    discipline = models.ForeignKey('Discipline')
    college = models.CharField(max_length=200)
    year_of_completion = models.IntegerField(blank=True, null=True)
    highest_qualification = models.IntegerField()
    completed = models.IntegerField()
    percent_marks_cpi_cgpa = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    max_marks_cpi_cgpa = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    normalized_marks_cpi_cgpa = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    degree_degree = models.ForeignKey('Degree')

    class Meta:
        managed = False
        db_table = 'candidate_qualification'
        unique_together = (('application', 'qualification', 'discipline', 'degree_degree'),)


class Coordinator(models.Model):
    coordinator_id = models.IntegerField(primary_key=True)
    coordinator_name = models.CharField(max_length=45)
    coordinator_address = models.CharField(max_length=500)
    phone = models.IntegerField(blank=True, null=True)
    mobile = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=100)
    coordinator_for_location = models.ForeignKey('Location', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coordinator'


class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=10)
    course_name = models.CharField(max_length=100)
    course_description = models.CharField(max_length=500, blank=True, null=True)
    number_of_lectures = models.IntegerField()
    dissertation_project_work = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'course'


class CourseLocationSemesterDetail(models.Model):
    course = models.ForeignKey(Course)
    location = models.ForeignKey('Location')
    semester = models.ForeignKey('Semester')
    discipline = models.ForeignKey('Discipline')
    program = models.ForeignKey('Program')
    max_faculty_count = models.IntegerField()
    number_of_students_in_class = models.IntegerField()
    number_of_sections = models.IntegerField(db_column='number _of_sections')  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'course_location_semester_detail'
        unique_together = (('course', 'location', 'semester'),)


class Degree(models.Model):
    degree_id = models.IntegerField(primary_key=True)
    degree_full_name = models.CharField(max_length=200, blank=True, null=True)
    degree_short_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'degree'


class Discipline(models.Model):
    discipline_id = models.IntegerField(primary_key=True)
    discipline_long_name = models.CharField(max_length=200, blank=True, null=True)
    discipline_short_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'discipline'


class FacultyClassAttendance(models.Model):
    semester = models.ForeignKey('Semester')
    course = models.ForeignKey(Course)
    program = models.ForeignKey('Program')
    guest_faculty = models.ForeignKey('GuestFaculty')
    class_date = models.DateTimeField()
    class_time_slot = models.CharField(max_length=45)
    absent = models.IntegerField()
    comments_for_absence = models.CharField(max_length=45, blank=True, null=True)
    insert_datetime = models.DateTimeField()
    update_datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'faculty_class_attendance'
        unique_together = (('semester', 'course', 'program', 'guest_faculty', 'class_date', 'class_time_slot'),)


class FeedbackSurvey(models.Model):
    survey_id = models.IntegerField()
    version_id = models.CharField(max_length=45)
    question_id = models.CharField(max_length=45)
    survey_name = models.CharField(max_length=45, blank=True, null=True)
    question_description = models.CharField(max_length=45, blank=True, null=True)
    question_type = models.CharField(max_length=45, blank=True, null=True)
    mandatory = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback_survey'
        unique_together = (('survey_id', 'version_id', 'question_id'),)


class GfInterestedInDiscipline(models.Model):
    discipline = models.ForeignKey(Discipline)
    guest_faculty = models.ForeignKey('GuestFaculty')
    areas_of_expertise = models.CharField(max_length=1000, blank=True, null=True)
    courses_can_handle = models.CharField(max_length=1000, blank=True, null=True)
    insert_date_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'gf_interested_in_discipline'
        unique_together = (('discipline', 'guest_faculty'),)


class GuestFaculty(models.Model):
    pan_number = models.CharField(max_length=10)
    guest_faculty_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateTimeField()
    email = models.CharField(max_length=100)
    total_experience_in_months = models.IntegerField(blank=True, null=True)
    phone = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    mobile = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    address1 = models.CharField(max_length=500)
    teach_experience_in_months = models.IntegerField(blank=True, null=True)
    current_organization = models.CharField(max_length=100)
    current_org_designation = models.CharField(max_length=100, blank=True, null=True)
    months_in_curr_org = models.IntegerField(blank=True, null=True)
    recruited_on_date = models.DateTimeField()
    current_location = models.ForeignKey('Location')
    last_updated_date = models.DateTimeField()
    inserted_date = models.DateTimeField()
    updated_by = models.CharField(max_length=100)
    confidentiality_requested = models.IntegerField()
    uploaded_cv_file_name = models.CharField(max_length=200)
    recruitment_location = models.ForeignKey('Location')
    payment_bank_name = models.CharField(max_length=200)
    bank_account_number = models.CharField(max_length=45)
    ifsc_code = models.CharField(max_length=15)
    bank_address = models.CharField(max_length=500)
    account_type = models.CharField(max_length=20)
    beneficiary_name = models.CharField(max_length=10)
    industry_exp_in_months = models.IntegerField(blank=True, null=True)
    nature_of_current_job = models.CharField(max_length=500, blank=True, null=True)
    certifications = models.CharField(max_length=2000, blank=True, null=True)
    awards_and_distinctions = models.CharField(max_length=2000, blank=True, null=True)
    publications = models.CharField(max_length=2000, blank=True, null=True)
    membership_of_prof_bodies = models.CharField(max_length=2000, blank=True, null=True)
    courses_taught = models.CharField(max_length=1000, blank=True, null=True)
    areas_of_expertise = models.CharField(max_length=2000, blank=True, null=True)
    taught_in_institutions = models.CharField(max_length=1000, blank=True, null=True)
    industry_projects_done = models.CharField(max_length=1000, blank=True, null=True)
    past_organizations = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guest_faculty'


class GuestFacultyCandidate(models.Model):
    application_id = models.IntegerField()
    pan_number = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateTimeField()
    email = models.CharField(max_length=100)
    total_experience_in_months = models.IntegerField()
    phone = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    mobile = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    address1 = models.CharField(max_length=500)
    teach_experience_in_months = models.IntegerField(blank=True, null=True)
    current_organization = models.CharField(max_length=100)
    current_org_designation = models.CharField(max_length=100)
    months_in_curr_org = models.IntegerField()
    current_location = models.ForeignKey('Location')
    application_status = models.CharField(max_length=45)
    reapplication = models.IntegerField()
    received_status = models.IntegerField(blank=True, null=True)
    application_ack_sent = models.IntegerField(blank=True, null=True)
    application_submission_date = models.DateTimeField(blank=True, null=True)
    applying_for_discipline = models.ForeignKey(Discipline)
    uploaded_cv_file_name = models.CharField(max_length=200, blank=True, null=True)
    industry_exp_in_months = models.IntegerField(blank=True, null=True)
    nature_of_current_job = models.CharField(max_length=200, blank=True, null=True)
    areas_of_expertise = models.CharField(max_length=2000, blank=True, null=True)
    certifications = models.CharField(max_length=1000, blank=True, null=True)
    awards_and_distinctions = models.CharField(max_length=1000, blank=True, null=True)
    publications = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guest_faculty_candidate'
        unique_together = (('application_id', 'applying_for_discipline'),)


class GuestFacultyCourseOffer(models.Model):
    course = models.ForeignKey(Course)
    semester = models.ForeignKey('Semester')
    program_id = models.IntegerField()
    guest_faculty = models.ForeignKey(GuestFaculty)
    location = models.ForeignKey('Location')
    course_offer_status = models.CharField(max_length=10)
    sequence_number = models.IntegerField()
    program_coordinator_id = models.IntegerField()
    offer_to_faculty_date = models.DateTimeField()
    number_students_in_class = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    section = models.CharField(max_length=20, blank=True, null=True)
    honorarium_given = models.IntegerField()
    honorarium_text = models.CharField(max_length=1000, blank=True, null=True)
    hon_issued_on_date = models.DateTimeField(blank=True, null=True)
    hon_issued_by = models.CharField(max_length=200, blank=True, null=True)
    honorarium_payment_mode = models.CharField(max_length=45, blank=True, null=True)
    insert_datetime = models.DateTimeField()
    update_datetime = models.DateTimeField()
    max_faculty_count_reached = models.IntegerField()
    assessment_score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    feedback = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guest_faculty_course_offer'
        unique_together = (('course', 'semester', 'program_id', 'guest_faculty', 'location', 'course_offer_status', 'sequence_number'),)


class GuestFacultyFeedbackResults(models.Model):
    guest_faculty_pan_number = models.ForeignKey(GuestFaculty, db_column='guest_faculty_pan_number')
    semester = models.ForeignKey('Semester')
    program = models.ForeignKey('Program')
    course = models.ForeignKey(Course)
    survey = models.ForeignKey(FeedbackSurvey)
    survey_version = models.ForeignKey(FeedbackSurvey)
    survey_question = models.ForeignKey(FeedbackSurvey)
    student_choice = models.CharField(max_length=45, blank=True, null=True)
    student_comments = models.CharField(max_length=1000, blank=True, null=True)
    answered_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'guest_faculty_feedback_results'
        unique_together = (('guest_faculty_pan_number', 'semester', 'program', 'course', 'survey', 'survey_version', 'survey_question'),)


class GuestFacultyHasLocation(models.Model):
    guest_faculty_faculty = models.ForeignKey(GuestFaculty)
    location_location = models.ForeignKey('Location')

    class Meta:
        managed = False
        db_table = 'guest_faculty_has_location'
        unique_together = (('guest_faculty_faculty', 'location_location'),)


class GuestFacultyHasQualification(models.Model):
    guest_faculty_faculty = models.ForeignKey(GuestFaculty)
    qualification_qualification = models.ForeignKey('Qualification')

    class Meta:
        managed = False
        db_table = 'guest_faculty_has_qualification'
        unique_together = (('guest_faculty_faculty', 'qualification_qualification'),)


class GuestFacultyPlanningNumbers(models.Model):
    program_coordinator = models.ForeignKey(Coordinator)
    location = models.ForeignKey('Location')
    course = models.ForeignKey(Course)
    program = models.ForeignKey('Program')
    semester = models.ForeignKey('Semester')
    discipline = models.ForeignKey(Discipline)
    version_number = models.IntegerField()
    buffer_type = models.ForeignKey(BufferType)
    current_plan_flag = models.IntegerField()
    plan_status = models.CharField(max_length=15)
    total_faculty_required = models.IntegerField()
    faculty_in_database = models.IntegerField()
    faculty_to_be_recruited = models.IntegerField(blank=True, null=True)
    buffer_number = models.IntegerField(blank=True, null=True)
    to_be_recruited_with_buffer = models.IntegerField(blank=True, null=True)
    planning_comments = models.CharField(max_length=2000, blank=True, null=True)
    created_by = models.CharField(max_length=45)
    created_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'guest_faculty_planning_numbers'
        unique_together = (('program_coordinator', 'location', 'course', 'program', 'semester', 'discipline', 'version_number'),)


class GuestFacultyQualification(models.Model):
    qualification = models.ForeignKey('Qualification')
    degree = models.ForeignKey(Degree)
    qualification_discipline = models.ForeignKey(Discipline)
    guest_faculty_pan_number = models.ForeignKey(GuestFaculty, db_column='guest_faculty_pan_number')
    college = models.CharField(max_length=200)
    year_of_completion = models.IntegerField()
    completed = models.IntegerField()
    highest_qualification = models.IntegerField()
    percent_marks_cpi_cgpa = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    max_marks_cpi_cgpa = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    inserted_date = models.DateTimeField()
    normalized_marks_cpi_cgpa = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    class Meta:
        managed = False
        db_table = 'guest_faculty_qualification'
        unique_together = (('qualification', 'degree', 'qualification_discipline', 'guest_faculty_pan_number'),)


class Location(models.Model):
    location_id = models.IntegerField(primary_key=True)
    location_name = models.CharField(max_length=45)
    location_state = models.CharField(max_length=45, blank=True, null=True)
    location_region = models.CharField(max_length=45, blank=True, null=True)
    location_country = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location'


class PlanningWindowStatus(models.Model):
    planning_id = models.IntegerField()
    semester = models.ForeignKey('Semester')
    program = models.ForeignKey('Program')
    status = models.CharField(max_length=15)
    updated_by = models.CharField(max_length=100)
    last_updated_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'planning_window_status'
        unique_together = (('planning_id', 'semester', 'program'),)


class Program(models.Model):
    program_id = models.IntegerField(primary_key=True)
    program_name = models.CharField(max_length=200)
    specific_program = models.IntegerField()
    client_organization = models.CharField(max_length=200, blank=True, null=True)
    program_coordinator = models.ForeignKey(Coordinator)

    class Meta:
        managed = False
        db_table = 'program'


class ProgramHasCourse(models.Model):
    program_program = models.ForeignKey(Program)
    course_course = models.ForeignKey(Course)
    degree_degree = models.ForeignKey(Degree)

    class Meta:
        managed = False
        db_table = 'program_has_course'
        unique_together = (('program_program', 'course_course', 'degree_degree'),)


class Qualification(models.Model):
    qualification_id = models.IntegerField(primary_key=True)
    qualification_name = models.CharField(max_length=45)
    qualification_level = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qualification'


class Semester(models.Model):
    semester_id = models.IntegerField(primary_key=True)
    semester_name = models.CharField(max_length=45)
    semester_number = models.CharField(max_length=45)
    year = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'semester'


class ValueLists(models.Model):
    id = models.IntegerField(primary_key=True)
    value_domain = models.CharField(db_column='value domain', max_length=45)  # Field renamed to remove unsuitable characters.
    value = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'value_lists'
