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
from django.contrib.auth.models import User,UserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model as user_model



from django.contrib.auth.models import Group 
from django.conf import settings
from django.db.models.signals import class_prepared
from django.core.validators import MaxLengthValidator


from django.dispatch import receiver
from allauth.account.signals import user_signed_up

from django.utils.translation import ugettext_lazy as _
#import init.py



import sys
reload(sys)
sys.setdefaultencoding("ISO-8859-1")

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


FIELD_NAMES = (
    ('lecture_rate_used', 'Lecture_Rate_Used'),
    ('mid_sem_qp_rate_used', 'Mid_Sem_qp_rate_used'),
    ('compre_qp_rate_used','Compre_qp_rate_used'),
    ('mid_sem_eval_rate_used','Mid_sem_eval_rate_used'),
    ('compre_eval_rate_used','Compre_eval_rate_used'),
    ('assignment_eval_rate_used','Assignment_eval_rate_used'),
    ('dissertation_rate_used','Dissertation_rate_used'),
    ('course_type_rate_used','Course_type_rate_used'),
    ('course_type_section_location_honorarium','Course_type_section_location_honorarium'),
)


FIELD_LIST = (
    ('regular','Regular'),
    ('flipped','Flipped'),
    ('none','None')
)


FIELD_LIST1 = (
    ('single location multiple sections','Single Location multiple sections'),
    ('multiple locations multiple sections','multiple locations multiple sections'),
    ('single location single section','Single Location single Section'),
    ('multiple locations single section','Multiple locations single section'),
    ('none','None')
)

NEW_USERNAME_LENGTH = 254
#User = user_model()

def extend_username():
    username = User._meta.get_field("username")
    username.max_length = NEW_USERNAME_LENGTH
    username.help_text = ""
    for v in username.validators:
        if isinstance(v, MaxLengthValidator):
            v.limit_value = NEW_USERNAME_LENGTH
extend_username()

class CandidateEvaluation(models.Model):
    application = models.ForeignKey('GuestFacultyCandidate',editable=False)
    evaluation_id = models.AutoField(primary_key=True,editable=False)
    evaluation_seq_no = models.IntegerField(editable=False,default=1)
    evaluation_step = models.IntegerField(editable=False,default=1)
    evaluation_type = models.CharField(max_length=50,editable=False,default='Application Review')
    evaluator_names_list = models.CharField(max_length=200,editable=False)
    evaluation_comments = models.CharField(db_column='evaluation comments', max_length=1000)  # Field renamed to remove unsuitable characters.
    evaluation_date = models.DateField(blank=True, null=True,auto_now_add=True)
    evaluation_venue = models.CharField(max_length=200, blank=True, null=True, default='ONLINE')
    evaluation_time_slot = models.CharField(max_length=45, blank=True, null=True)
    evaluation_result = models.CharField(max_length=45, blank=True, null=True, choices=STATUS_LIST)
    letter_for_evaluation_rnd_sent = models.IntegerField(blank=True, null=True, default=0)
    assessment_score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    evaluation_location = models.ForeignKey('Location', blank=True, null=True,editable=False)
    regret_letter_sent = models.IntegerField(editable=False, default=0)
    selected_letter_sent = models.IntegerField(editable=False, default=0)
    interview_venue_conformed = models.BooleanField(default = 0,) 
    insert_datetime = models.DateTimeField(editable=False,default=datetime.datetime.now)
    update_datetime = models.DateTimeField(editable=False,default=datetime.datetime.now)

    class Meta:
        managed = False
        db_table = 'candidate_evaluation'
        #unique_together = (('application', 'evaluation_id'),)
        #verbose_name = 'Guest Faculty Candidate Evalution'
        verbose_name = 'Guest Faculty Candidate Evaluation'
        verbose_name_plural = 'Guest Faculty Candidate Evaluation'

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
    percent_marks_cpi_cgpa = models.DecimalField('% Marks/CPI/CGPA',max_digits=10, decimal_places=2)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    max_marks_cpi_cgpa = models.DecimalField("Max Marks/CPI/CGPA",max_digits=10, decimal_places=2,blank=True, null=True)  
  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
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
        #self.normalized_marks_cpi_cgpa = (self.percent_marks_cpi_cgpa/self.max_marks_cpi_cgpa)*factor
        super(CandidateQualification, self).save(*args, **kwargs)		
		
class Coordinator(models.Model):
    #User = user_model()
    #coordinator = models.ForeignKey(User,primary_key=True,limit_choices_to={'is_staff': True,'coordinator':'True'})
    #id = models.AutoField(editable=False,primary_key=True)
    #coordinator = models.ForeignKey(User,primary_key=True,limit_choices_to={'is_staff': True},verbose_name='coordinator Id',help_text='Choose Coordinator ID from existing users list')
    coordinator = models.ForeignKey(User,primary_key=True,limit_choices_to={'is_staff': True},verbose_name='coordinator Id',help_text='Choose Coordinator ID from existing users list')

    coordinator_name = models.CharField(max_length=45)
    coordinator_address = models.CharField(max_length=500)
    phone = models.CharField(max_length=13,blank=True, null=True)
    mobile = models.CharField(max_length=13,blank=True, null=True)
    email = models.CharField(max_length=100,blank=True, null=True)
    coordinator_for_location = models.ForeignKey('Location', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'coordinator'
        verbose_name = 'Coordinator Master'
        verbose_name_plural = 'Coordinator Master'

    def __str__(self):              # Returns Name wherever referenced
        return str(self.coordinator_name)	
    #def username1(self):
    #   return self.user.username
    #username1.admin_order_field = 'user.username'
    #username1.short_description = 'program coordinator'

class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=10)
    course_name = models.CharField(max_length=100)
    course_description = models.CharField(max_length=500, blank=True, null=True)
    number_of_lectures = models.IntegerField()
    dissertation_project_work = models.IntegerField()

    class Meta:
        ordering = ('course_name',)        
        managed = False
        db_table = 'course'
	unique_together = (('course_name'),)
        verbose_name = 'Course Master'
        verbose_name_plural = 'Course Master'
		
    def __str__(self):              # Returns Name wherever referenced
        return self.course_name	

    

class CourseLocationSemesterDetail(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    course = models.ForeignKey('Course')
    location = models.ForeignKey('Location')
    semester = models.ForeignKey('Semester')
    discipline = models.ForeignKey('Discipline')
    program = models.ForeignKey('Program')
    max_faculty_count = models.IntegerField('Max Faculty')
    number_of_students_in_class = models.IntegerField('Class Size')
    number_of_sections = models.IntegerField(db_column='number _of_sections')  # Field renamed to remove unsuitable characters.
    assigned_count = models.IntegerField('Assigned',editable=False,default=0)
    accepted_count = models.IntegerField('Accepted',editable=False,default=0)
	
    class Meta:
        managed = False
        db_table = 'course_location_semester_detail'
        unique_together = (('course', 'location', 'semester'),)
        verbose_name = 'Course Location Semester Details'
        verbose_name_plural = 'Course Location Semester Details. Assign Course to Faculty'
		
    def __str__(self):              # Returns Name wherever referenced
        return str(self.course) + "/" + str(self.location) + "/" + str(self.discipline) + "/" + str(self.semester)

		

class Degree(models.Model):
    degree_id = models.AutoField(primary_key=True,editable=False)
    degree_full_name = models.CharField(max_length=200, blank=True, null=True)
    degree_short_name = models.CharField(max_length=45, blank=True, null=True)
    
    class Meta:
        ordering = ('degree_full_name',)
        managed = False
        db_table = 'degree'
        verbose_name_plural = 'Degree Master'


    def __str__(self):              # Returns Name wherever referenced
        return self.degree_full_name	
		

class Discipline(models.Model):
    discipline_id = models.AutoField(primary_key=True,editable=False)
    discipline_long_name = models.CharField('Name',max_length=200, blank=True, null=True)
    discipline_short_name = models.CharField('Code',max_length=45)

    class Meta:
        ordering=('discipline_long_name',)
        managed = False
        db_table = 'discipline'
        verbose_name = 'Academic Discipline Master'
        verbose_name_plural = 'Academic Discipline Master'

    def __str__(self):              # Returns Name wherever referenced
        return self.discipline_long_name	

		

class Natureofcurrentjob(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    name = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'nature_of_current_job'
        verbose_name_plural = 'Nature Of Current Job'


    def __str__(self):              # Returns Name wherever referenced
        return self.name	

  

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
        verbose_name = 'Guest Faculty Class Attendance'
        verbose_name_plural = 'Guest Faculty Class Attendance'

    def __str__(self):              # Returns Name wherever referenced
        return str(self.guest_faculty)		



class FeedbackSurvey(models.Model):
    survey_id = models.IntegerField(primary_key=True,editable=False,unique=True)
    version_id = models.CharField(max_length=45,editable=False)
    question_id = models.CharField(max_length=45,editable=False)
    survey_name = models.CharField(max_length=45, blank=True, null=True,editable=False)
    question_description = models.CharField(max_length=45, blank=True, null=True,editable=False)
    question_type = models.CharField(max_length=45, blank=True, null=True,editable=False)
    mandatory = models.IntegerField(blank=True, null=True,editable=False)

    class Meta:
        managed = False
        db_table = 'feedback_survey'
        unique_together = (('survey_id', 'version_id', 'question_id'),)
        verbose_name = 'Faculty Feedback'
        verbose_name_plural = 'Faculty Feedback'

    def __str__(self):              # Returns Name wherever referenced
        return str(self.survey_name)		



class GfInterestedInDiscipline(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    discipline = models.ForeignKey(Discipline)
    guest_faculty = models.ForeignKey('GuestFaculty')
    areas_of_expertise = models.CharField(max_length=1000, null=True)
    courses_can_handle = models.CharField(max_length=1000,  null=True)
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
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=100)
    total_experience_in_months = models.IntegerField("total experience in years", null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    mobile = models.CharField(max_length=13, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    address1 = models.TextField(max_length=500)
    teach_experience_in_months = models.IntegerField("Teach experience in years", null=True)
    current_organization = models.CharField(max_length=100)
    current_org_designation = models.CharField(max_length=100, null=True)
    months_in_curr_org = models.IntegerField(blank=True, null=True)
    recruited_on_date = models.DateField(editable=False,default=datetime.datetime.now)
    current_location = models.ForeignKey('Location',related_name="current_location")
    last_updated_date = models.DateTimeField(editable=False,default=datetime.datetime.now)
    inserted_date = models.DateTimeField(editable=False,default=datetime.datetime.now)
    #updated_by = models.IntegerField(blank=True, null=True, verbose_name = 'Last Updated By')
   # updated_by = models.ForeignKey(User, null=True, blank=True, verbose_name = 'Last Updated By')
    updated_by = models.CharField(max_length=45,)
    confidentiality_requested = models.BooleanField(default=0)
    uploaded_cv_file_name = models.FileField(max_length=200, null=True,blank=True)
    recruitment_location = models.ForeignKey('Location',related_name="recruitment_location")
    payment_bank_name = models.CharField(max_length=200)
    bank_account_number = models.CharField(max_length=45)
    ifsc_code = models.CharField(max_length=15)
    bank_address = models.CharField(max_length=500)
    account_type = models.CharField(max_length=20)
    beneficiary_name = models.CharField("Beneficiary PAN number",max_length=10)
    industry_exp_in_months = models.IntegerField("Industry exp in years", null=True)
    nature_of_current_job =  models.ForeignKey(Natureofcurrentjob,null=True, blank=True)
    certifications = models.TextField(max_length=2000, blank=True, null=True)
    awards_and_distinctions = models.TextField(max_length=2000, blank=True, null=True)
    publications = models.TextField(max_length=2000, blank=True, null=True)
    membership_of_prof_bodies = models.TextField(max_length=2000, blank=True, null=True)
    courses_taught = models.TextField(max_length=1000, blank=True, null=True)
    areas_of_expertise = models.TextField(max_length=2000, blank=True, null=True)
    taught_in_institutions = models.TextField(max_length=1000, blank=True, null=True)
    industry_projects_done = models.TextField(max_length=1000, blank=True, null=True)
    past_organizations = models.TextField(max_length=1000, blank=True, null=True)
    inactive_flag = models.BooleanField('Inactive',)
    active_flag = models.BooleanField('Active')

    class Meta:
        managed = False
        db_table = 'guest_faculty'
        verbose_name = 'Guest Faculty'
        verbose_name_plural = 'Guest Faculty'
        ordering = ('name',)
    def __str__(self):              # Returns Name of wherever referenced
        return self.name + "(" + self.guest_faculty_id + " - " + str(self.recruitment_location) + ")"
    def get_id(self):
        return str(self.id)
    getid = property(get_id)
    def __str__(self):
        return self.name
    #def __str__(self):
        #return str(self.updated_by_id)

#    def facultystatus(self):
#       return self.inactive_flag
#    facultystatus.admin_order_field = 'inactive_flag'
#    facultystatus.short_description = 'Guest Faculty Status'

#    def updatedby(self):
       # return self.updated_by(user.username)
   # updatedby.admin_order_field = 'updated_by'
   # updatedby.short_description = 'Last Updated By'
		
    #def save(self, *args, **kwargs):
    #    super(GuestFaculty, self).save(*args, **kwargs) # Call the "real" save() method.


class GuestFacultyCandidate(models.Model):
    application_id = models.AutoField(primary_key=True,editable=False)
    application_number = models.CharField(editable=False,max_length=25)
    pan_number = models.CharField('PAN Number',max_length=10)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GENDER_LIST)
    date_of_birth = models.DateField()
    email = models.EmailField(max_length=100)
    total_experience_in_months = models.IntegerField("Total experience in years", null=True)
    phone = models.CharField(max_length=13)
    mobile = models.CharField(max_length=13)
    address1 = models.TextField(max_length=500)
    teach_experience_in_months = models.IntegerField("teach experience in years", null=True)
    current_organization = models.CharField(max_length=100)
    current_org_designation = models.CharField(max_length=100, null=True)
    months_in_curr_org = models.IntegerField(blank=True, null=True)
    current_location = models.ForeignKey('Location')
    application_status = models.CharField(max_length=45)
    reapplication = models.BooleanField()
    received_status = models.IntegerField(blank=True, null=True)
    application_ack_sent = models.IntegerField(blank=True, null=True)
    application_submission_date = models.DateTimeField('Applied On')
    applying_for_discipline = models.ForeignKey(Discipline)
    uploaded_cv_file_name = models.FileField('Upload CV',max_length=200,)
    industry_exp_in_months = models.IntegerField( "industry exp in years", null=True)
    nature_of_current_job =  models.ForeignKey(Natureofcurrentjob,)
    areas_of_expertise = models.TextField(max_length=2000,)
    certifications = models.TextField(max_length=1000,)
    awards_and_distinctions = models.TextField(max_length=1000,)
    publications = models.TextField(max_length=2000,)
    by_user = models.ForeignKey(User, null=True, blank=True)
	
    class Meta:
        managed = False
        db_table = 'guest_faculty_candidate'
        #unique_together = (('application_id', 'applying_for_discipline'),)
        verbose_name = 'Fill in the Guest Faculty Application Form '
        verbose_name_plural = 'Guest Faculty Candidate'
        ordering = ('name',)        

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
    course = models.ForeignKey('Course')
    semester = models.ForeignKey('Semester')
    program = models.ForeignKey('Program')
    guest_faculty = models.ForeignKey('GuestFaculty')
    location = models.ForeignKey('Location')
    course_offer_status = models.CharField('Status',max_length=10)
    sequence_number = models.IntegerField()
    program_coordinator = models.ForeignKey('Coordinator')
    offer_to_faculty_date = models.DateTimeField('Offer Date')
    number_students_in_class = models.IntegerField('Class Size') 
    section = models.CharField(max_length=20, blank=True, null=True)
    honorarium_given = models.NullBooleanField(blank=True, null=True)
    honorarium_text = models.CharField(max_length=1000, blank=True, null=True)
    hon_issued_on_date = models.DateTimeField(blank=True, null=True)
    hon_issued_by = models.CharField(max_length=200, blank=True, null=True)
    honorarium_payment_mode = models.CharField(max_length=45, blank=True, null=True)
    honorarium_amount_paid =  models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    honorarium_pay_date = models.DateTimeField(blank=True, null=True)
    insert_datetime = models.DateTimeField(default=datetime.datetime.now)
    update_datetime = models.DateTimeField(default=datetime.datetime.now)
    max_faculty_count_reached = models.IntegerField(default=0)
    assessment_score = models.DecimalField('Score',max_digits=10, decimal_places=2, blank=True, null=True)
    feedback = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guest_faculty_course_offer'
        unique_together = (('course', 'semester', 'guest_faculty','sequence_number'),)
        verbose_name = 'Guest Faculty Course Assignments'
        verbose_name_plural = 'Guest Faculty Course Assignments'

    def __str__(self):              # Returns Name of Location wherever referenced
        return str(self.course)
		
class GuestFacultyHonararium(GuestFacultyCourseOffer):

    class Meta:
        proxy = True	
        managed = False         
        #verbose_name = 'Guest Faculty Honararium'
        verbose_name = 'Guest Faculty Honorarium'
        verbose_name_plural = 'Guest Faculty Honorarium'
		
class GuestFacultyScore(GuestFacultyCourseOffer):

    class Meta:
        proxy = True	
        managed = False         
        verbose_name = 'Guest Faculty  Assessment Score'
       


		
class GuestFacultyFeedbackResults(models.Model):
    # Commented out foreign key relations as the parent keys are not unique 
    #guest_faculty_pan_number = models.ForeignKey(GuestFaculty,primary_key=True,db_column="guest_faculty_pan_number",related_name="guest_faculty_pan_number",editable=False,to_field="pan_number")
    guest_faculty_pan_number = models.TextField(primary_key=True,db_column="guest_faculty_pan_number",editable=False)
    semester = models.ForeignKey('Semester',primary_key=True,editable=False)
    program = models.ForeignKey('Program',primary_key=True,editable=False)
    course = models.ForeignKey(Course,primary_key=True,editable=False)
    #survey = models.ForeignKey(FeedbackSurvey,primary_key=True,related_name="survey",editable=False,to_field="survey_id")
    survey_id = models.TextField(primary_key=True,editable=False)
    #survey_version = models.ForeignKey(FeedbackSurvey,primary_key=True,related_name="survey_version",editable=False,to_field="version_id")
    survey_version_id = models.TextField(primary_key=True,editable=False)
    #survey_question = models.ForeignKey(FeedbackSurvey,primary_key=True,related_name="survey_question",editable=False,to_field="question_id")
    survey_question_id = models.TextField(primary_key=True,editable=False)
    student_choice = models.CharField(max_length=45, blank=True, null=True)
    student_comments = models.CharField(max_length=1000, blank=True, null=True)
    answered_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'guest_faculty_feedback_results'
        #unique_together = (('guest_faculty_pan_number', 'semester', 'program', 'course', 'survey', 'survey_version', 'survey_question'),)
        verbose_name = 'Guest Faculty Feedback'
        verbose_name_plural = 'Guest Faculty Feedback'
		

"""class GuestFacultyHasLocation(models.Model):
    guest_faculty_faculty = models.ForeignKey(GuestFaculty)
    location_location = models.ForeignKey('Location')

    class Meta:
        managed = False
        db_table = 'guest_faculty_has_location'
        unique_together = (('guest_faculty_faculty', 'location_location'),)"""


"""class GuestFacultyHasQualification(models.Model):
    guest_faculty_faculty = models.ForeignKey(GuestFaculty)
    qualification_qualification = models.ForeignKey('Qualification')

    class Meta:
        managed = False
        db_table = 'guest_faculty_has_qualification'
        unique_together = (('guest_faculty_faculty', 'qualification_qualification'),)"""





class GuestFacultyQualification(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    #guest_faculty = models.ForeignKey('GuestFaculty')
    qualification = models.ForeignKey('Qualification')
    degree = models.ForeignKey(Degree)
    qualification_discipline = models.ForeignKey(Discipline)
    guest_faculty = models.ForeignKey('GuestFaculty')
    guest_faculty_pan_number = models.CharField(max_length=10)
    college = models.CharField(max_length=200)
    year_of_completion = models.IntegerField()
    completed = models.BooleanField()
    #highest_qualification = models.BooleanField()
    highest_qualification = models.BooleanField()
    percent_marks_cpi_cgpa = models.DecimalField(max_digits=10, decimal_places=2,default=0)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    max_marks_cpi_cgpa = models.DecimalField(max_digits=10, decimal_places=2,default=0,blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    inserted_date = models.DateTimeField(default=datetime.datetime.now)
    normalized_marks_cpi_cgpa = models.DecimalField(max_digits=10, decimal_places=2,default=0)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    class Meta:
        managed = False
        db_table = 'guest_faculty_qualification'
        verbose_name = 'Guest Faculty Qualification'
        verbose_name_plural = 'Guest Faculty Qualification'
        #unique_together = (('qualification', 'degree', 'qualification_discipline', 'guest_faculty_pan_number'),)

    def __str__(self):              # Returns Name of Location wherever referenced
        return ""		

class Location(models.Model):
    location_id = models.AutoField(primary_key=True, editable=False)
    location_name = models.CharField('Location', max_length=45)
    location_state = models.CharField('State', max_length=45)
    location_region = models.CharField('Region', max_length=45, help_text='Please enter region or area')
    location_country = models.CharField('Country', max_length=45, default='IN', choices=COUNTRY_LIST)

    class Meta:
        ordering = ('location_name',)
        managed = False
        db_table = 'location'
        #app_label = "LOCATTAIAOAO"
        #verbose_name = 'Coordinator Master'
        verbose_name = 'Location Master'
        verbose_name_plural = 'Location Master'

    def __str__(self):              # Returns Name of Location wherever referenced
        return self.location_name	




class Program(models.Model):
    program_id = models.AutoField(primary_key=True,editable=False)
    program_code = models.CharField(max_length=10)
    program_name = models.CharField(max_length=200)
    specific_program = models.BooleanField()
    client_organization = models.CharField(max_length=200, blank=True, null=True)
    program_coordinator = models.ForeignKey(Coordinator,blank=True, null=True)

    class Meta:
        ordering = ('program_name',)
        managed = False
        db_table = 'program'
	unique_together = (('program_code'),)
        verbose_name = 'Program Master'
        verbose_name_plural = 'Program Master'

    def __str__(self):              # Returns Name wherever referenced
        #return self.program_name + "-" + self.program_code + ""
        return self.program_name

"""class ProgramHasCourse(models.Model):
    program_program = models.ForeignKey(Program)
    course_course = models.ForeignKey(Course)
    degree_degree = models.ForeignKey(Degree)

    class Meta:
        managed = False
        db_table = 'program_has_course'
        unique_together = (('program_program', 'course_course', 'degree_degree'),)"""


class Qualification(models.Model):
    qualification_id = models.AutoField(primary_key=True,editable=False)
    qualification_name = models.CharField('Qualification',max_length=45)
    qualification_level = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        verbose_name = 'Qualification Master'
        verbose_name_plural = 'Qualification Master'
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
        ordering = ('semester_name',)
        managed = False
        db_table = 'semester'
        verbose_name = 'Semester Master'
        verbose_name_plural = 'Semester Master'

    def __str__(self):              # Returns Name wherever referenced
        return self.semester_name	

class ValueLists(models.Model):
    id = models.IntegerField(primary_key=True)
    value_domain = models.CharField(db_column='value domain', max_length=45)  # Field renamed to remove unsuitable characters.
    value = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'value_lists'

class FacultyBucketMaster(models.Model):
    bucket_id = models.AutoField(primary_key=True, editable=False)
    bucket_name = models.CharField(max_length=55,verbose_name='Categery Name')
    active_bucket_flag = models.BooleanField(default=1)
    lower_tech_interval_gap = models.DecimalField(max_digits=10, decimal_places=0,default=None,verbose_name='Lower Limit in Semesters for Teaching History',blank=True, null=True)
    #upper_tech_interval_gap = models.IntegerField(verbose_name='Upper Limit in Semesters for Teaching History')
    upper_tech_interval_gap = models.DecimalField(max_digits=10, decimal_places=0,default=None,verbose_name='Upper Limit in Semesters for Teaching History',blank=True, null=True)
    inactive_faculty_flag = models.BooleanField('Inactive Flag')
    current_faculty_flag = models.BooleanField('Current Flag')
    lower_bound_year = models.IntegerField()
    lower_bound_sem_nbr = models.IntegerField()
    upper_bound_year = models.IntegerField()
    upper_bound_sem_nbr = models.IntegerField()
    created_on=models.DateTimeField(editable=False,default=datetime.datetime.now)
    created_by=models.IntegerField(blank=True, null=True)
    updated_on = models.DateTimeField(editable=False,default=datetime.datetime.now)
    updated_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        ordering = ('created_on',)
        #ordering = ('-bucket_id',)
        db_table = 'faculty_bucket_master'
        verbose_name = 'Guest Faculty Category Definitions'
        verbose_name_plural = 'Guest Faculty Category Definitions'
    def __str__(self):              # Returns Name wherever referenced
        return str(self.bucket_name)

class GuestFacultyBucket(models.Model):
    id = models.IntegerField(primary_key=True)
    faculty_bucket=models.ForeignKey('FacultyBucketMaster')
    #faculty_bucket=models.CharField(max_length=225,blank=True, null=True)
    guest_faculty=models.ForeignKey('GuestFaculty')
    bucket_assigned_on=models.DateField(verbose_name='Bucket Assigneddata types  date')
    class Meta:
        managed = False
        db_table = 'guest_faculty_bucket'
        verbose_name = 'Guest Faculty Bucket'
        verbose_name_plural = 'Guest Faculty Bucket'

    def __str__(self):              # Returns Name wherever referenced
        return str(self.id)




class CurrentGFSemester(models.Model):
    #current_semester_id = models.Foreignkey(Semester)
    current_semester = models.ForeignKey(Semester,primary_key=True)

    class Meta:
        managed = False
        db_table = 'current_gf_teaching_semester'
        verbose_name='CurrentGFSemester'
        verbose_name_plural = 'Current GF Teaching Semester'   


class AssessmentQuestionMaster(models.Model):
    question_id = models.AutoField(primary_key=True,editable=False)
    question_description = models.TextField('Question Name',max_length=80,blank=True)
    
    class Meta:
        managed = False
        db_table = 'assessment_question'
        verbose_name = 'Assessment Question Master'
        verbose_name_plural = 'Assessment Question Master'
    def __str__(self):              # Returns Name wherever referenced
        return str(self.question_id)	

class AssessmentMaster(models.Model):
    assessment_id = models.AutoField(primary_key=True,editable=False)
    assessment_identifier = models.CharField('Assessment Identifier',max_length=80)
    
    class Meta:
        managed = False
        db_table = 'assessment_master'
        verbose_name = 'Guest Faculty Assessment Scores Master'
        verbose_name_plural = 'Guest Faculty Assessment Scores Master'
    def __str__(self):              # Returns Name wherever referenced
        return str(self.assessment_identifier)	


class GuestFacultyAssessmentSummary(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    guest_faculty = models.ForeignKey('GuestFaculty')
    assessment_identifier = models.CharField('Assessment Identifier',max_length=50)
    #assessment_identifier = models.ForeignKey('AssessmentMaster',verbose_name='Assessment Identifier',null=True,blank=True)
    assessment_date = models.DateField('Assessment Date')
    assessment_location = models.ForeignKey('Location',verbose_name='Assessment Location',null=True,blank=True)
    overall_score = models.DecimalField('Overall Score',max_digits=10, decimal_places=2)
    normalized_score = models.DecimalField('Normalized Score',max_digits=10, decimal_places=2,null=True,blank=True)
    gf_strength = models.CharField('Overall Strengths',max_length=225,null=True,blank=True)
    gf_weaknesses = models.CharField('Overall Weaknesses',max_length=225,null=True,blank=True)
    recommendations_comments = models.CharField('Recommendations',max_length=225,null=True,blank=True)
    assessor1_name = models.CharField('1st Assessor Name',max_length=100,null=True,blank=True)
    assessor2_name = models.CharField('2nd Assessor Name',max_length=100,null=True,blank=True)
    assessor3_name = models.CharField('3rd Assessor Name',max_length=100,null=True,blank=True)
    sme1_name = models.CharField('1st SME Name',max_length=100,null=True,blank=True)
    sme2_name = models.CharField('2nd SME Name',max_length=100,null=True,blank=True)
    coordinator = models.ForeignKey('Coordinator')
    created_on = models.DateTimeField(editable=False,default=datetime.datetime.now)
    last_updated_on = models.DateTimeField(editable=False,default=datetime.datetime.now)
    last_updated_by = models.CharField(max_length=50,blank=True)

    class Meta:
        managed = False
        db_table = 'gf_assessment_summary'
	#unique_together = (('guest_faculty'),)
	unique_together = (('guest_faculty','assessment_identifier'),)
        verbose_name = 'Guest Faculty Assessment Scores'
        verbose_name_plural = 'Guest Faculty Assessment Scores'    
    def __str__(self):              # Returns Name wherever referenced
        return str(self.assessment_identifier)
    def coordinator1(self):
        return self.coordinator.coordinator
    coordinator1.admin_order_field = 'coordinator__coordinator'
    coordinator1.short_description = 'coordinator mail'	



class GuestFacultyDetailedAssessment(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    #guest_faculty_id = models.CharField(max_length=40,blank=True)
    guest_faculty = models.ForeignKey('GuestFaculty')
    assessment_identifier = models.ForeignKey(GuestFacultyAssessmentSummary,verbose_name='Assessment Identifier')
    #assessment_identifier = models.ForeignKey('AssessmentMaster',verbose_name='Assessment Identifier',null=True,blank=True)
    question = models.ForeignKey('AssessmentQuestionMaster')
    assessment_score = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    key_observations = models.CharField(max_length=225,blank=True, null=True)
    recommendations = models.CharField(max_length=225,blank=True, null=True)
    created_on = models.DateTimeField(editable=False,default=datetime.datetime.now)
    last_updated_on = models.DateTimeField(editable=False,default=datetime.datetime.now)
    last_updated_by = models.CharField(max_length=50,blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gf_assessment_details'
	#unique_together = (('guest_faculty'),)
        verbose_name = 'Guest Faculty Detailed Assessment'
        verbose_name_plural = 'Guest Faculty Detailed Assessment'

    def __str__(self):# Returns Name wherever referenced
        return str(self.id)

    def question1(self):
        return self.question.question_description
    question1.admin_order_field = 'question'
    question1.short_description = 'Question Name'

    def guestfacultyassessmentsummary_assessment_date(self):
        return self.assessment_identifier.assessment_date
    guestfacultyassessmentsummary_assessment_date.admin_order_field = 'assessment_identifier__assessment_date'
    guestfacultyassessmentsummary_assessment_date.short_description = 'Assessment Date'
    def guestfacultyassessmentsummary_coordinator(self):
        return self.assessment_identifier.coordinator
    guestfacultyassessmentsummary_coordinator.admin_order_field = 'assessment_identifier__coordinator'
    guestfacultyassessmentsummary_coordinator.short_description = 'Coordinator'


class CategoryValueMaster(models.Model):
    value_id = models.AutoField(primary_key=True,editable=False)
    category_value = models.CharField(max_length=255,unique=True)

    class Meta:
        managed = False
        db_table = 'honorarium_category_value_master'
        verbose_name = 'Honorarium Category Value Master'
        verbose_name_plural = 'Honorarium Category Value Master' 

    def __str__(self):# Returns Name wherever referenced
        return str(self.category_value)



class CategoryNameMaster(models.Model):
    category_id = models.AutoField(primary_key=True,editable=False)
    category_name = models.CharField(max_length=225,unique=True)

    class Meta:
        managed = False
        db_table = 'honorarium_category_master'
        verbose_name = 'Honorarium Category Name Master'
        verbose_name_plural = 'Honorarium Category Name Master'

    def __str__(self): # Returns Name wherever referenced
        return str(self.category_name)



class HonorariumRateMaster(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    category = models.ForeignKey('CategoryNameMaster')
    active_flag = models.BooleanField('Active Flag',default=True)
    category1_value = models.ForeignKey(CategoryValueMaster,related_name='category1_value')
    category2_value = models.ForeignKey(CategoryValueMaster,related_name='category2_value')
    honorarium_rate = models.DecimalField('Honorariun Rate',max_digits=10, decimal_places=2,null=True,blank= True)
    honorarium_amount = models.DecimalField('Honorariun Amount',max_digits=10, decimal_places=2,null=True,blank= True)
    created_on = models.DateTimeField(editable=False,default=datetime.datetime.now)
    last_updated_on = models.DateTimeField(editable=False,default=datetime.datetime.now)
    last_updated_by = models.CharField(max_length=225,blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'honorarium_rate_master'
        unique_together = (('category','category1_value','category2_value'),)
        verbose_name = 'Honorarium Rate Master'
        verbose_name_plural = 'Honorarium Rate Master'



class AdditionalCourseOfferAttributes(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    course = models.ForeignKey('Course')
    semester = models.ForeignKey('Semester')
    program = models.ForeignKey('Program',blank=True,null=True)
    guest_faculty = models.ForeignKey('GuestFaculty',verbose_name='GF ID')
    course_type = models.CharField('Course Type',max_length=225,choices=FIELD_LIST)
    mid_sem_weightage = models.DecimalField('Mid Sem Weightage',max_digits=10, decimal_places=2,)
    compre_weightage = models.DecimalField('Compre Weightage',max_digits=10, decimal_places=2,)
    assignment_weightage = models.DecimalField('Assignment Weightage',max_digits=10, decimal_places=2,)
    number_of_students = models.IntegerField('Number of Students attending lectures',max_length=11,)
    number_of_lectures = models.IntegerField('Number of Lectures taken',max_length=11,)
    faculty_role = models.ForeignKey('CategoryValueMaster', related_name = 'Faculty Role Played +')
    mid_sem_evaluated_flag = models.BooleanField('Midsem evaluation done')
    assignment_evaluated_flag = models.BooleanField('Assignment Evaluation Done')
    compre_evaluated_flag = models.BooleanField('Compre Exam evaluation done')
    qp_work_done = models.ForeignKey('CategoryValueMaster',verbose_name='Question paper setting work role',)
    course_location_section_detail = models.CharField('Course Location And Semester Type', max_length=225,choices=FIELD_LIST1)
    mid_sem_exam_students_count = models.IntegerField('Number of Students taking Mid Sem',max_length=11,blank =True,default = 0)
    dissertation_role = models.ForeignKey('CategoryValueMaster', related_name = 'Dissertation Role Played+')
    dissertation_students_count = models.IntegerField('Number of students taking dissertation',max_length=11,default = 0)
    assignment_student_count = models.IntegerField('Number of students doing assignments',max_length=11,blank = True,default = 0)
    compre_exams_students_count = models.IntegerField('Number of Students taking Compre',max_length=11,blank = True,default = 0)
    honorarium_calculated_flag = models.BooleanField('Honorarium Calculated Flag',default=False,)
    last_updated_on_datetime = models.DateTimeField('Last updated date time',editable=False,default=datetime.datetime.now)
    created_on_datetime = models.DateTimeField('Created Date Time',editable=False,default=datetime.datetime.now)
    last_updated_by = models.CharField('Last updated by',max_length=225,)
    
   
    class Meta:
        managed = False
        db_table = 'additional_course_offer_attributes'
        unique_together = (('guest_faculty','course','semester','program'),)
        verbose_name = 'Guest Faculty Honorarium Input Data'
        verbose_name_plural = 'Guest Faculty Honorarium Input Data'
   
 
    def faculty(self):
        return self.faculty_role
    faculty.short_description = 'Faculty Role Played'

    def dissertation1(self):
        return self.dissertation_role.category_value
    dissertation1.short_description = 'Dissertation Role Played'

    def createddatetime(self):
        return self.created_on_datetime
    createddatetime.admin_order_field = 'created_on_datetime'
    createddatetime.short_description = 'Data Uploaded on' 

#class RenameField(AdditionalCourseOfferAttributes, dissertation_role, Dissertation Role Played)

   

     


class GuestFacultyHonorarium(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    course = models.ForeignKey('Course')
    semester = models.ForeignKey('Semester')
    program = models.ForeignKey('Program')
    guest_faculty = models.ForeignKey(GuestFaculty)
    lecture_rate_used = models.DecimalField('Lecture Rate Used',max_digits=10, decimal_places=2,null=True,blank=True)
    lecture_honorarium = models.DecimalField('Lecture Honorarium',max_digits=10, decimal_places=2,null=True,blank=True)
    mid_sem_qp_rate_used = models.DecimalField('Mid Sem Qp Rate Used',max_digits=10, decimal_places=2,null=True,blank=True)
    compre_qp_rate_used = models.DecimalField('Compre Qp Rate Used',max_digits=10, decimal_places=2,null=True,blank=True)
    qp_honorarium = models.CharField(max_length=225,blank=True,null=True)
    mid_sem_eval_rate_used = models.DecimalField('Mid Sem Eval Rate Used',max_digits=10, decimal_places=2,null=True,blank=True)
    compre_eval_rate_used = models.DecimalField('Compre Eval Rate Used',max_digits=10, decimal_places=2,null=True,blank=True)
    assignment_eval_rate_used = models.DecimalField('Assignment Eval Rate Used',max_digits=10, decimal_places=2,null=True,blank=True)
    evaluation_honorarium = models.DecimalField('Evaluation Honorarium',max_digits=10, decimal_places=2,null=True,blank=True)
    dissertation_rate_used = models.DecimalField('Dissertation Rate Used',max_digits=10, decimal_places=2,null=True,blank=True)
    dissertation_honorarium = models.DecimalField('Dissertation Honorarium',max_digits=10, decimal_places=2,null=True,blank=True)
    course_type_section_location_honorarium = models.DecimalField('Course Type Section Location',max_digits=10, decimal_places=2,null=True,blank=True)
    manualy_calculated_flag = models.BooleanField('Manually Calculated Flag',default=True)
    course_type_rate_used = models.DecimalField('Course Type Rate Used',max_digits=10, decimal_places=2,null=True,blank=True)
    total_honorarium = models.DecimalField('Total Honorarium',max_digits=10, decimal_places=2,null=True,blank=True)
    created_on_datetime = models.DateTimeField('Created Date Time',editable=False,default=datetime.datetime.now)
    last_updated_datetime = models.DateTimeField('Last updated date time',editable=False,default=datetime.datetime.now)
    last_updated_by = models.CharField('Last updated by',max_length=225,)
    additional_teaching_honorarium = models.DecimalField('Additional Teaching Honorarium',max_digits=10, decimal_places=2,null=True,blank=True)

    class Meta:
        managed = False
        db_table = 'guest_faculty_honorarium'
        verbose_name = 'Guest Faculty Honorarium Amounts'
        verbose_name_plural = 'Guest Faculty Honorarium Amounts' 
    #admin order field for sorting the display field

    def __str__(self): # Returns lecture_rate_used wherever referenced
        return str(self.lecture_rate_used)

    def course1(self):
        return self.course.course_name
    course1.admin_order_field = 'course__course_id'
    course1.short_description = 'Course'

    def semester1(self):
        return self.semester.semester_name
    semester1.admin_order_field = 'semester__semester_id'
    semester1.short_description = 'Semester'

    def guestfaculty1(self):
        return self.guest_faculty.name
    guestfaculty1.admin_order_field = 'guest_faculty__guest_faculty_id'
    guestfaculty1.short_description = 'Guest Faculty'

    def honorarium1(self):
        return self.last_updated_datetime
    honorarium1.admin_order_field = 'last_updated_datetime'
    honorarium1.short_description = 'Honorarium calculated on'

    def lecture1(self):
        return self.lecture_honorarium	
    lecture1.admin_order_field = 'lecture_honorarium'
    lecture1.short_description = 'Lecture Honorarium Amount'

    def qphonorarium1(self):
        return self.qp_honorarium
    qphonorarium1.admin_order_field = 'qp_honorarium'
    qphonorarium1.short_description = 'QP honorarium Amount'

    def evaluationhonorarium1(self):
        return self.evaluation_honorarium
    evaluationhonorarium1.admin_order_field = 'evaluation_honorarium'
    evaluationhonorarium1.short_description = 'Evaluation Honorarium Amount'

    def dissertationhonorarium1(self):
        return self.dissertation_honorarium 
    dissertationhonorarium1.admin_order_field = 'dissertation_honorarium'
    dissertationhonorarium1.short_description = 'Dissertation Honorarium Amount'

    def teachinghonorarium1(self):
        return self.additional_teaching_honorarium
    teachinghonorarium1.admin_order_field = 'additional_teaching_honorarium'
    teachinghonorarium1.short_description = 'Additional Teaching Honorarium Amount'

    def totalhonorarium1(self):
        return self.total_honorarium
    totalhonorarium1.admin_order_field = 'total_honorarium'
    totalhonorarium1.short_description = 'Total Honorarium Amount'  


class HonorariumFieldKeyWords(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    key_value = models.ForeignKey('CategoryNameMaster')
    field_name = models.CharField(max_length=225,choices=FIELD_NAMES,unique=True)

    class Meta:
        managed = False
        db_table = 'honorarium_field_key_words'
        verbose_name = 'Honorarium Field Key Words'
        verbose_name_plural = 'Honorarium Field Key Words'


class GuestFacultyDiscipline(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    qualification_id = models.IntegerField(max_length=11)
    name = models.CharField(max_length = 200)
    degree_id = models.IntegerField(max_length=11)
    qualification_discipline_id = models.IntegerField(max_length=11)
    guest_faculty_id = models.CharField('Guest Faculty',max_length = 20)
    current_location_id = models.IntegerField(max_length = 11)
   # discipline_id = models.IntegerField(max_length = 11)
    areas_of_expertise = models.CharField(max_length=1000, null=True) 
    courses_can_handle = models.CharField(max_length=1000,  null=True)
    location_name = models.CharField(max_length = 45,verbose_name ='Location')
    degree_full_name = models.CharField(max_length = 200,verbose_name = 'Degree name')
    discipline_long_name = models.CharField('Discipline Interested In',max_length = 200)
    qualification_name = models.CharField(max_length = 45,verbose_name = 'Qualification Discipline')
  
    class Meta:
        managed = False
        db_table = 'gfdegreediscipline'
      #  unique_together = (('guest_faculty_id','discipline_long_name','areas_of_expertise','courses_can_handle'),)
        verbose_name = 'Guest Faculty By Degree And Discipline'
        verbose_name_plural = 'Guest Faculty By Degree And Discipline'  
  #     ordering = ('guest_faculty_id',)
 
    def __str__(self):              # Returns Name of Location wherever referenced
        return ""	


class GuestFacultyInterview(models.Model):
    application_id = models.AutoField(primary_key=True, editable=False)
    application_number = models.CharField(max_length=200, blank=True, null=True,verbose_name = 'Candidate Id')
    name = models.CharField(max_length = 200,verbose_name = 'Name')
    current_location_id = models.IntegerField(max_length = 11)
    evaluation_venue = models.CharField(max_length=200, blank=True, null=True, default='ONLINE',verbose_name = 'Interview Venue')
    evaluation_time_slot = models.CharField(max_length=45, blank=True, null=True,verbose_name = 'Interview time')
    evaluator_names_list = models.CharField(max_length=200,editable=False,verbose_name = 'Interview panel')
    interview_venue_conformed = models.BooleanField(default = 0,verbose_name = 'Accepted')
    evaluation_result = models.CharField(max_length=45, blank=True, null=True,verbose_name = 'Interview Result')
    assessment_score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,verbose_name = 'Interview Score')
    location_id = models.IntegerField(max_length=11)
    location_name = models.CharField(max_length = 45,verbose_name ='Location Name')
   
    class Meta:
        managed = False
        db_table = 'gfinterview'
        verbose_name = 'Guest Faculty Candidate Interview Schedule'
        verbose_name = 'Guest Faculty Candidate Interview Schedule'

    def __str__(self):
        return ""	




        


