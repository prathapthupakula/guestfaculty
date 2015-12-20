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
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import Group 

from django.dispatch import receiver
from allauth.account.signals import user_signed_up

# Set First-Time registration to registrant role, so they can add a new application.
@receiver(user_signed_up)
def set_applicant(sender, **kwargs):
    user = kwargs.pop('user')  
    #user.is_staff = True
    user.username=user.email
    user.save()
    user.groups.add(Group.objects.get(name='registrant'))

STATUS_LIST = (
    ('Submitted', 'Submitted'),
    ('Shortlisted', 'Shortlisted'),
    ('In Process', 'In Process'),	
    ('Rejected', 'Rejected'),
)
GENDER_LIST = (
    ('M', 'Male'),
    ('F', 'Female'),
)

COUNTRY_LIST = (
    ('IN', 'India'),
    ('US', 'USA'),
    ('UK', 'United Kingdom'),
)



class CandidateEvaluation(models.Model):
    application = models.ForeignKey('GuestFacultyCandidate',editable=False)
    evaluation_id = models.AutoField(primary_key=True,editable=False)
    evaluation_seq_no = models.IntegerField(editable=False,default=1)
    evaluation_step = models.IntegerField(editable=False,default=1)
    evaluation_type = models.CharField(max_length=50,editable=False,default='Application Review')
    evaluator_names_list = models.CharField(max_length=200,editable=False)
    evaluation_comments = models.CharField(db_column='evaluation comments', max_length=1000)  # Field renamed to remove unsuitable characters.
    evaluation_date = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    evaluation_venue = models.CharField(max_length=200, blank=True, null=True, default='ONLINE')
    evaluation_time_slot = models.CharField(max_length=45, blank=True, null=True)
    evaluation_result = models.CharField(max_length=45, blank=True, null=True, choices=STATUS_LIST)
    letter_for_evaluation_rnd_sent = models.IntegerField(blank=True, null=True, default=0)
    assessment_score = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    evaluation_location = models.ForeignKey('Location', blank=True, null=True,editable=False)
    regret_letter_sent = models.IntegerField(editable=False, default=0)
    selected_letter_sent = models.IntegerField(editable=False, default=0)
    insert_datetime = models.DateTimeField(editable=False,default=datetime.datetime.now)
    update_datetime = models.DateTimeField(editable=False,default=datetime.datetime.now)

    class Meta:
        managed = False
        db_table = 'candidate_evaluation'
        #unique_together = (('application', 'evaluation_id'),)

    def __str__(self):              # Returns Name of Location wherever referenced
        return str(self.application)
		


class CandidateQualification(models.Model):
    candidate_qualificaton_id = models.AutoField(primary_key=True,editable=False)
    application = models.ForeignKey('GuestFacultyCandidate')
    qualification = models.ForeignKey('Qualification')
    discipline = models.ForeignKey('Discipline')
    college = models.CharField('School/College',max_length=200)
    year_of_completion = models.IntegerField(blank=True, null=True)
    highest_qualification = models.BooleanField()
    completed = models.BooleanField()
    percent_marks_cpi_cgpa = models.DecimalField('% Marks/CPI/CGPA',max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    max_marks_cpi_cgpa = models.DecimalField('Max Marks/CPI/CGPA',max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    normalized_marks_cpi_cgpa = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    degree_degree = models.ForeignKey('Degree',verbose_name='Degree') # Verbose_Name added since foriegn key column must be first

    class Meta:
        managed = False
        db_table = 'candidate_qualification'
        unique_together = (('application', 'qualification', 'discipline', 'degree_degree'),)
    
    def __str__(self):              # Returns Name of Location wherever referenced
        return ""

    # Generate normalized Marks based on user inputs
    def save(self, *args, **kwargs):
        if self.max_marks_cpi_cgpa > 50:
            factor = 100
        else: 
            factor = 10
        self.normalized_marks_cpi_cgpa = (self.percent_marks_cpi_cgpa/self.max_marks_cpi_cgpa)*factor
        super(CandidateQualification, self).save(*args, **kwargs)		
		
class Coordinator(models.Model):
    #coordinator = models.ForeignKey(User,primary_key=True,limit_choices_to={'is_staff': True,'coordinator':'True'})
    coordinator = models.ForeignKey(User,primary_key=True,limit_choices_to={'is_staff': True})
    coordinator_name = models.CharField(max_length=45)
    coordinator_address = models.CharField(max_length=500)
    phone = models.CharField(max_length=13,blank=True, null=True)
    mobile = models.CharField(max_length=13,blank=True, null=True)
    email = models.CharField(max_length=100)
    coordinator_for_location = models.ForeignKey('Location', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'coordinator'

    def __str__(self):              # Returns Name wherever referenced
        return self.coordinator_name	
	

class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=10)
    course_name = models.CharField(max_length=100)
    course_description = models.CharField(max_length=500, blank=True, null=True)
    number_of_lectures = models.IntegerField()
    dissertation_project_work = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'course'
		
    def __str__(self):              # Returns Name wherever referenced
        return self.course_name	

class CourseLocationSemesterDetail(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    course = models.ForeignKey(Course)
    location = models.ForeignKey('Location')
    semester = models.ForeignKey('Semester')
    discipline = models.ForeignKey('Discipline')
    program = models.ForeignKey('Program')
    max_faculty_count = models.IntegerField('Max Faculty')
    number_of_students_in_class = models.IntegerField('Class Size')
    number_of_sections = models.IntegerField(db_column='number _of_sections')  # Field renamed to remove unsuitable characters.
    assigned_count = models.IntegerField('Assigned',editable=False,default=0)
	
    class Meta:
        managed = False
        db_table = 'course_location_semester_detail'
        unique_together = (('course', 'location', 'semester'),)
        verbose_name = 'Course Semester Details'
        verbose_name_plural = 'Course Semester Details'
		
    def __str__(self):              # Returns Name wherever referenced
        return str(self.course) + "/" + str(self.location) + "/" + str(self.discipline) + "/" + str(self.semester)

		

class Degree(models.Model):
    degree_id = models.AutoField(primary_key=True,editable=False)
    degree_full_name = models.CharField(max_length=200, blank=True, null=True)
    degree_short_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'degree'

    def __str__(self):              # Returns Name wherever referenced
        return self.degree_full_name	
		

class Discipline(models.Model):
    discipline_id = models.AutoField(primary_key=True,editable=False)
    discipline_long_name = models.CharField('Name',max_length=200, blank=True, null=True)
    discipline_short_name = models.CharField('Code',max_length=45)

    class Meta:
        managed = False
        db_table = 'discipline'

    def __str__(self):              # Returns Name wherever referenced
        return self.discipline_long_name			

class FacultyClassAttendance(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    semester = models.ForeignKey('Semester')
    course = models.ForeignKey(Course)
    program = models.ForeignKey('Program')
    guest_faculty = models.ForeignKey('GuestFaculty')
    class_date = models.DateField()
    class_time_slot = models.CharField(max_length=45)
    absent = models.BooleanField()
    comments_for_absence = models.CharField(max_length=45, blank=True, null=True)
    insert_datetime = models.DateTimeField(editable=False,default=datetime.datetime.now)
    update_datetime = models.DateTimeField(editable=False,default=datetime.datetime.now)

    class Meta:
        managed = False
        db_table = 'faculty_class_attendance'
        unique_together = (('semester', 'course', 'program', 'guest_faculty', 'class_date', 'class_time_slot'),)

    def __str__(self):              # Returns Name wherever referenced
        return str(self.guest_faculty)		



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
    id = models.AutoField(primary_key=True, editable=False)
    discipline = models.ForeignKey(Discipline)
    guest_faculty = models.ForeignKey('GuestFaculty')
    areas_of_expertise = models.CharField(max_length=1000, blank=True, null=True)
    courses_can_handle = models.CharField(max_length=1000, blank=True, null=True)
    insert_date_time = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        managed = False
        db_table = 'gf_interested_in_discipline'
        unique_together = (('discipline', 'guest_faculty'),)
    
    def __str__(self):              #
        return ""

class GuestFaculty(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    pan_number = models.CharField(max_length=10)
    guest_faculty_id = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10,choices=GENDER_LIST)
    date_of_birth = models.DateField()
    email = models.CharField(max_length=100)
    total_experience_in_months = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    mobile = models.CharField(max_length=13, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    address1 = models.TextField(max_length=500)
    teach_experience_in_months = models.IntegerField(blank=True, null=True)
    current_organization = models.CharField(max_length=100)
    current_org_designation = models.CharField(max_length=100, blank=True, null=True)
    months_in_curr_org = models.IntegerField(blank=True, null=True)
    recruited_on_date = models.DateField()
    current_location = models.ForeignKey('Location',related_name="current_location")
    last_updated_date = models.DateTimeField(editable=False,default=datetime.datetime.now)
    inserted_date = models.DateTimeField(editable=False,default=datetime.datetime.now)
    updated_by = models.CharField(max_length=100)
    confidentiality_requested = models.BooleanField(default=0)
    uploaded_cv_file_name = models.FileField(max_length=200)
    recruitment_location = models.ForeignKey('Location',related_name="recruitment_location")
    payment_bank_name = models.CharField(max_length=200)
    bank_account_number = models.CharField(max_length=45)
    ifsc_code = models.CharField(max_length=15)
    bank_address = models.CharField(max_length=500)
    account_type = models.CharField(max_length=20)
    beneficiary_name = models.CharField(max_length=10)
    industry_exp_in_months = models.IntegerField(blank=True, null=True)
    nature_of_current_job = models.TextField(max_length=500, blank=True, null=True)
    certifications = models.TextField(max_length=2000, blank=True, null=True)
    awards_and_distinctions = models.TextField(max_length=2000, blank=True, null=True)
    publications = models.TextField(max_length=2000, blank=True, null=True)
    membership_of_prof_bodies = models.TextField(max_length=2000, blank=True, null=True)
    courses_taught = models.TextField(max_length=1000, blank=True, null=True)
    areas_of_expertise = models.TextField(max_length=2000, blank=True, null=True)
    taught_in_institutions = models.TextField(max_length=1000, blank=True, null=True)
    industry_projects_done = models.TextField(max_length=1000, blank=True, null=True)
    past_organizations = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guest_faculty'
        verbose_name = 'Guest Faculty Details'
        verbose_name_plural = 'Guest Faculty Details'

    def __str__(self):              # Returns Name of wherever referenced
        return self.name + "(" + self.guest_faculty_id + " - " + str(self.recruitment_location) + ")"
		
    #def save(self, *args, **kwargs):
    #    super(GuestFaculty, self).save(*args, **kwargs) # Call the "real" save() method.


class GuestFacultyCandidate(models.Model):
    application_id = models.AutoField(primary_key=True,editable=False)
    application_number = models.CharField(editable=False,max_length=25)
    pan_number = models.CharField('PAN Number',max_length=10)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GENDER_LIST)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=100)
    total_experience_in_months = models.IntegerField()
    phone = models.CharField(max_length=13)
    mobile = models.CharField(max_length=13)
    address1 = models.CharField(max_length=500)
    teach_experience_in_months = models.IntegerField(blank=True, null=True)
    current_organization = models.CharField(max_length=100)
    current_org_designation = models.CharField(max_length=100)
    months_in_curr_org = models.IntegerField()
    current_location = models.ForeignKey('Location')
    application_status = models.CharField(max_length=45)
    reapplication = models.BooleanField()
    received_status = models.IntegerField(blank=True, null=True)
    application_ack_sent = models.IntegerField(blank=True, null=True)
    application_submission_date = models.DateTimeField('Applied On')
    applying_for_discipline = models.ForeignKey(Discipline)
    uploaded_cv_file_name = models.FileField('Upload CV',max_length=200, blank=True, null=True)
    industry_exp_in_months = models.IntegerField(blank=True, null=True)
    nature_of_current_job = models.CharField(max_length=200, blank=True, null=True)
    areas_of_expertise = models.CharField(max_length=2000, blank=True, null=True)
    certifications = models.CharField(max_length=1000, blank=True, null=True)
    awards_and_distinctions = models.CharField(max_length=1000, blank=True, null=True)
    publications = models.CharField(max_length=2000, blank=True, null=True)
    by_user = models.ForeignKey(User, null=True, blank=True)
	
    class Meta:
        managed = False
        db_table = 'guest_faculty_candidate'
        #unique_together = (('application_id', 'applying_for_discipline'),)
        verbose_name = 'Guest Faculty Candidate'

    def __str__(self):              # Returns Name of Location wherever referenced
        return self.application_number + "(" + self.name + ")"

    def get_id(self):
        return str(self.id)
    getid = property(get_id)		
	
    # Following function handle default Save and dependencies	
    #def save(self):
    #    if not self.application_id:
    #        self.application_submission_date = datetime.datetime.today()
    #        self.application_status = 'SUB'
	#		#self.total_experience_in_months = self.months_in_curr_org + self.industry_exp_in_months
    #        #self.by_user = request.user #This is not working here		
    #    super(GuestFacultyCandidate, self).save()	#Call the original action

class GuestFacultyCourseOffer(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    #course_location_semester = models.ForeignKey('CourseLocationSemesterDetail')
    course = models.ForeignKey(Course)
    semester = models.ForeignKey('Semester')
    program = models.ForeignKey('Program')
    guest_faculty = models.ForeignKey(GuestFaculty)
    location = models.ForeignKey('Location')
    course_offer_status = models.CharField('Status',max_length=10)
    sequence_number = models.IntegerField()
    program_coordinator = models.ForeignKey(Coordinator)
    offer_to_faculty_date = models.DateTimeField('Offer Date')
    number_students_in_class = models.IntegerField('Class Size') 
    section = models.CharField(max_length=20, blank=True, null=True)
    honorarium_given = models.NullBooleanField(blank=True, null=True)
    honorarium_text = models.CharField(max_length=1000, blank=True, null=True)
    hon_issued_on_date = models.DateTimeField(blank=True, null=True)
    hon_issued_by = models.CharField(max_length=200, blank=True, null=True)
    honorarium_payment_mode = models.CharField(max_length=45, blank=True, null=True)
    insert_datetime = models.DateTimeField(default=datetime.datetime.now)
    update_datetime = models.DateTimeField(default=datetime.datetime.now)
    max_faculty_count_reached = models.IntegerField(default=0)
    assessment_score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    feedback = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guest_faculty_course_offer'
        unique_together = (('course', 'semester', 'program', 'guest_faculty', 'location', 'course_offer_status'),)
        verbose_name = 'Course Assignment'

class GuestFacultyHonararium(GuestFacultyCourseOffer):

    class Meta:
        proxy = True	
        managed = False         
        verbose_name = 'Guest Faculty Honararium'
		
class GuestFacultyFeedbackResults(models.Model):
    guest_faculty_pan_number = models.ForeignKey(GuestFaculty, db_column='guest_faculty_pan_number')
    semester = models.ForeignKey('Semester')
    program = models.ForeignKey('Program')
    course = models.ForeignKey(Course)
    survey = models.ForeignKey(FeedbackSurvey,related_name="survey")
    survey_version = models.ForeignKey(FeedbackSurvey,related_name="survey_version")
    survey_question = models.ForeignKey(FeedbackSurvey,related_name="survey_question")
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





class GuestFacultyQualification(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    guest_faculty = models.ForeignKey('GuestFaculty')
    qualification = models.ForeignKey('Qualification')
    degree = models.ForeignKey(Degree)
    qualification_discipline = models.ForeignKey(Discipline)
    guest_faculty_pan_number = models.CharField(max_length=10)
    college = models.CharField(max_length=200)
    year_of_completion = models.IntegerField()
    completed = models.BooleanField()
    highest_qualification = models.BooleanField()
    percent_marks_cpi_cgpa = models.DecimalField(max_digits=10, decimal_places=2)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    max_marks_cpi_cgpa = models.DecimalField(max_digits=10, decimal_places=2)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    inserted_date = models.DateTimeField()
    normalized_marks_cpi_cgpa = models.DecimalField(max_digits=10, decimal_places=2)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    class Meta:
        managed = False
        db_table = 'guest_faculty_qualification'
        unique_together = (('qualification', 'degree', 'qualification_discipline', 'guest_faculty_pan_number'),)

    def __str__(self):              # Returns Name of Location wherever referenced
        return ""		

class Location(models.Model):
    location_id = models.AutoField(primary_key=True, editable=False)
    location_name = models.CharField('Location', max_length=45)
    location_state = models.CharField('State', max_length=45)
    location_region = models.CharField('Region', max_length=45, help_text='Please enter region or area')
    location_country = models.CharField('Country', max_length=45, default='IN', choices=COUNTRY_LIST)

    class Meta:
        managed = False
        db_table = 'location'

    def __str__(self):              # Returns Name of Location wherever referenced
        return self.location_name	




class Program(models.Model):
    program_id = models.AutoField(primary_key=True,editable=False)
    program_name = models.CharField(max_length=200)
    specific_program = models.BooleanField()
    client_organization = models.CharField(max_length=200, blank=True, null=True)
    program_coordinator = models.ForeignKey(Coordinator)

    class Meta:
        managed = False
        db_table = 'program'
	unique_together = (('program_coordinator'),)

    def __str__(self):              # Returns Name wherever referenced
        return self.program_name		


class ProgramHasCourse(models.Model):
    program_program = models.ForeignKey(Program)
    course_course = models.ForeignKey(Course)
    degree_degree = models.ForeignKey(Degree)

    class Meta:
        managed = False
        db_table = 'program_has_course'
        unique_together = (('program_program', 'course_course', 'degree_degree'),)


class Qualification(models.Model):
    qualification_id = models.AutoField(primary_key=True,editable=False)
    qualification_name = models.CharField('Qualification',max_length=45)
    qualification_level = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qualification'

    def __str__(self):              # Returns Name wherever referenced
        return self.qualification_name	
		

class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True,editable=False)
    semester_name = models.CharField(max_length=45)
    semester_number = models.CharField(max_length=45)
    year = models.CharField(max_length=45)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
	
    class Meta:
        managed = False
        db_table = 'semester'

    def __str__(self):              # Returns Name wherever referenced
        return self.semester_name	

class ValueLists(models.Model):
    id = models.IntegerField(primary_key=True)
    value_domain = models.CharField(db_column='value domain', max_length=45)  # Field renamed to remove unsuitable characters.
    value = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'value_lists'
