from __future__ import unicode_literals

from django.db import models
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import Group 
from facultyapp.models import Coordinator, Course, Discipline, Location, Program, Semester

STATUS_LIST = (
    ('Open', 'Open'),
    ('Closed', 'Closed'),
)
ROLE_LIST = (
    ('Location Cordinator', 'Location Cordinator'),
    ('Program Cordinator', 'Program Cordinator'),
)
NAME_LIST = (
    ('GFLAN'),
)
class BufferType(models.Model):
    buffer_calc_id = models.AutoField('ID',primary_key=True,editable=False)
    buffer_percentage = models.DecimalField('Percentage',max_digits=10, decimal_places=2)
    buffer_name = models.CharField('Name',max_length=20)

    class Meta:
        managed = False
        db_table = 'buffer_type'

    def __str__(self):              # Returns Name wherever referenced
        return self.buffer_name
		
class GuestFacultyPlanningNumbers(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    program_coordinator = models.ForeignKey(Coordinator,null=True)
    location = models.ForeignKey(Location)
    course = models.ForeignKey(Course)
    program = models.ForeignKey(Program)
    semester = models.ForeignKey(Semester)
    discipline = models.ForeignKey(Discipline)
    version_number = models.IntegerField('Version')
    buffer_type = models.ForeignKey(BufferType)
    current_plan_flag = models.BooleanField('Current')
    plan_status = models.CharField('Status',max_length=15)
    total_faculty_required = models.IntegerField('Faculty Reqd')
    faculty_in_database = models.IntegerField('Faculty in DB')
    faculty_to_be_recruited = models.IntegerField('To Recruit',blank=True, null=True)
    buffer_number = models.IntegerField('Buffer',blank=True, null=True)
    to_be_recruited_with_buffer = models.IntegerField('Recruit with Buffer',blank=True, null=True)
    planning_comments = models.CharField(max_length=2000, blank=True, null=True)
    created_by = models.ForeignKey(User,related_name='+')
    created_on = models.DateTimeField()
    last_updated_on = models.DateTimeField(blank=True, null=True,default=datetime.datetime.now)
    updated_by = models.ForeignKey(User,related_name='+',blank=True, null=True)	
    approver_comments = models.CharField(max_length=2000,blank=True, null=True)
    approved_rejected_by = models.ForeignKey(User,related_name='+',blank=True, null=True)	
    approved_rejected_on = models.DateTimeField(blank=True, null=True)
	
    class Meta:
        managed = False
        db_table = 'guest_faculty_planning_numbers'
        unique_together = (('program_coordinator', 'location', 'course', 'program', 'semester', 'discipline', 'version_number'),)
        verbose_name = 'Forecast Plan'
        verbose_name_plural = 'Forecast Plans'

    def __str__(self):              # Returns Name wherever referenced
        return str(self.id)

class PlanningWindowStatus(models.Model):
    planning_id = models.AutoField(primary_key=True,editable=False)
    semester = models.ForeignKey(Semester)
    program = models.ForeignKey(Program)
    status = models.CharField(max_length=15, choices=STATUS_LIST)
    start_date = models.DateField(blank=True, null=True,editable=True)
    end_date = models.DateField(blank=True, null=True,editable=True)
    updated_by = models.ForeignKey(User,limit_choices_to={'is_staff': True})
    last_updated_date = models.DateTimeField('Last Updated',editable=False,default=datetime.datetime.now)

    class Meta:
        managed = False
        db_table = 'planning_window_status'
        unique_together = (('planning_id', 'semester', 'program'),)		
        verbose_name = 'Plan Window'
        verbose_name_plural = 'Plan Window'
		
    def __str__(self):              # Returns Name wherever referenced
        return str(self.planning_id)
		
class ApplicationUsers(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    application_name = models.CharField(max_length=50, default='GF PLANNING APP')
    user = models.CharField(max_length=200, null=False)
    role_name = models.CharField(max_length=20, choices=ROLE_LIST)
    role_parameters = models.CharField(max_length=200)
    created_on = models.DateTimeField()
    created_by =  models.CharField(max_length=50)
    last_updated_on = models.DateTimeField()
    last_updated_by = models.CharField(max_length=50)
    
    class Meta:
        managed = False
        db_table = 'application_users'
        verbose_name = 'Application Users'
        verbose_name_plural = 'Application Users'
        #abstract = True
		
    def __unicode__(self):              
        return self.user
class CurrentSemester(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    currentsemester = models.ForeignKey(Semester,null=True, on_delete=models.SET_NULL)
    created_on_date = models.DateTimeField(editable=True,default=datetime.datetime.now)
    def delete(self):
        super(CurrentSemester, self).delete() # Call the "real" save() method.
    
    class Meta:
        managed = False
        db_table = 'current_semester'
        verbose_name = 'Current Semester'
        verbose_name_plural = 'Current Semester'
		
    def __str__(self):             
        return str(self.currentsemester)


class DesignationResource(models.Model):
    id = models.AutoField(primary_key=True,editable=False)
    name = models.CharField(max_length=225,)
  
    class Meta:
        managed = False
        db_table = 'design_resource'
        verbose_name = 'resource '
        verbose_name_plural ='Resource example'


class Designation(models.Model):
    d_id = models.AutoField(primary_key=True,editable=False)
    name = models.CharField(max_length=225,)
    company_name=models.CharField(max_length=225,)
    role= models.CharField(max_length=225,)
    
    class Meta:
        managed =False
        db_table='gfdesignation'
        verbose_name='Designation example'
        verbose_name_plural='gfplan designation example'
    
    def __str__(self):
        return str(self.role)




class GfPlanExample(models.Model):
    id=models.AutoField(primary_key=True,editable = False)
    name = models.CharField(max_length = 225,)
    mobilenum = models.CharField( max_length =225,)
    email=models.CharField(max_length = 225)
    location = models.CharField(max_length = 225)
    designation=models.ForeignKey('Designation',)

    class Meta:
        managed=False
        db_table='gfplanexample'
        verbose_name='example list'
        verbose_name_plural= 'Exapmple list details'
     
    def __str__(self):
        return str(self.name)
















