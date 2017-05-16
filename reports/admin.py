from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django import forms
from django.forms import TextInput, ModelForm, Textarea, Select
from django.db import models
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
import datetime
from django.core.mail import send_mail
from django.template import Context
from django.db.models import Q, F
from django.contrib.admin.helpers import ActionForm
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.conf import settings
from django.template.loader import render_to_string
from django.db import Error

from import_export import resources
#from import_export.admin import ExportActionModelAdmin
#from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportMixin, ImportMixin, ImportExportMixin
from import_export import fields,widgets
from import_export.widgets import ForeignKeyWidget, BooleanWidget

#from django_object_actions import DjangoObjectActions
from django_object_actions import (DjangoObjectActions, takes_instance_or_queryset)
#from django_object_actions import BaseDjangoObjectActions
from django_object_actions import (BaseDjangoObjectActions, takes_instance_or_queryset)

from django.contrib.admin import RelatedFieldListFilter

from django.contrib.admin import AdminSite

from django.db.models import Sum, Avg, Count, Min, Max


from .models import GFCandidateListReport, GFCandidateCountReport, GuestFacultyActivityReport, GuestFacultyListReport, GuestFacultyQualificationReport, GuestFacultyAttendanceReport, SemesterPlanDetailReport, PlanningWindowStatusReport, SemesterTimetableEditWindowReport,SemesterMilestonePlanMasterReport,GuestFacultyDegreeDisciplineReport,GuestFacultyInterviewReport
from admin_report.mixins import ChartReportAdmin
from timetable.models import SemesterMilestone,SemesterMilestonePlanMaster,SemesterTimetableEditWindow
from facultyapp.models import Course,Program,Semester,GuestFaculty,Location,User,Degree,Qualification,Discipline
from django.conf.urls import url

class AdminNoAddPermissionMixin(object):
    def has_add_permission(self, request):
        return False
class GFResource(resources.ModelResource):
    current_location = fields.Field(column_name=' current_location ',attribute='current_location', widget=ForeignKeyWidget(Location, 'location_name'))
    by_user = fields.Field(column_name='by_user',attribute='by_user',widget=ForeignKeyWidget(User,'username'))
    class Meta:
        model = GFCandidateListReport
        fields = ('application_id','application_number','pan_number','name','gender','date_of_birth','email','total_experience_in_months','phone','mobile','address1','	teach_experience_in_months','current_organization','current_org_designation','months_in_curr_org','current_location','application_status','reapplication','received_status','application_ack_sent','application_submission_date','applying_for_discipline','uploaded_cv_file_name','industry_exp_in_month','nature_of_current_job','areas_of_expertise','certifications','awards_and_distinctions','publications','by_user')

class ReportGFCandidateAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
   
    resource_class = GFResource
    list_display = ('application_number','name','application_status','application_submission_date','current_location_id')	
    list_filter = ('application_status','application_submission_date','applying_for_discipline',('current_location',admin.RelatedOnlyFieldListFilter))	

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Candidate List'}
        return super(ReportGFCandidateAdmin, self).changelist_view(request, extra_context=extra_context)
		
admin.site.register(GFCandidateListReport, ReportGFCandidateAdmin)


class ReportGFCandidateCountAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
   
    list_display = ('applying_for_discipline','show_application_count')	
    list_filter = ('applying_for_discipline',)
    #report_annotates = (('application_id', Count, "mycount"),('application_id', Sum, "mysum"))
    #report_aggregates = (('application_id', Count, "mycount"),('application_id', Sum, "mysum"))
    group_by = ('applying_for_discipline_id',)
    def get_queryset(self, request):
        qs = super(ReportGFCandidateCountAdmin, self).get_queryset(request)
        return qs.values('applying_for_discipline_id').annotate(application_count=Count('name')).order_by('application_count')
        #return []
        #return GFCandidateCountReport.objects.values('applying_for_discipline_id').annotate(application_count=Count('application_id')).order_by()
    def show_application_count(self, obj):
        return obj.application_count
    show_application_count.short_description = 'Application Count'
    #show_application_count.admin_order_field = 'application_count'

#admin.site.register(GFCandidateCountReport, ReportGFCandidateCountAdmin)
class GfResource(resources.ModelResource):
    current_location = fields.Field(column_name=' current_location ',attribute='current_location', widget=ForeignKeyWidget(Location, 'location_name'))
    recruitment_location = fields.Field(column_name='recruitment_location',attribute='recruitment_location', widget=ForeignKeyWidget(Location, 'location_name'))
    

    class Meta:
        model = GuestFacultyListReport
        fields = ('id','pan_number','guest_faculty_id','name','gender','date_of_birth','email','total_experience_in_months','phone','mobile','address1','teach_experience_in_months','current_organization','current_org_designation','months_in_curr_org','recruited_on_date','current_location','last_updated_date','inserted_date','updated_by','confidentiality_requested','uploaded_cv_file_name','recruitment_location','payment_bank_name','bank_account_number','ifsc_code','bank_address','account_type','beneficiary_name','industry_exp_in_months','nature_of_current_job','certifications','awards_and_distinctions','publications','membership_of_prof_bodies','courses_taught','areas_of_expertise','taught_in_institutions','industry_projects_done','past_organizations')
        
class ReportGuestFacultyListAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
   
    resource_class = GfResource
    list_display = ('guest_faculty_id','name','pan_number','recruitment_location','recruited_on_date', 'current_organization')	
    list_filter = ('recruited_on_date','current_organization',('recruitment_location',admin.RelatedOnlyFieldListFilter))

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Listing With Current Affiliation'}
        return super(ReportGuestFacultyListAdmin, self).changelist_view(request, extra_context=extra_context)
		
admin.site.register(GuestFacultyListReport, ReportGuestFacultyListAdmin)

class GuestFacultyResource(resources.ModelResource):
    guest_faculty = fields.Field(column_name='guest_faculty', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'guest_faculty_id'))
    degree = fields.Field(column_name='degree', attribute='degree', widget=ForeignKeyWidget(Degree, 'degree_full_name'))
    qualification = fields.Field(column_name='qualification', attribute='qualification', widget=ForeignKeyWidget(Qualification, 'qualification_name'))
    qualification_discipline = fields.Field(column_name='qualification_discipline', attribute='qualification_discipline', widget=ForeignKeyWidget(Discipline, 'discipline_long_name'))    

    class Meta:
        model = GuestFacultyQualificationReport
        fields = ('qualification','degree','qualification_discipline','guest_faculty','guest_faculty_pan_number','college','year_of_completion','completed','highest_qualification','percent_marks_cpi_cgpa','max_marks_cpi_cgpa','inserted_date','normalized_marks_cpi_cgpa')
    
      

     
class ReportGuestFacultyQualificationAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
   
    resource_class = GuestFacultyResource
    list_display = ('guest_faculty','qualification','degree','qualification_discipline','year_of_completion','completed','highest_qualification','normalized_marks_cpi_cgpa')	
    list_filter = ('qualification','degree','qualification_discipline')

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Listing With Qualification'}
        return super(ReportGuestFacultyQualificationAdmin, self).changelist_view(request, extra_context=extra_context)
		
admin.site.register(GuestFacultyQualificationReport, ReportGuestFacultyQualificationAdmin)
class GFCOResource(resources.ModelResource):

    course = fields.Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    location = fields.Field(column_name='location', attribute='location', widget=ForeignKeyWidget(Location, 'location_name'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'program_name'))
    guest_faculty = fields.Field(column_name='guest_faculty', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'guest_faculty_id'))
    #delete = fields.Field(widget=widgets.BooleanWidget())
	
    class Meta:
        model = GuestFacultyActivityReport
        fields = ('course','location','semester','program','guest_faculty','course_offer_status','sequence_number','program_coordinator','offer_to_faculty_date','number_students_in_class','section','honorarium_given','honorarium_text','hon_issued_on_date','hon_issued_by','assessment_score','feedback')

class ReportGuestFacultyActivityAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
   
    resource_class = GFCOResource
    list_display = ('guest_faculty','course','semester','program','location')	
    list_filter = ('semester','program',('location',admin.RelatedOnlyFieldListFilter),'course__course_name')	
	
    def get_queryset(self, request):
        qs = super(ReportGuestFacultyActivityAdmin, self).get_queryset(request) 
        return qs.filter(course_offer_status="Accepted")

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Listing With Teaching Activity'}
        return super(ReportGuestFacultyActivityAdmin, self).changelist_view(request, extra_context=extra_context)	
		
admin.site.register(GuestFacultyActivityReport, ReportGuestFacultyActivityAdmin)
class FacultyClassAttendanceResource(resources.ModelResource):

    #course = fields.Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'program_name'))
    guest_faculty = fields.Field(column_name='guest_faculty', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'name'))
    class Meta:
        model = GuestFacultyAttendanceReport
        fields = ('id','course','semester','program','guest_faculty','class_date','class_time_slot','absent','comments_for_absence','insert_datetime','update_datetime')
class ReportGuestFacultyAttendanceAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
   
    resource_class = FacultyClassAttendanceResource
    #change_list_template = 'admin/reports/change_list.html'
    #program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'program_name'))
    list_display = ('guest_faculty','course','semester','program','class_date','class_time_slot','absent')	
    list_filter = ('class_date','semester','program','course__course_name')

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Attendance'}
        return super(ReportGuestFacultyAttendanceAdmin, self).changelist_view(request, extra_context=extra_context)	
 
	
#admin.site.register(GuestFacultyAttendanceReport, ReportGuestFacultyAttendanceAdmin)

class ReportSemesterPlanDetailAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    template = "change_list.html"
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
   
    list_display = ('semester_milestone_plan_master','semester_milestone','event_date','semestermilestoneplanmaster_program','semestermilestoneplanmaster_discipline','semestermilestoneplanmaster_batch','semestermilestoneplanmaster_location','semestermilestoneplanmaster_client_organization','semestermilestoneplanmaster_student_strength','semestermilestoneplanmaster_milestone_plan_owner','semestermilestoneplanmaster_secondary_owner',)	
    list_filter = ('semester_milestone',)
    #list_display_links = ('semestermilestoneplanmaster_location',)
    #list_display_links = ('semester_milestone_plan_master',)

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': ' New Milestone  Plan Report'}
        return super(ReportSemesterPlanDetailAdmin, self).changelist_view(request, extra_context=extra_context)
		
admin.site.register(SemesterPlanDetailReport, ReportSemesterPlanDetailAdmin)

class ReportPlanningWindowStatusAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
   
    list_display = ('semester','program','status','start_date','end_date')   
    list_filter = ('semester','program','status')	

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'PlanningWindow'}
        return super(ReportPlanningWindowStatusAdmin, self).changelist_view(request, extra_context=extra_context)
		
admin.site.register(PlanningWindowStatusReport, ReportPlanningWindowStatusAdmin)

class EditWindowResource(resources.ModelResource):

    #course = fields.Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    location = fields.Field(column_name='location', attribute='location', widget=ForeignKeyWidget(Location, 'location_name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'program_name'))
    class Meta:
        model = SemesterTimetableEditWindow
        fields = ('id','semester','location','program','timetable_owner','status','last_updated_on','last_updated_by','dealine_creation_date','daeadline_submission_date','deadline_approval_date','exam_date','days_before_exam',)

class ReportSemesterTimetableEditWindowAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
    resource_class = EditWindowResource
    list_display = ('semester_id','status','program','location','timetable_owner','dealine_creation_date','daeadline_submission_date','deadline_approval_date')  
    list_filter = ('semester_id','status','program','location')	

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'SemesterTimetableEditWindow'}
        return super(ReportSemesterTimetableEditWindowAdmin, self).changelist_view(request, extra_context=extra_context)
		
admin.site.register(SemesterTimetableEditWindowReport, ReportSemesterTimetableEditWindowAdmin)

class GFDegreeAndDisciplineResource(resources.ModelResource):
    guest_faculty = fields.Field(column_name='guest_faculty', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'guest_faculty_id'))
    class Meta:
        model = GuestFacultyDegreeDisciplineReport
        fields = ('guest_faculty_id','areas_of_expertise')

class ReportGuestFacultyDegreeDisciplineAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
    resource_class = GFDegreeAndDisciplineResource
    list_display = ('guest_faculty_id','areas_of_expertise')
#    list_filter = ('guest_faculty',) 

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty By Degree And Discipline'}
        return super(ReportGuestFacultyDegreeDisciplineAdmin, self).changelist_view(request, extra_context=extra_context)         
   
admin.site.register(GuestFacultyDegreeDisciplineReport, ReportGuestFacultyDegreeDisciplineAdmin)


class GFInterview(resources.ModelResource):
    class Meta:
        model = GuestFacultyInterviewReport
        fields = ('application_number','name','current_location_id','location_name','evaluation_venue','evaluation_time_slot','evaluator_names_list','interview_venue_conformed','evaluation_result','assessment_score',)


class ReportGuestFacultyInterviewAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    class Media:
       static_url = getattr(settings, 'STATIC_URL', '/static/')
       js = [ static_url+'admin/js/list_filter_collaps.js', ]
    model = GuestFacultyInterviewReport
    resource_class = GFInterview
    list_display = ('application_number','name','location_name','evaluation_venue','evaluation_time_slot','evaluator_names_list','interview_venue_conformed','evaluation_result','assessment_score')
    list_filter = ('name','location_name')


admin.site.register(GuestFacultyInterviewReport,ReportGuestFacultyInterviewAdmin)    

