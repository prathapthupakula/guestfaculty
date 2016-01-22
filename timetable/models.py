from django.db import models
from django.contrib.auth.models import User
import datetime
from facultyapp.models import Semester
from facultyapp.models import Program
from facultyapp.models import Location
from facultyapp.models import Degree
from facultyapp.models import Discipline
from facultyapp.models import Coordinator

STATUS_LIST = (
    ('Created', 'Created'),
    ('Approved', 'Approved'),
    ('In Process', 'In Process'),	
    ('Rejected', 'Rejected'),
    ('Submitted','Submitted'),
    ('Escalated','Escalated'),
    ('Escalated/In Process','Escalated/In Process')
)
STATUS_LIST1 = (
    ('Open', 'Open'),
    ('Closed', 'Closed'),
)
STATUS_LIST2= (
    ('Application', 'Application'),
    ('Site', 'Site'),
)
class Batch(models.Model):
    batch_id = models.AutoField(primary_key=True, editable=False)
    batch_name = models.CharField(max_length=45)
    admission_year = models.CharField(max_length=4)
    expected_grad_year = models.CharField(max_length=4)	
    duration = models.IntegerField()
    total_admission_strength = models.IntegerField()
    admittted_semester = models.ForeignKey(Semester)

    class Meta:
        managed = False
        db_table = 'batch'
        verbose_name = 'Batch'
        verbose_name_plural = 'Batches'
		
    def __str__(self):              # Returns Name wherever referenced
        return self.batch_name	
class Organization(models.Model):
    organization_id = models.AutoField(primary_key=True, editable=False)
    organization_name = models.CharField(max_length=100)
   #organization_long_time= models.IntegerField()
   #class_date = models.DateField()
   #organization_long_time = models.CharField(max_length=45)
    organization_long_name = models.CharField(max_length=200)
    association_duration_in_months = models.IntegerField()	
    start_year = models.IntegerField()
 

    class Meta:
        managed = False
        db_table = 'organization'
		
    def __str__(self):              # Returns Name wherever referenced
        return self.organization_name	
class SemesterMilestone(models.Model):
    milestone_id = models.AutoField(primary_key=True, editable=False)
    milestone_short_name = models.CharField(max_length=45)
    milestone_long_name = models.CharField(null=True, blank=True ,max_length=200)
    milestone_type = models.CharField('Milestone Type',max_length=45)	
    is_duration_milestone = models.BooleanField(default=1)
    is_editable_by_owner = models.NullBooleanField(blank=True, null=True,default=0) 
    active = models.BooleanField()
    max_duration_in_days = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'semester_milestone'
		
    def __str__(self):              # Returns Name wherever referenced
        return self.milestone_short_name	
class SemesterTimetableEditWindow(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    semester = models.ForeignKey(Semester)
    program = models.ForeignKey(Program)
    location = models.ForeignKey(Location)		
    timetable_owner = models.ForeignKey(Coordinator,null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_LIST1)
    last_updated_on = models.DateTimeField('Last Updated',editable=False,default=datetime.datetime.now)
    last_updated_by = models.CharField(max_length=45)
    dealine_creation_date = models.DateField()
    daeadline_submission_date = models.DateField()
    deadline_approval_date = models.DateField()
    exam_date = models.DateTimeField()
    days_before_exam = models.IntegerField()		
   
    class Meta:
        managed = False
        db_table = 'semester_timetable_edit_window'
        unique_together = (('semester','program','location'),)
		
    def __str__(self):              # Returns Name wherever referenced
        return str(self.timetable_owner)

class SemesterMilestonePlanMaster(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    version_number = models.IntegerField(default=1)
    semester_plan_name = models.CharField(max_length=45,verbose_name='plan name')
    created_date = models.DateTimeField()
    last_updated_date=models.DateTimeField(verbose_name='last updated on')
    last_update_by= models.CharField(max_length=100)
    timetable_status = models.CharField(max_length=45, blank=True, null=True, choices=STATUS_LIST,verbose_name='current state')
    current_version_flag = models.BooleanField(default=1)
    timetable_comments = models.CharField(max_length=200,blank=True, null=True)
    location = models.ForeignKey(Location)
    degree = models.ForeignKey(Degree)
    program = models.ForeignKey(Program)
    semester = models.ForeignKey(Semester)
    batch = models.ForeignKey(Batch)
    #client_organization = models.ForeignKey(Organization)
    client_organization=models.ForeignKey(Organization)
    discipline = models.ForeignKey(Discipline)
    milestone_plan_owner = models.ForeignKey(Coordinator,verbose_name='timetable owner',null=True)
    #program_coordinator = models.ForeignKey(Coordinator,null=True)
    alternate_owner = models.ForeignKey(Coordinator,related_name="alternate_owner",null=True, blank=True)
    #alternate_owner= models.ForeignKey(Coordinator)
    mode_of_delivery = models.CharField(max_length=100,choices=STATUS_LIST2)
    registration_completed_in_wilp = models.BooleanField()
    student_strength = models.IntegerField()
    approved_rejected_date = models.DateTimeField('Rejected Date')
    approved_rejected_by = models.CharField('Rejected By',max_length=100)
    approval_rejection_comments = models.CharField(max_length=200)
    escalated_on_date = models.DateTimeField()
    escalated_by = models.CharField(max_length=200)
    escalation_comments = models.CharField(max_length=200)
    class Meta:
        managed = False
        db_table = 'semester_milestone_plan_master'
		
    def __str__(self):              # Returns Name wherever referenced
        return self.semester_plan_name
class SemesterPlanDetail(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    semester_milestone_plan_master= models.ForeignKey(SemesterMilestonePlanMaster)
    version_number = models.IntegerField(default=1)
    semester_milestone = models.ForeignKey(SemesterMilestone,verbose_name='Milestone Name')
    start_date = models.DateField()
    end_date = models.DateField()
    event_date = models.DateField()
    date_editable = models.BooleanField(default=1)
    system_populated_date = models.BooleanField(default=1)
    created_by = models.CharField(max_length=45)
    created_date = models.DateField()
    milestone_comments = models.CharField(max_length=45)
    last_updated_by = models.CharField(max_length=45)
    last_updated_date = models.DateTimeField('Last Updated',editable=False,default=datetime.datetime.now)

    class Meta:
        managed = False
        db_table = 'semester_milestone_plan_detail'
		
    def __str__(self):              # Returns Name wherever referenced
        return str(self.semester_milestone)	
      
