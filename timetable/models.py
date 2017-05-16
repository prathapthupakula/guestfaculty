from django.db import models
from django.contrib.auth.models import User
import datetime
from facultyapp.models import Semester
from facultyapp.models import Program
from facultyapp.models import Location
from facultyapp.models import Degree
from facultyapp.models import Discipline
from facultyapp.models import Coordinator
from django.utils.translation import gettext as _
from django import forms



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
    ('Diss', 'Diss'),
    ('DTVC', 'DTVC'),
    ('Class Room','Class Room'),
    ('Class Room With Tandberg','Class Room With Tandberg'),
    ('DTVC/Interaction','DTVC/Interaction'),
    ('Dissertation','Dissertation'),
    ('Polycom/Class Room','Polycom/Class Room'),
    ('Technology bassed','Technology based'),
    ('Class Room (Diss)','Class Room (Diss)'),
    ('Class Room/flipped','Class Room/flipped'),
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
        ordering = ('batch_name',)
        managed = False
        db_table = 'batch'
        verbose_name = 'Batch'
        verbose_name_plural = 'Batches'
		
    def __str__(self):              # Returns Name wherever referenced
        return self.batch_name	
class Organization(models.Model):
    organization_id = models.AutoField(primary_key=True, editable=False)
    organization_name = models.CharField(max_length=100)
    organization_long_name = models.CharField(max_length=200)
    association_duration_in_months = models.IntegerField()	
    start_year = models.IntegerField()
 

    class Meta:
        ordering = ('organization_name',)
        managed = False
        db_table = 'organization'
		
    def __str__(self):              # Returns Name wherever referenced
        return self.organization_name	
class SemesterMilestone(models.Model):
    milestone_id = models.AutoField(primary_key=True, editable=False)
    milestone_short_name = models.CharField(max_length=45)
    milestone_long_name = models.CharField(null=True, blank=True ,max_length=200)
    milestone_type = models.CharField('Milestone Type',max_length=45)
    #milestone_type = models.TypedChoiceField(choices=OPEN_TYPES)
    #milestone_type = models.CharField(max_length=10, choices=OPEN_TYPES,default='Default')	
    is_duration_milestone = models.BooleanField(default=0)
    is_editable_by_owner = models.NullBooleanField(blank=True, null=True,default=0) 
    active = models.BooleanField()
    max_duration_in_days = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('milestone_short_name',)
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
    dealine_creation_date = models.DateField(verbose_name='deadline creation date')
    daeadline_submission_date = models.DateField(verbose_name='deadline submission date')
    deadline_approval_date = models.DateField()
    exam_date = models.DateTimeField(blank=True, null=True)
    days_before_exam = models.IntegerField(blank=True, null=True)		
   
    class Meta:
        managed = False
        db_table = 'semester_timetable_edit_window'
        unique_together = (('semester','program','location'),)
		
    def __str__(self):              # Returns Name wherever referenced
        return str(self.timetable_owner)
    def program1(self):
        return self.program.program_code
    program1.admin_order_field = 'program__program_code'
    program1.short_description = 'program code'

class SemesterMilestonePlanMaster(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    program_code1 = models.CharField(max_length=200,blank=True, null=True,verbose_name='program code')
    version_number = models.IntegerField(default=1)
    semester_plan_name = models.CharField(max_length=200,verbose_name='plan name')
    created_date = models.DateTimeField(editable=False,default=datetime.datetime.now)
    last_updated_date=models.DateTimeField(editable=False,default=datetime.datetime.now,verbose_name='last updated on')
    last_update_by= models.CharField(max_length=100)
    timetable_status = models.CharField(max_length=45, blank=True, null=True, choices=STATUS_LIST,verbose_name='current state')
    current_version_flag = models.BooleanField(default=1)
    timetable_comments = models.CharField(max_length=200,blank=True, null=True)
    location = models.ForeignKey(Location)
    degree = models.ForeignKey(Degree)
    program = models.ForeignKey(Program)
    #program = models.ForeignKey('facultyapp.program',to_field='program_code')
    semester = models.ForeignKey(Semester)
    batch = models.ForeignKey(Batch,to_field='batch_id')
    #client_organization = models.ForeignKey(Organization)
    client_organization=models.ForeignKey(Organization)
    discipline = models.ForeignKey(Discipline)
    milestone_plan_owner = models.ForeignKey(Coordinator,verbose_name='primary owner',null=True)
    #program_coordinator = models.ForeignKey(Coordinator,null=True)
    secondary_owner = models.ForeignKey(Coordinator,related_name='secondary_owner',null=True, blank=True)
    #alternate_owner= models.ForeignKey(Coordinator)
    mode_of_delivery = models.CharField(max_length=100,choices=STATUS_LIST2)
    registration_completed_in_wilp = models.BooleanField()
    student_strength = models.IntegerField()
    approved_rejected_date = models.DateTimeField('Rejected Date',editable=False,default=datetime.datetime.now)
    approved_rejected_by = models.CharField('Rejected By',max_length=100)
    approval_rejection_comments = models.CharField(max_length=200)
    escalated_on_date = models.DateTimeField(editable=False,default=datetime.datetime.now)
    escalated_by = models.CharField(max_length=200)
    escalation_comments = models.CharField(max_length=200)
    class Meta:
        managed = False
        db_table = 'semester_milestone_plan_master'
        verbose_name = 'Semester Milestone Calendar'
        verbose_name_plural = 'Semester Milestone Calendar'
        #unique_together = ('program',)

		
    def __str__(self):              # Returns Name wherever referenced
        return str(self.id)
    def program1(self):
        return self.program.program_code
    program1.admin_order_field = 'program__program_code'
    program1.short_description = 'program code'
class SemesterMilestonePlanMaster1(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    version_number = models.IntegerField(default=1)
    semester_plan_name = models.CharField(max_length=200,verbose_name='plan name')
    created_date = models.DateTimeField(editable=False,default=datetime.datetime.now)
    last_updated_date=models.DateTimeField(editable=False,default=datetime.datetime.now)
    last_update_by= models.CharField(max_length=100)
    timetable_status = models.CharField(max_length=45, blank=True, null=True, choices=STATUS_LIST,verbose_name='current state')
    current_version_flag = models.BooleanField(default=1)
    timetable_comments = models.CharField(max_length=200,blank=True, null=True)
    location = models.ForeignKey(Location)
    degree = models.ForeignKey(Degree)
    program = models.ForeignKey(Program)
    semester = models.ForeignKey(Semester)
    batch = models.ForeignKey(Batch)
    client_organization = models.ForeignKey(Organization)
    #client_organization=models.ForeignKey(Organization)
    discipline = models.ForeignKey(Discipline)
    milestone_plan_owner = models.ForeignKey(Coordinator,verbose_name='primary  owner',null=True)
    secondary_owner = models.ForeignKey(Coordinator,related_name='secondary__owner',null=True, blank=True)
    #example1 = models.ForeignKey('Example', related_name='example1')
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
        verbose_name = 'Semester Milestone Plan Master report'
        verbose_name_plural = 'Timetable and Milestones Date report'
		
    #def __str__(self):
       # return str(self.id)
    #def get_nm(self):
        #return self.semesterplandetail1.event_date

class SemesterPlanDetail(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    semester_milestone_plan_master= models.ForeignKey(SemesterMilestonePlanMaster,verbose_name='Plan id')
    version_number = models.IntegerField(default=1)
    semester_milestone = models.ForeignKey(SemesterMilestone,verbose_name='Milestone Name')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    date_editable = models.BooleanField(default=1)
    is_milestone=models.BooleanField(verbose_name='Is Duration Milestone',default=0)
    system_populated_date = models.BooleanField(default=1)
    created_by = models.CharField(max_length=45)
    created_date = models.DateField()
    milestone_comments = models.CharField(max_length=45,blank=True, null=True)
    last_updated_by = models.CharField(max_length=45)
    last_updated_date = models.DateTimeField('Last Updated',editable=False,default=datetime.datetime.now)

    class Meta:
        managed = False
        db_table = 'semester_milestone_plan_detail'
    def __str__(self):# Returns Name wherever referenced
        return str(self.semester_milestone)	
    def semestermilestoneplanmaster_semester_plan_name(self):
        return self.semester_milestone_plan_master.semester_plan_name
    semestermilestoneplanmaster_semester_plan_name.short_description = 'semester plan name'
    def semestermilestoneplanmaster_location(self):
        return self.semester_milestone_plan_master.location
    semestermilestoneplanmaster_location.short_description = 'location'
    def semestermilestoneplanmaster_program(self):
        return self.semester_milestone_plan_master.program
    semestermilestoneplanmaster_program.short_description = 'program'
    def semestermilestoneplanmaster_discipline(self):
        return self.semester_milestone_plan_master.discipline
    semestermilestoneplanmaster_discipline.short_description = 'discipline'
    def semestermilestoneplanmaster_batch(self):
        return self.semester_milestone_plan_master.batch
    semestermilestoneplanmaster_batch.short_description = 'batch'
    def semestermilestoneplanmaster_client_organization(self):
        return self.semester_milestone_plan_master.client_organization
    semestermilestoneplanmaster_client_organization.short_description = 'client organization'
    def semestermilestoneplanmaster_student_strength(self):
        return self.semester_milestone_plan_master.student_strength
    semestermilestoneplanmaster_student_strength.short_description = 'student strength'
    def semestermilestoneplanmaster_milestone_plan_owner(self):
        return self.semester_milestone_plan_master.milestone_plan_owner
    semestermilestoneplanmaster_milestone_plan_owner.short_description = 'primary owner'
    def semestermilestoneplanmaster_secondary_owner(self):
        return self.semester_milestone_plan_master.secondary_owner
    semestermilestoneplanmaster_secondary_owner.short_description = 'secondary owner'
		

class SemesterPlanDetail1(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    semester_milestone_plan_master= models.ForeignKey(SemesterMilestonePlanMaster,verbose_name='Plan id')
    version_number = models.IntegerField(default=1)
    semester_milestone = models.ForeignKey(SemesterMilestone,verbose_name='Milestone Name')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    date_editable = models.BooleanField(default=1)
    is_milestone=models.BooleanField(verbose_name='Is Duration Milestone',default=0)
    system_populated_date = models.BooleanField(default=1)
    created_by = models.CharField(max_length=45)
    created_date = models.DateField()
    milestone_comments = models.CharField(max_length=45,blank=True, null=True)
    last_updated_by = models.CharField(max_length=45)
    last_updated_date = models.DateTimeField('Last Updated',editable=False,default=datetime.datetime.now)

    class Meta:
        managed = False
        db_table = 'semester_milestone_plan_detail'
        verbose_name = 'Timetable and Milestones Date report'
        verbose_name_plural = 'Timetable and Milestones Date report'
		
    def __str__(self):# Returns Name wherever referenced
        return str(self.semester_milestone)	
    def semestermilestoneplanmaster_semester_plan_name(self):
        return self.semester_milestone_plan_master.semester_plan_name
    semestermilestoneplanmaster_semester_plan_name.short_description = 'semester plan name'
    def semestermilestoneplanmaster_location(self):
        return self.semester_milestone_plan_master.location
    semestermilestoneplanmaster_location.admin_order_field = 'semester_milestone_plan_master__location'
    semestermilestoneplanmaster_location.short_description = 'location'
    def semestermilestoneplanmaster_program(self):
        return self.semester_milestone_plan_master.program
    semestermilestoneplanmaster_program.admin_order_field = 'semester_milestone_plan_master__program'
    semestermilestoneplanmaster_program.short_description = 'program'
    def semestermilestoneplanmaster_program_code(self):
        return self.semester_milestone_plan_master.program.program_code
    semestermilestoneplanmaster_program_code.admin_order_field = 'semester_milestone_plan_master__program__program_code'
    semestermilestoneplanmaster_program_code.short_description = 'program code'
    def semestermilestoneplanmaster_discipline(self):
        return self.semester_milestone_plan_master.discipline
    semestermilestoneplanmaster_discipline.admin_order_field = 'semester_milestone_plan_master__discipline'
    semestermilestoneplanmaster_discipline.short_description = 'discipline'
    def semestermilestoneplanmaster_batch(self):
        return self.semester_milestone_plan_master.batch
    semestermilestoneplanmaster_batch.short_description = 'batch'
    def semestermilestoneplanmaster_client_organization(self):
        return self.semester_milestone_plan_master.client_organization
    semestermilestoneplanmaster_client_organization.admin_order_field = 'semester_milestone_plan_master__client_organization'
    semestermilestoneplanmaster_client_organization.short_description = 'client organization'
    def semestermilestoneplanmaster_student_strength(self):
        return self.semester_milestone_plan_master.student_strength
    semestermilestoneplanmaster_student_strength.short_description = 'student strength'
    def semestermilestoneplanmaster_milestone_plan_owner(self):
        return self.semester_milestone_plan_master.milestone_plan_owner
    semestermilestoneplanmaster_milestone_plan_owner.short_description = 'primary owner'
    def semestermilestoneplanmaster_secondary_owner(self):
        return self.semester_milestone_plan_master.secondary_owner
    semestermilestoneplanmaster_secondary_owner.short_description = 'secondary owner'

GENDER_LIST = (
    ('M','Male'),
    ('F','Female'),
)

class Employee(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    employee_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=10,unique=True)
    location = models.ForeignKey(Location)
    gender = models.CharField(max_length=10,choices=GENDER_LIST)
    address = models.TextField(max_length=500,blank=True)
    

    class Meta:
        managed = False
	db_table = 'employee'
	verbose_name_plural = 'Employee'












