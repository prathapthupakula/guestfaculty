from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django import forms
from django.forms import TextInput, ModelForm, Textarea, Select
from django.db import models
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
import datetime 
import tablib
from django.core.mail import send_mail
from django.template import Context
from django.db.models import Q, F
from django.contrib.admin.helpers import ActionForm
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.template.loader import render_to_string
from django.db import Error
from django.db import IntegrityError,transaction
from import_export import resources
#from import_export.admin import ExportActionModelAdmin
#from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportMixin, ImportMixin, ImportExportMixin,ImportExportModelAdmin
from import_export import fields,widgets
from import_export.widgets import ForeignKeyWidget, BooleanWidget

from django.core.exceptions import ValidationError

from django_object_actions import DjangoObjectActions

#from django_object_actions import DjangoObjectActions
from django_object_actions import (DjangoObjectActions, takes_instance_or_queryset)
#from django_object_actions import BaseDjangoObjectActions
from django_object_actions import (BaseDjangoObjectActions, takes_instance_or_queryset)

from django.contrib.admin import RelatedFieldListFilter

from django.contrib.contenttypes.models import ContentType

from django.contrib.admin import AdminSite

from admin_report.mixins import ChartReportAdmin

from .models import Location, GuestFacultyCandidate, Program, CandidateQualification, CandidateEvaluation, GuestFaculty, GuestFacultyQualification, GfInterestedInDiscipline, Course, Discipline, Semester, CourseLocationSemesterDetail, Coordinator, GuestFacultyCourseOffer, GuestFacultyHonararium, FacultyClassAttendance, FeedbackSurvey, GuestFacultyFeedbackResults, GuestFacultyScore, Degree, Qualification ,Natureofcurrentjob,FacultyBucketMaster,GuestFacultyBucket,CurrentGFSemester,AssessmentQuestionMaster,GuestFacultyAssessmentSummary,GuestFacultyDetailedAssessment,CategoryValueMaster,CategoryNameMaster,HonorariumRateMaster,HonorariumFieldKeyWords,AdditionalCourseOfferAttributes,GuestFacultyHonorarium,AssessmentMaster
#from facultyapp.models import User
from timetable.models import SemesterMilestonePlanMaster
from .forms import AssignCourseForm

from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import (
    AdminPasswordChangeForm, UserChangeForm, UserCreationForm,
)
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Max 
from django.contrib import messages

from django.forms.models import inlineformset_factory

import numpy as np

from decimal import Decimal

from datetime import date

from django.utils import timezone

from django.db import connection

from django.forms import BaseModelFormSet


from django.db.models import F





csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())

import sys
reload(sys)
sys.setdefaultencoding("ISO-8859-1")




STATUS_LIST = (
    ('Submitted', 'Submitted'),
    ('Shortlisted', 'Shortlisted'),
    ('In Process', 'In Process'),	
    ('Selected', 'Selected'),
    ('Rejected', 'Rejected'),
)
# for override the list fields and add the pan_number in __init__.py and also (auth_user table)dbfields 
UserAdmin.fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','pan_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

#UserAdmin.readonly_fields=('pan_number',)


class GFResource(resources.ModelResource):

    class Meta:
        model = GuestFacultyCandidate

class HonarariumResource(resources.ModelResource):

    class Meta:
        model = GuestFacultyHonararium

    course = fields.Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    location = fields.Field(column_name='location', attribute='location', widget=ForeignKeyWidget(Location, 'location_name'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'program_name'))
    guest_faculty = fields.Field(column_name='guest_faculty', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'guest_faculty_id'))
    program_coordinator = fields.Field(column_name='program_coordinator', attribute='program_coordinator', widget=ForeignKeyWidget(Coordinator, 'coordinator_name'))
    #delete = fields.Field(widget=widgets.BooleanWidget())
	
    class Meta:
        model = GuestFacultyCourseOffer
        fields = ('course','location','semester','program','guest_faculty','honorarium_given','honorarium_text','hon_issued_on_date','hon_issued_by','honorarium_payment_mode','course_offer_status','sequence_number','program_coordinator','number_students_in_class','offer_to_faculty_date')
        import_id_fields = ['course','location','semester','program','guest_faculty','course_offer_status',]
        #import_id_fields = ['course_id',]

    #def for_delete(self, row, instance):
    #    return self.fields['delete'].clean(row)

class ScoreResource(resources.ModelResource):

    class Meta:
        model = GuestFacultyScore

    course = fields.Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    location = fields.Field(column_name='location', attribute='location', widget=ForeignKeyWidget(Location, 'location_name'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'program_name'))
    guest_faculty = fields.Field(column_name='guest_faculty', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'guest_faculty_id'))
    program_coordinator = fields.Field(column_name='program_coordinator', attribute='program_coordinator', widget=ForeignKeyWidget(Coordinator, 'coordinator_name'))

    #delete = fields.Field(widget=widgets.BooleanWidget())
	
    class Meta:
        model = GuestFacultyCourseOffer
        fields = ('course','location','semester','program','guest_faculty','course_offer_status','sequence_number','assessment_score','feedback','program_coordinator','number_students_in_class','offer_to_faculty_date')
        import_id_fields = ['course', 'semester', 'program', 'guest_faculty', 'location','course_offer_status']

    #def for_delete(self, row, instance):
    #    return self.fields['delete'].clean(row)
class GufResource(resources.ModelResource):
    current_location = fields.Field(column_name='current_location', attribute='current_location', widget=ForeignKeyWidget(Location, 'location_name'))
    recruitment_location = fields.Field(column_name='recruitment_location', attribute='recruitment_location', widget=ForeignKeyWidget(Location, 'location_name'))
    class Meta:
        model = GuestFaculty
        fields = ('id','pan_number','guest_faculty_id','name','gender','date_of_birth','email','total_experience_in_months','phone','mobile','address1','teach_experience_in_months',
'current_organization','current_org_designation','months_in_curr_org','current_location','confidentiality_requested','uploaded_cv_file_name',
'recruitment_location','payment_bank_name','bank_account_number','ifsc_code','bank_address','account_type','beneficiary_name',
'industry_exp_in_months','nature_of_current_job','certifications','awards_and_distinctions','publications','membership_of_prof_bodies',
'courses_taught','areas_of_expertise','taught_in_institutions','industry_projects_done','past_organizations','recruited_on_date','inserted_date','updated_by',
'last_updated_date',)
        import_id_fields = ['guest_faculty_id',]
        export_order=('id','guest_faculty_id','pan_number','name','gender','date_of_birth','email','total_experience_in_months','phone','mobile','address1','current_location','recruitment_location')
		
class CLSResource(resources.ModelResource):

    location = fields.Field(column_name='location', attribute='location', widget=ForeignKeyWidget(Location, 'location_name'))
    course = fields.Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    discipline = fields.Field(column_name='discipline', attribute='discipline', widget=ForeignKeyWidget(Discipline, 'discipline_long_name'))
    class Meta:
        model = CourseLocationSemesterDetail
        fields = ('course','location','semester','discipline','max_faculty_count','number_of_students_in_class','number_of_sections')
        import_id_fields = ('semester',)
class CourseResource(resources.ModelResource):

    class Meta:
        model = Course
        fields = ('course_id','course_name','course_description','number_of_lectures','dissertation_project_work')
        import_id_fields = ['course_id',]
class UserResource(resources.ModelResource):

    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email','is_active')
        import_id_fields = ['username','id']
		

class GFCOResource(resources.ModelResource):

    location = fields.Field(column_name='location', attribute='location', widget=ForeignKeyWidget(Location, 'location_name'))
    course = fields.Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'program_code'))
    guest_faculty = fields.Field(column_name='guest_faculty', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'guest_faculty_id'))
    guest_faculty = fields.Field(column_name='guest_faculty', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'guest_faculty_id'))
    #program_coordinator = fields.Field(column_name='program_coordinator', attribute='program_coordinator', widget=ForeignKeyWidget(Coordinator, 'coordinator_name'))
    username = fields.Field(column_name='program coordinator', attribute='program_coordinator__coordinator', widget=ForeignKeyWidget(User, 'username'))
    #username = fields.Field(column_name='program coordinator', attribute='semester_milestone_plan_master__program', widget=ForeignKeyWidget(Program, 'program_name'))
    #delete = fields.Field(widget=widgets.BooleanWidget())
	
    class Meta:
        model = GuestFacultyCourseOffer
        fields = ('course','location','semester','program','guest_faculty','course_offer_status','sequence_number','offer_to_faculty_date','number_students_in_class','section','honorarium_given','honorarium_text','hon_issued_on_date','hon_issued_by','assessment_score','feedback','username',)
        import_id_fields = ['course', 'semester', 'guest_faculty','sequence_number',]
        export_order=('course','location','semester','program','guest_faculty','username','course_offer_status','sequence_number','offer_to_faculty_date','number_students_in_class','section','honorarium_given','honorarium_text','hon_issued_on_date','hon_issued_by','assessment_score','feedback',)

    # The following increments assigned_count in courselocationsemesterdetail every time a new offer is imported		
    def after_save_instance(self,instance, dry_run):
        if not dry_run:
            if instance.course_offer_status == 'Offered':	
                p = CourseLocationSemesterDetail.objects.filter(course=instance.course,location=instance.location,semester=instance.semester,program=instance.program)
                p.update(assigned_count=F('assigned_count') + 1)
		
    #def get_instance(self, instance_loader, row):
    #    return False	
class FacultyClassAttendanceResource(resources.ModelResource):

    course = fields.Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'program_name'))
    guest_faculty = fields.Field(column_name='guest_faculty', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'name'))
    absent = fields.Field(column_name='absent', attribute='absent', widget=BooleanWidget())
    delete = fields.Field(widget=widgets.BooleanWidget())

    class Meta:
        model = FacultyClassAttendance
        fields = ('course','semester','program','guest_faculty','class_date','class_time_slot','absent','comments_for_absence')
        import_id_fields = ('semester', 'course', 'program', 'guest_faculty', 'class_date', 'class_time_slot')

    #def get_instance(self, instance_loader, row):
    #    return False	

    def for_delete(self, row, instance):
        return self.fields['delete'].clean(row)

class CEResource(resources.ModelResource):

    application = fields.Field(column_name='application', attribute='application', widget=ForeignKeyWidget(GuestFacultyCandidate,'application_number'))
    delete = fields.Field(widget=widgets.BooleanWidget())
	
    class Meta:
        model = CourseLocationSemesterDetail
        fields = ('application','evaluation_type','evaluator_names_list','evaluation comments',' evaluation_date','evaluation_result','assessment_score','evaluation_seq_no','evaluation_venue','evaluation_time_slot','letter_for_evaluation_rnd_sent','evaluation_location','regret_letter_sent','selected_letter_sent')
        import_id_fields = ('application','evaluation_seq_no')

    def for_delete(self, row, instance):
        return self.fields['delete'].clean(row)	

    # The following increments sequence_number for new rows
    def after_save_instance(self,instance, dry_run):
        if not dry_run:
            if instance.evaluation_seq_no == '':	
                p = CourseLocationSemesterDetail.objects.filter(course=instance.course,location=instance.location,semester=instance.semester,program=instance.program)
                p.update(assigned_count=F('assigned_count') + 1)
		
		
# Sample Test Function to modify the display of State/County Listing in Uppercase
def upper_case_name(obj):
    return ("%s %s" % (obj.location_state, obj.location_country)).upper()
upper_case_name.short_description = 'STATE CITY'

# Function to display Application Number in Full by Concatenating PAN NUMBER, APPLICATION_ID
def full_application_number(obj):
    return ("A%s%s" % (obj.pan_number, obj.application_id)).upper()
full_application_number.short_description = 'Application Number'

# This functions is no longer being used as we are directly injecting full values in DB
def full_application_status(obj):
    if (obj.application_status == 'SUB'):
        return "Submitted"
    elif (obj.application_status == 'SLD'):
        return "Shortlisted"
    elif (obj.application_status == 'REJ'):
        return "Rejected"
    else:
        return "Submitted"
full_application_status.short_description = 'Application Status'
		
#email server functionality method		
def send_gfemail(emailid, mailtemplate,mailtitle,c):
    msg_plain = render_to_string('%s' %mailtemplate, c)
    send_mail(mailtitle, msg_plain, settings.EMAIL_HOST_USER, emailid, fail_silently=True)	
    return True


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(("This account is inactive."), code='inactive',)

class Admin(AdminSite):
    def has_permission(self,request): 
        return request.user.is_active
		
    login_form = CustomAuthenticationForm
    site_url = None
    site_header = 'Guest Faculty Application'
    site_title =  'Guest Faculty Application'
    index_title = 'Guest Faculty Application'
    index_template = 'facultyapp/index.html'
    app_index_template = 'facultyapp/index.html'
	
admin.site = Admin(name='admin')


class LocationAdmin(admin.ModelAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]

    list_filter = ['location_country','location_state']
    list_display = ('location_id','location_name','location_state','location_country')	# Field Value Modification while displaying
    list_display_links = ('location_name',)
    #list_display = ('location_id','location_name',upper_case_name)	# Field Value Modification while displaying
    #list_editable = ('location_name',)	  #Editable Grid
#    readonly_fields = ('location_id',)    # Making Read-Only. THis can also be set in the Model file
    #search_fields = ('^location_name','location_id')	#enable search bar (= for %, @ for fulltext. recommended is ^)
# search_fields = ['foreign_key__related_fieldname']	This is for foreign_key search
#    save_on_top = True
#    fields = ('location_name', 'location_state', 'location_country')

class location:
    def __init__(self,location_name):
        self.location_name=location_name
        return location.getattr(location_name)
        print location_name


    """def add_view(self, request, form_url='', extra_context=None):
        extra_context = {'title': 'Location Master'}
        return super(LocationAdmin, self).changeform_view(request, extra_context=extra_context)

    def change_view(self, request, extra_context=None):
        extra_context = {'title': 'Location Master'}
        return super(LocationAdmin, self).changeform_view(request, extra_context=extra_context)"""

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Location Master'}
        return super(LocationAdmin, self).changelist_view(request, extra_context=extra_context)


admin.site.register(Location, LocationAdmin)
#in the candidate qualification inline exist at least one record untill you get the error at click on save button    
class CandidateQualificationInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 1:
            raise forms.ValidationError('Please enter atleast one Qualification')



# Create Inline Form for Candidate Qualifications to display as Stack
class CandidateQualificationInlineForm(ModelForm):

    class Meta:
        model = CandidateQualification
        fields = ('degree_degree','college','discipline','qualification','year_of_completion','percent_marks_cpi_cgpa','highest_qualification')
        list_filter=['highest_qualification']
		
class CandidateQualificationInline(admin.TabularInline):
    model = CandidateQualification
    #readonly_fields = ('normalized_marks_cpi_cgpa',)
    list_filter=('highest_qualification',)
    form = CandidateQualificationInlineForm
    formset=CandidateQualificationInlineFormset
    extra = 1
    max_num = 5	
    verbose_name_plural = 'Candidate Qualifications'

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            #return self.readonly_fields + ('name',) # This is used for each field selectively
            return self.get_fields(request,obj=None) # This is for All fields			
        return self.readonly_fields	

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        if obj:
           max_num = 0
           return 0
        return extra
		
    def get_max_num(self, request, obj=None, **kwargs):
        max_num = 5
        if obj:
            return 0
        return max_num	
    	
class GuestFacultyCandidateAdmin(BaseDjangoObjectActions,ExportMixin,admin.ModelAdmin):
# Main Form	
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
    #js = ['list_filter_collapse.js']
    #js=['jquery.doubleScroll.js']
    site_header = 'Guest Faculty Application'
    site_title =  'Guest Faculty Application'
    site_url = None
    index_title = 'Guest Faculty Application'
    resource_class = GFResource
    
    model = GuestFacultyCandidate
    fieldsets = (
        ('Personal Details', {
            'fields': ('application_number',('name','pan_number'),('date_of_birth','gender'),('phone','mobile'),('address1','current_location'),('applying_for_discipline', 'reapplication','application_status',))
        }),
		   ('Current Experience', {
            'fields': (('current_organization','current_org_designation'),('months_in_curr_org','teach_experience_in_months'),('industry_exp_in_months','total_experience_in_months'),('nature_of_current_job','areas_of_expertise'),('certifications','awards_and_distinctions'),'publications','uploaded_cv_file_name')
        }),
    )
    list_display = ('application_number','name','application_status','application_submission_date','current_location_id',)
    radio_fields = {"gender": admin.HORIZONTAL}
    readonly_fields = ('application_id','application_number','reapplication','application_status',)
    widgets = {
            'address1': Textarea(attrs={'cols': 20, 'rows': 5}),
    }
    inlines = (CandidateQualificationInline,)
	
    list_filter = ('application_status','application_submission_date','applying_for_discipline','name',('current_location',admin.RelatedOnlyFieldListFilter))
    actions = ['update_candidate_status','interview_candidate_call','update_candidate_selection','convert_to_guestfaculty']
    objectactions = ['update_candidate_selection','update_candidate_status','interview_candidate_call','convert_to_guestfaculty',]
	
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
                           attrs={'rows': 2,
                                  'cols': 20})},
    }	

    # Provide Add permissions for registrant role only and disable all others	
    def has_add_permission(self, request, obj=None):
        if request.user.groups.filter(name__in=['registrant']).exists():
            return True
        else:
            return False	
	
    # Hide Filter for Non-Staff users	
    """def changelist_view(self, request, extra_context=None):
        if not request.user.is_staff:
            self.list_filter = tuple()
        extra_context = {'title': 'Guest Faculty Candidate List'}
        return super(GuestFacultyCandidateAdmin, self).changelist_view(request, extra_context=extra_context)"""

    # Do the following upon Saving		
    def save_model(self, request, obj, form, change): 
        if not change:
            obj.application_submission_date = datetime.datetime.today()
            obj.application_status = 'Submitted'
            obj.email = request.user.email
            
            obj.by_user = request.user
            obj.received_status = 1
            
            # The following section checks if an application has been recieved from the same email or PAN Number and mark as reapplication			
            dup_count = GuestFacultyCandidate.objects.filter(Q(email=obj.email) | Q(pan_number=obj.pan_number)).count()
            if dup_count > 0:
                obj.reapplication = 1				
            obj.save()

            # Generate Application Number and Save it			
            obj.application_number = 'A' + obj.pan_number + str(obj.application_id)   
            obj.save()
            # Pan number update in usersz
            apuser=User.objects.filter(username=request.user).update(pan_number=obj.pan_number)
          
            #print apuser
            #print apuser.pan_number
            #apan=User.objects.filter(username=request.user).values_list('pan_number',flat=True)[0]
            #print apan
            #userpan=User.objects.update(pan_number=obj.pan_number)
            
            #userpan.save()
            # Change Role to Candidate
            request.user.groups.remove(Group.objects.get(name='registrant'))
            request.user.groups.add(Group.objects.get(name='candidate'))   	

			
            # Send Email
            c = Context({'username': obj.name, 'application_url':settings.APPLICATION_URL, 'application_num':obj.application_number})			
            send_gfemail([obj.email],'welcomeemail.txt','Re: BITS Guest Faculty Application',c) 				
            #send_gfemail('welcomeemail.txt','Re: BITS Guest Faculty Application',obj)
            obj.application_ack_sent = 1
            obj.save()
    
    # This will filter and show only applications submitted by the user.	
    def get_queryset(self, request):
        qs = super(GuestFacultyCandidateAdmin, self).get_queryset(request)
        if  request.user.is_superuser:
            return qs
        elif request.user.is_staff and request.user.groups.filter(name__in=['coordinator']):
            cl = Coordinator.objects.get(coordinator=request.user)
            #pr =Program.objects.get(program_coordinator=request.user)			
            return qs.filter(current_location=cl.coordinator_for_location,)
      # get application's "owner"
        else :
            userpan=User.objects.filter(username=request.user).values_list('pan_number',flat=True)[0]
            return qs.filter(pan_number=userpan)
           
        
    # Admin MRA Actions controlled here depending on role	
    def get_actions(self, request):
        if request.user.is_superuser or request.user.is_staff and request.user.groups.filter(name='coordinator').exists():
            actions = super(GuestFacultyCandidateAdmin, self).get_actions(request)
        else:
            actions = []
        return actions

    # Single Object actions controlled here depending on role/status	
    def get_object_actions(self, request, context, **kwargs):
        objectactions = []
        obj = context['original']		
        if request.user.is_superuser or request.user.is_staff and request.user.groups.filter(name__in=['coordinator', 'chairperson']).exists():
            if obj.application_status == "Submitted":
                objectactions.extend(['update_candidate_status',])
            if obj.application_status == "In Process":
                objectactions.extend(['update_candidate_selection',])
            if obj.application_status == "Shortlisted":
                objectactions.extend(['interview_candidate_call',])
            if obj.application_status == "Selected":
                objectactions.extend(['convert_to_guestfaculty',])
        return objectactions		

    class UpdateCandidateStatusForm(forms.Form):
        status = forms.ChoiceField(choices=(('Shortlisted', 'Shortlisted'), ('Rejected', 'Rejected'),))
        comments = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': '30','rows' : '10'}))
        
    @takes_instance_or_queryset		
    def update_candidate_status(self,request,queryset):
        form = None
        if 'update' in request.POST:
            form = self.UpdateCandidateStatusForm(request.POST)
            if form.is_valid():
                status = form.cleaned_data['status']
                comments = form.cleaned_data['comments']
                count = 0
                for candidate in queryset:
                    candidate.application_status = status
                    count += 1
                    candidate.save()
                    application_id = candidate.application_id					
                    #count=queryset.update(application_status=status)
                    if status == 'Shortlisted':
                        p = CandidateEvaluation(application=candidate,evaluation_result=status,evaluation_type='Application Review',evaluator_names_list=request.user, evaluation_comments=comments, letter_for_evaluation_rnd_sent=1, evaluation_step=1)
                        p.save()					
                        template = 'shortlistedemail.txt'
                        c = Context({'username': candidate.name, 'application_url':settings.APPLICATION_URL})
                        send_gfemail([candidate.email],template,'Re: BITS Guest Faculty Application',c) 										
                    elif status == 'Rejected': 
                        p = CandidateEvaluation(application=candidate,evaluation_result=status,evaluation_type='Application Review',evaluator_names_list=request.user, evaluation_comments=comments, regret_letter_sent=1)
                        p.save()						
                        template = 'rejectedemail.txt'
                        c = Context({'username': candidate.name, 'application_url':settings.APPLICATION_URL})
                        send_gfemail([candidate.email],template,'Re: BITS Guest Faculty Application',c) 				
                plural = ''
                if count != 1:
                    plural = 's'

                self.message_user(request, "Successfully updated status of %d candidate%s." % (count, plural))
                #return HttpResponseRedirect(request.get_full_path())
                return "<script>window.history.back();</script>"
        if not form:
            form = self.UpdateCandidateStatusForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        
        data = {'candidates': queryset,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/update_candidate_status.html', data)

    update_candidate_status.label = "Shortlist/Reject Candidate"
    update_candidate_status.short_description = "Shortlist/Reject Candidate"	

    class InterviewCandidateForm(forms.Form):
        #_selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        #tag = forms.ModelChoiceField(Tag.objects)
        #status = forms.ChoiceField(STATUS_LIST)
        intdate = forms.DateField(label='Interview Date',required=True,widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
        inttime = forms.TimeField(label='Interview Time',required=True,widget=forms.TextInput(attrs=
                                {
                                    'class':'timepicker'
                                }))
        location = forms.ChoiceField(choices=[ (l.location_id, l.location_name) for l in Location.objects.all()])		
        venue = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': '30','rows' : '5'}))
        panel = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': '30','rows' : '5'}))
        comments = forms.CharField(widget=forms.Textarea(attrs={'cols': '30','rows' : '5'}))
  
    @takes_instance_or_queryset
    def interview_candidate_call(self,request,queryset):
        form = None
        if 'update' in request.POST:
            form = self.InterviewCandidateForm(request.POST)
            if form.is_valid():
                #status = form.cleaned_data['status']
                status = "In Process"				
                intdate = form.cleaned_data['intdate']
                inttime = form.cleaned_data['inttime']				
                location = form.cleaned_data['location']
                location_name = Location.objects.get(pk=location)
                venue = form.cleaned_data['venue']
                panel = form.cleaned_data['panel']				
                comments = form.cleaned_data['comments']
                count = 0
                for candidate in queryset:
                    candidate.application_status = status
                    count += 1
                    candidate.save()
                    application_id = candidate.application_id					
                    #count=queryset.update(application_status=status)
                    p = CandidateEvaluation(application=candidate,evaluation_result=status,evaluation_type='Interview',evaluation_step=2,evaluation_seq_no=2,evaluator_names_list=panel, evaluation_comments=comments,evaluation_date=intdate,evaluation_venue=venue,evaluation_time_slot=inttime,letter_for_evaluation_rnd_sent=1,evaluation_location_id=location,regret_letter_sent=0,selected_letter_sent=0)
                    p.save()
                    c = Context({'username': candidate.name, 'application_url':settings.APPLICATION_URL, 'date':intdate,'time':inttime,'location':location_name,'venue':venue})  					
                    send_gfemail([candidate.email],'interviewcallemail.txt','Re: BITS Guest Faculty Application',c) 					
                
                plural = ''
                if count != 1:
                    plural = 's'

                self.message_user(request, "Successfully sent Interview Calls of %d candidate%s." % (count, plural))
                #return HttpResponseRedirect(request.get_full_path())
                return "<script>window.history.back();</script>"		
        if not form:
            form = self.InterviewCandidateForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        
        data = {'candidates': queryset,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/interview_candidate_call.html', data)	
    
    interview_candidate_call.label = "Call for Interview"
    interview_candidate_call.short_description = "Call for Interview"

		
    class UpdateCandidateSelectionForm(forms.Form):
        #_selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        #tag = forms.ModelChoiceField(Tag.objects)
        status = forms.ChoiceField(choices=(('Selected', 'Selected'), ('Rejected', 'Rejected'),))
        comments = forms.CharField(widget=forms.Textarea(attrs={'cols': '30','rows' : '5'}))
        score = forms.DecimalField(max_digits=10, decimal_places=2,initial=5,help_text='(maximum score value = 5.0)',min_value=0.0, max_value=5.0 )
        #error_css_class = 'error'
        #required_css_class = 'required'
        
    @takes_instance_or_queryset	
    def update_candidate_selection(self,request,queryset):
        form = None
        if 'update' in request.POST:
            form = self.UpdateCandidateSelectionForm(request.POST)
            if form.is_valid():
                status = form.cleaned_data['status']
                comments = form.cleaned_data['comments']
                score = form.cleaned_data['score']
                count = 0
                for candidate in queryset:
                    candidate.application_status = status
                    count += 1
                    candidate.save()
                    application_id = candidate.application_id					

                    if status == 'Selected':
                        p = CandidateEvaluation.objects.filter(application_id=application_id,evaluation_step=2).update(evaluation_comments=comments,evaluation_result=status,selected_letter_sent=1,assessment_score=score)
                        
                        #template = 'selectedemail.txt'
                        #c = Context({'username': candidate.name, 'application_url':settings.APPLICATION_URL})
                        #send_gfemail([candidate.email],template,'Re: BITS Guest Faculty Application',c) 										
                    elif status == 'Rejected': 
                        p = CandidateEvaluation.objects.filter(application_id=application_id,evaluation_step=2).update(evaluation_comments=comments,evaluation_result=status,regret_letter_sent=1,assessment_score=score)
                        
                        template = 'rejectedemail.txt'
                        c = Context({'username': candidate.name, 'application_url':settings.APPLICATION_URL})
                        send_gfemail([candidate.email],template,'Re: BITS Guest Faculty Application',c)
                plural = ''
                if count != 1:
                    plural = 's'

                self.message_user(request, "Successfully updated status of %d candidate%s." % (count, plural))
                #return HttpResponseRedirect(request.get_full_path())
                return "<script>window.history.back();</script>"		
        if not form:
            form = self.UpdateCandidateSelectionForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
            #form = self.UpdateCandidateSelectionForm(initial={'_selected_action': (self.application_id,)})
        data = {'candidates': queryset,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/update_candidate_selection.html', data)	    
    update_candidate_selection.label = "Select/Reject After Interview"
    update_candidate_selection.short_description = "Select/Reject After Interview"

    #def shortlist_candidate(self, request, queryset):
    #    rows_updated = queryset.update(application_status='SLD')
    #    if rows_updated == 1:
    #        message_bit = "1 Candidate was"
    #    else:
    #        message_bit = "%s Candidates were" % rows_updated
    #    self.message_user(request, "%s successfully marked as Shortlisted ." % message_bit)		
    #shortlist_candidate.short_description = "Shortlist selected Candidates"

    class ConvertToGuestFacultyForm(forms.Form):
        dummy = 1
    @takes_instance_or_queryset
    def convert_to_guestfaculty(self,request,queryset):
        form = None
        if 'update' in request.POST:
            form = self.ConvertToGuestFacultyForm(request.POST)
            if form.is_valid():
                count = 0
                for candidate in queryset:
                    count += 1

                    # Get the corresponding evaluation record.                                  
                    ev = CandidateEvaluation.objects.get(application=candidate,evaluation_result='Selected')

                    gf = GuestFaculty(pan_number=candidate.pan_number,name=candidate.name,gender=candidate.gender,date_of_birth=candidate.date_of_birth,email=candidate.email,total_experience_in_months=candidate.total_experience_in_months,phone=candidate.phone,mobile=candidate.mobile,address1=candidate.address1,teach_experience_in_months=candidate.teach_experience_in_months,current_organization=candidate.current_organization,months_in_curr_org=candidate.months_in_curr_org,recruited_on_date=datetime.datetime.today(),current_location=candidate.current_location,uploaded_cv_file_name=candidate.uploaded_cv_file_name,recruitment_location=ev.evaluation_location,industry_exp_in_months=candidate.industry_exp_in_months,nature_of_current_job=candidate.nature_of_current_job,certifications=candidate.certifications,awards_and_distinctions=candidate.awards_and_distinctions,publications=candidate.publications,areas_of_expertise=candidate.areas_of_expertise,confidentiality_requested=0,updated_by=candidate.by_user.id,)

                    gf.save()
                    gf.guest_faculty_id = 'GF' + str(gf.id)
                    gf.save()

                    cqs = CandidateQualification.objects.filter(application=candidate)
                    for cq in cqs:

                        gq = GuestFacultyQualification(guest_faculty=gf,qualification=cq.qualification,degree=cq.degree_degree,qualification_discipline=cq.discipline,guest_faculty_pan_number=gf.pan_number,college=cq.college,year_of_completion=cq.year_of_completion,completed=cq.completed,highest_qualification=cq.highest_qualification,percent_marks_cpi_cgpa=cq.percent_marks_cpi_cgpa,max_marks_cpi_cgpa=cq.max_marks_cpi_cgpa,inserted_date=datetime.datetime.today(),normalized_marks_cpi_cgpa=cq.normalized_marks_cpi_cgpa)
                        gq.save()

                    #candidate.application_status = "Recruited"
                    candidate.application_status ="Selected as Guest Faculty"
                    candidate.save()

                    # modify the role so they can access only their GF details and not the application.
                    candidate.by_user.groups.remove(Group.objects.get(name='candidate'))
                    candidate.by_user.groups.add(Group.objects.get(name='guestfaculty'))

                    template = 'selectedemail.txt'
                    c = Context({'username': candidate.name, 'application_url':settings.APPLICATION_URL1})                  
                    send_gfemail([candidate.email],template,'Re: BITS Guest Faculty Application',c) 					
                
                plural = ''
                if count != 1:
                    plural = 's'
                self.message_user(request, "Successfully Converted %d candidate%s." % (count, plural))
                #return "<script>window.history.back();</script>"
                return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.ConvertToGuestFacultyForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        
        data = {'candidates': queryset,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/convert_to_guestfaculty.html', data)				
            			
    convert_to_guestfaculty.label = "Convert to Guest Faculty"
    convert_to_guestfaculty.short_description = "Convert to Guest Faculty"

admin.site.register(GuestFacultyCandidate, GuestFacultyCandidateAdmin)

class CandidateEvaluationAdmin(admin.ModelAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
    list_filter = ['evaluation_step','evaluation_type','evaluation_result']
    list_display = ('application','evaluation_type','evaluation_result','assessment_score')
    #fields = '__all__'
    #readonly_fields = '__all__',

    def has_add_permission(self, request, obj=None):
        return False	

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        for field in self.model._meta.fields:
            readonly_fields.append(field.name)
        return readonly_fields
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Candidate Evaluation'}
        return super(CandidateEvaluationAdmin, self).changelist_view(request, extra_context=extra_context)	
	

admin.site.register(CandidateEvaluation,CandidateEvaluationAdmin)
# No qualification record data you get the alert when click on save button
class GuestFacultyQualificationInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 1:
            raise forms.ValidationError('Please enter atleast one Qualification')
# No Discipline Interested record data you get the alert when click on save button
class GfInterestedInDisciplineInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 1:
            raise forms.ValidationError('Please enter atleast one Discipline Interested')


class GuestFacultyQualificationInlineForm(forms.ModelForm):
    class Meta:
        model = GuestFacultyQualification
        fields = ('degree','college','qualification_discipline','qualification','year_of_completion','percent_marks_cpi_cgpa','max_marks_cpi_cgpa','highest_qualification')


class  QualificationFilter(SimpleListFilter):
    title = 'qualification'
    parameter_name = 'qualification'

    def lookups(self, request, model_admin):
        qualification = set([s for s in Qualification.objects.all()])
        return [(s.qualification_id,s.qualification_name) for s in qualification]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(qualification__id__exact=self.value())
        else:
            return queryset

	
class GuestFacultyQualificationInline(admin.TabularInline):
    model = GuestFacultyQualification
    #form = GuestFacultyQualificationInlineForm
    formset = GuestFacultyQualificationInlineFormset
    fields = ('degree','college','qualification_discipline','qualification','year_of_completion','percent_marks_cpi_cgpa','max_marks_cpi_cgpa','highest_qualification')
    extra = 0


class GfInterestedInDisciplineInlineForm(

ModelForm):

    class Meta:
        model = GfInterestedInDiscipline
        fields = ('discipline', 'areas_of_expertise','courses_can_handle')
	
class GfInterestedInDisciplineInline(admin.TabularInline):
    model = GfInterestedInDiscipline
    form = GfInterestedInDisciplineInlineForm
    formset=GfInterestedInDisciplineInlineFormset
    extra = 0
    verbose_name_plural = 'Disciplines Interested'
# semtech used in display data based on last semester taught GF 
def semtech(obj):
    gf_offer=GuestFacultyCourseOffer.objects.filter(guest_faculty=obj.id).order_by('-id')
    if gf_offer.exists():
        for gfo in gf_offer:
            return gfo.semester
semtech.admin_order_field = 'guest_faculty_id'            
semtech.short_description = 'Last Semester taught' 



	
class GuestFacultyAdmin(DjangoObjectActions,ImportExportModelAdmin,admin.ModelAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
    resource_class = GufResource
    model = GuestFaculty
    fieldsets = (
        ('Personal Details', {
            'fields': (('guest_faculty_id','recruited_on_date','last_updated_date'),('name','pan_number'),('date_of_birth','gender'),('phone','mobile'),('address1','current_location','email',))
        }),
		   ('Experience', {
            'fields': (('current_organization','current_org_designation'),('months_in_curr_org','teach_experience_in_months'),('industry_exp_in_months','total_experience_in_months'),('nature_of_current_job','areas_of_expertise'),('certifications','awards_and_distinctions'),'publications','uploaded_cv_file_name')
        }),
		   ('Bank Details', {
            'fields': (('payment_bank_name','bank_account_number'),('ifsc_code','bank_address'),('account_type','beneficiary_name'),'confidentiality_requested')
        }),	
		   ('Additional Details', {
            'fields': (('membership_of_prof_bodies','courses_taught'),('taught_in_institutions','industry_projects_done'),'past_organizations')
        }),		
		
    )
    list_display = ('guest_faculty_id','name','current_location','inactive_flag',semtech)
    radio_fields = {"gender": admin.HORIZONTAL}
    readonly_fields = ('recruited_on_date','last_updated_date',)
    list_filter = ['last_updated_date','inactive_flag',('current_location',admin.RelatedOnlyFieldListFilter),]
    search_fields = ('guest_faculty_id','name','pan_number','inactive_flag')
    actions = ['assign_course']
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields + ('pan_number',)
        elif request.user.is_staff and request.user.groups.filter(name__in=['coordinator']):
            return self.readonly_fields + ('pan_number','guest_faculty_id',)
        else:
            return self.readonly_fields + ('guest_faculty_id',)
	
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
                           attrs={'rows': 2,
                                  'cols': 20})},
    }	
    inlines = (GuestFacultyQualificationInline,GfInterestedInDisciplineInline)
    #Level Based list_editable field show in below function 
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            list_editable = ('inactive_flag',)
        if request.user.is_staff and request.user.groups.filter(name__in=['coordinator']):
            list_editable = ('inactive_flag',)
        extra_context = {'title': 'WILP Guest Faculty List'}
        return super(GuestFacultyAdmin, self).changelist_view(request, extra_context=extra_context)
    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(GuestFacultyAdmin, self).get_form(request, obj, **kwargs)

    def save_related(self, request, form, formsets, change):
        obj = form.instance
        # whatever your formset dependent logic is to change obj.filedata and also some code dependency at tem/adm/change_form.html
        obj.save()
        super(GuestFacultyAdmin, self).save_related(request, form, formsets, change)
        gf = GuestFacultyQualification.objects.filter(guest_faculty=obj.id,highest_qualification=1).count()
        if gf==0:
            gfmax=GuestFacultyQualification.objects.filter(guest_faculty=obj.id).aggregate(Max('year_of_completion'))['year_of_completion__max']
            ghup=GuestFacultyQualification.objects.filter(guest_faculty=obj.id,year_of_completion=gfmax).update(highest_qualification=1)      
    def save_model(self, request, obj, form, change):
        if change:
            obj.last_updated_date=datetime.datetime.now()
            obj.save()
            apuser=User.objects.filter(id=request.user.id).update(pan_number=obj.pan_number)

    def has_add_permission(self, request, obj=None):
        if request.user.groups.filter(name__in=['GuestFaculty']).exists():
            return False
        else:
            return True

    def get_queryset(self, request):
        qs = super(GuestFacultyAdmin, self).get_queryset(request)
        if  request.user.is_superuser:
            return qs
        elif request.user.is_staff and request.user.groups.filter(name__in=['coordinator']):
            cl = Coordinator.objects.get(coordinator=request.user)
            return qs.filter(current_location=cl.coordinator_for_location)
        else :
            userpan=User.objects.filter(username=request.user).values_list('pan_number',flat=True)[0]
            return qs.filter(pan_number=userpan)
    def get_actions(self, request):
        actions = super(GuestFacultyAdmin, self).get_actions(request)
        if not request.user.is_staff:
            actions = []			
        return actions		

    def view_teach_history(self, request, obj):
        return HttpResponseRedirect("/application/facultyapp/guestfacultycourseoffer/?guest_faculty__id__exact=%s" % obj.id)
		
    view_teach_history.short_description = "View Teaching History"
    view_teach_history.label = "View Teaching History"

    objectactions = ('view_teach_history',)

                	
admin.site.register(GuestFaculty, GuestFacultyAdmin)

class GuestFacultyResource(resources.ModelResource):

    guest_faculty = fields.Field(column_name='guest_faculty', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'guest_faculty_id'))
    degree = fields.Field(column_name='degree', attribute='degree', widget=ForeignKeyWidget(Degree, 'degree_full_name'))
    qualification = fields.Field(column_name='qualification', attribute='qualification', widget=ForeignKeyWidget(Qualification, 'qualification_name'))
    qualification_discipline = fields.Field(column_name='qualification_discipline', attribute='qualification_discipline', widget=ForeignKeyWidget(Discipline, 'discipline_long_name'))    

    class Meta:
        model = GuestFacultyQualification

        fields = ('guest_faculty_id','qualification','degree','qualification_discipline','guest_faculty_pan_number','college','year_of_completion','highest_qualification','max_marks_cpi_cgpa','normalized_marks_cpi_cgpa','inserted_date','max_marks_cpi_cgpa','percent_marks_cpi_cgpa','completed',)
        import_id_fields = ['guest_faculty','guest_faculty_pan_number','year_of_completion',]
        export_order=('guest_faculty_id','guest_faculty_pan_number',)


class GuestFacultyQualificationAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = GuestFacultyResource
    model = GuestFacultyQualification
    list_display = ('guest_faculty_id','qualification','degree','qualification_discipline','guest_faculty_pan_number','college','year_of_completion','highest_qualification','max_marks_cpi_cgpa','completed')
    def has_add_permission(self, request, obj=None):
        return False	

    def has_delete_permission(self, request, obj=None):
        return False	
	
admin.site.register(GuestFacultyQualification, GuestFacultyQualificationAdmin)
   

class CourseAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = CourseResource

    list_display = ('course_id','course_name','number_of_lectures','dissertation_project_work')
    search_fields = ('course_id','course_name',)
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Course Master'}
        return super(CourseAdmin, self).changelist_view(request, extra_context=extra_context)	
	
admin.site.register(Course, CourseAdmin)

class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('discipline_id','discipline_long_name','discipline_short_name')
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Academic Discipline Master'}
        return super(DisciplineAdmin, self).changelist_view(request, extra_context=extra_context)	
	
admin.site.register(Discipline, DisciplineAdmin)

class DegreeAdmin(admin.ModelAdmin):
    list_display = ('degree_id','degree_full_name','degree_short_name')
admin.site.register(Degree, DegreeAdmin)

class NatureofcurrentjobAdmin(admin.ModelAdmin):
    list_display = ('id','name')
admin.site.register(Natureofcurrentjob,  NatureofcurrentjobAdmin)

class QualificationAdmin(admin.ModelAdmin):
    list_display = ('qualification_id','qualification_name','qualification_level')
    list_display_links = ('qualification_name',)
admin.site.register(Qualification,QualificationAdmin)

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('semester_id','semester_name','semester_number','year','start_date','end_date')
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Semester Master'}
        return super(SemesterAdmin, self).changelist_view(request, extra_context=extra_context)
	
admin.site.register(Semester, SemesterAdmin)

class CoordinatorForm(forms.ModelForm):
    coordinator_for_location = forms.ModelMultipleChoiceField(queryset=Location.objects.all(), widget=forms.CheckboxSelectMultiple,required=False)

    class Meta:
        model = Coordinator
        exclude = ['coordinator_for_location']

class CoordinatorAdmin(admin.ModelAdmin):
    #form = CoordinatorForm
    fields =('coordinator','coordinator_name','coordinator_address','phone','mobile','coordinator_for_location')
    list_display = ('coordinator','coordinator_name','coordinator_for_location')
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Location Coordinator List'}
        return super(CoordinatorAdmin, self).changelist_view(request, extra_context=extra_context)
    def save_model(self, request, obj, form, change):
        obj.save()
        apuser=User.objects.filter(username=obj.coordinator,is_staff=1).count()
        if apuser!=0:
            user=obj.coordinator
            apuser1=User.objects.filter(username=obj.coordinator,is_staff=1).values_list('email',flat=True)[0]
            coordinatormail=Coordinator.objects.filter(coordinator=obj.coordinator).update(email=apuser1)
            #user.is_staff = True
            #coordinatormail.save()
            #user.groups.add(Group.objects.get(name='coordinator'))
            user.save()
admin.site.register(Coordinator, CoordinatorAdmin)

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('program_id','program_code','program_name','specific_program','client_organization','program_coordinator')
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Program Master'}
        return super(ProgramAdmin, self).changelist_view(request, extra_context=extra_context)
    def save_model(self, request, obj, form, change):
        tprg=SemesterMilestonePlanMaster.objects.filter(program=obj.program_id).update(program_code1=obj.program_code)   
        obj.save()	
admin.site.register(Program, ProgramAdmin)

def accept_reject(obj):
    if obj.course_offer_status == "Offered":
        return "Accept/Reject"
    else: 
        return ""
accept_reject.short_description = ''

class GuestFacultyCourseOfferAdmin(ImportExportMixin,DjangoObjectActions,admin.ModelAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
    
    model = GuestFacultyCourseOffer
    resource_class = GFCOResource
    fields = ('course','semester','program','guest_faculty','location','program_coordinator','number_students_in_class','course_offer_status','assessment_score','honorarium_amount_paid','honorarium_pay_date')
    readonly_fields = ('course','semester','program','guest_faculty','location','course_offer_status','program_coordinator','number_students_in_class','assessment_score','honorarium_amount_paid','honorarium_pay_date')
    list_filter = ('semester','program','course_offer_status',('location',admin.RelatedOnlyFieldListFilter),'course__course_name')
    ordering = ['-update_datetime']
    #list_display_links = ('course',)
    

    def has_add_permission(self, request, obj=None):
        if request.user.groups.filter(name__in=['GuestFaculty']).exists():
            return True
        else:
            return False	
   
   # def has_delete_permission(self, request, obj=None):
        #return False	
		
    def changelist_view(self, request, extra_context=None):
        if request.user.groups.filter(name__in=['guestfaculty']).exists():
            self.list_display = ('course','semester','program','guest_faculty','location','number_students_in_class','course_offer_status','assessment_score',accept_reject)
            self.list_display_links = ('None', accept_reject)
        else:
            self.list_display = ('course','semester','program','guest_faculty','location','number_students_in_class','course_offer_status','assessment_score')
            self.list_display_links = ('course',)
        extra_context = {'title': 'View Course Assignments and Scores'}
        return super(GuestFacultyCourseOfferAdmin, self).changelist_view(request, extra_context=extra_context)
	
    def get_queryset(self, request):
        qs = super(GuestFacultyCourseOfferAdmin, self).get_queryset(request)
        if request.user.is_superuser :
            return qs
        elif  request.user.is_staff and request.user.groups.filter(name__in=['coordinator']):
            # coordinator_for_location is not null get location wise else get program wise
            if Coordinator.objects.filter(coordinator=request.user,coordinator_for_location__isnull=False).exists():
                cl = Coordinator.objects.get(coordinator=request.user)
                return qs.filter(location=cl.coordinator_for_location)
            else:
                pr =Program.objects.get(program_coordinator_id=request.user.id)
                return qs.filter(program=pr.program_id)
        else :
	    # get application's "owner" 
            return qs.filter(guest_faculty__updated_by=request.user.id)

    def accept_course_offer(self, request, obj):
        try:
            obj.course_offer_status='Accepted'
            obj.save()
            ls = CourseLocationSemesterDetail.objects.filter(course=obj.course,location=obj.location,semester=obj.semester,program=obj.program)
            ls.update(accepted_count=F('accepted_count') + 1)
            ls.update(assigned_count=F('assigned_count') - 1)
            #ls.update(assigned_count=F('assigned_count') - 1)
            #obj.save()
            #st1=ls.assigned_count
            #ls.update(assigned_count=0)
            message_bit = "Course was"
            self.message_user(request, "%s successfully marked as Accepted ." % message_bit)
        except IntegrityError:
            message_bit = "Course was"
            self.message_user(request, "%s was already marked as Accepted ." % message_bit,messages.ERROR)
			
    accept_course_offer.short_description = "Accept Course Offer"
    accept_course_offer.label = "Accept Course Offer"

    def reject_course_offer(self, request, obj):
        # catch the IntegrityError
        try:      
            obj.course_offer_status='Rejected'
            obj.save()
            # Decrement assigned_count in Course Location Semester Details   
            ls = CourseLocationSemesterDetail.objects.filter(course=obj.course,location=obj.location,semester=obj.semester,program=obj.program)
            ls.update(assigned_count=F('assigned_count') - 1)
            message_bit = "Course was"  
            self.message_user(request, "%s successfully marked as Rejected ." % message_bit)
        except IntegrityError:
            message_bit = "Course was"
            self.message_user(request, "%s was already marked as Rejected ." % message_bit,messages.ERROR)		

    reject_course_offer.short_description = "Reject Course Offer"
    reject_course_offer.label = "Reject Course Offer"
			
	
    objectactions = ('accept_course_offer','reject_course_offer',)

    def get_object_actions(self, request, context, **kwargs):
        objectactions = []
        obj = context['original']		
        if request.user.groups.filter(name__in=['guestfaculty']).exists():
            if obj.course_offer_status == "Offered":
                objectactions.extend(['accept_course_offer',])
                objectactions.extend(['reject_course_offer',])
        return objectactions
		
admin.site.register(GuestFacultyCourseOffer, GuestFacultyCourseOfferAdmin)




class CourseLocationSemesterDetailAdmin(ImportExportMixin,DjangoObjectActions,admin.ModelAdmin):
    #form = AssignCourseForm
    model=CourseLocationSemesterDetail
    list_display = ('course','location','semester','discipline','program', 'max_faculty_count','assigned_count','accepted_count')
    list_filter = (('location',admin.RelatedOnlyFieldListFilter),('semester',admin.RelatedOnlyFieldListFilter),('discipline',admin.RelatedOnlyFieldListFilter),('program',admin.RelatedOnlyFieldListFilter),)
    readonly_fields = ('assigned_count', 'accepted_count')	
    actions = ['assign_course']
    objectactions =['assign_course',]


    resource_class = CLSResource
    def get_queryset(self, request):
        qs = super(CourseLocationSemesterDetailAdmin, self).get_queryset(request)
        if request.user.is_superuser :
            return qs
           
        elif  request.user.is_staff and request.user.groups.filter(name__in=['coordinator']):
            # coordinator_for_location is not null get location wise else get program wise
            if Coordinator.objects.filter(coordinator=request.user,coordinator_for_location__isnull=False).exists():
                cl = Coordinator.objects.get(coordinator=request.user)
                return qs.filter(location=cl.coordinator_for_location)
            else:
                pr =Program.objects.get(program_coordinator_id=request.user.id)
                return qs.filter(program=pr.program_id)
        
            return ""

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Add/Edit Course Location Semester Details. Assign Course to Faculty'}
        return super(CourseLocationSemesterDetailAdmin, self).changelist_view(request, extra_context=extra_context)
    class AssignCourseForm(forms.Form):
        guestfaculty = forms.ModelChoiceField(label='Guest Faculty',queryset=GuestFaculty.objects.all())

    @takes_instance_or_queryset		
    def assign_course(self,request,queryset):
        form = None
        if 'update' in request.POST:
            form =AssignCourseForm(request.POST)
            if form.is_valid():
                guestfaculty = form.cleaned_data['guestfaculty']
                count = 0
                for course in queryset:
                    # Get Count of Faculty Offer records 
                    faculty_course_count = GuestFacultyCourseOffer.objects.filter(course=course.course,semester=course.semester,guest_faculty=guestfaculty).count()
					
                    # Check if record already exists and skip
                    if faculty_course_count < 1:
                        # Get Program Coordinator
                        prog_coord = Program.objects.get(program_id=course.program_id)
                        try:   
                            gfo = GuestFacultyCourseOffer(course=course.course,semester=course.semester,program=course.program,guest_faculty=guestfaculty,location=course.location,course_offer_status='Offered',sequence_number=faculty_course_count+1,program_coordinator_id=prog_coord.program_coordinator_id,offer_to_faculty_date=datetime.datetime.today(),number_students_in_class=course.number_of_students_in_class,max_faculty_count_reached=0)
                            gfo.save()
                            course.assigned_count = course.assigned_count + 1
                            course.save()
                            count += 1
                            template = 'courseassignemail.txt'
                            c = Context({'username': guestfaculty.name, 'application_url':settings.APPLICATION_URL1})                    
                            send_gfemail([guestfaculty.email],template,'Re: BITS Guest Faculty Application',c)
                        except Error as e:
                            pass					
                plural = ''
                if count > 0:
                    if count != 1:
                        plural = 's'				   
                    self.message_user(request, "Successfully assigned %d Course%s." % (count, plural))
                else:
                    self.message_user(request, "The allocation is not possible as the chosen faculty is already assigned this course",messages.ERROR)				    
                #return HttpResponseRedirect(request.get_full_path())
                return "<script>window.history.back();</script>"
        if not form:
            form =AssignCourseForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
				
   
        data = {'courses': queryset,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/assign_course.html', data)

    assign_course.label = "Assign Course to Faculty"
    assign_course.short_description = "Assign Course to Faculty"	
	
    def get_actions(self, request):
        if request.user.is_superuser or request.user.is_staff and request.user.groups.filter(name='coordinator').exists():
           actions = super(CourseLocationSemesterDetailAdmin, self).get_actions(request)           
        else:     
            actions = []			
        return actions			
	
admin.site.register(CourseLocationSemesterDetail, CourseLocationSemesterDetailAdmin)

class GuestFacultyHonarariumAdmin(ImportExportMixin,admin.ModelAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
 
    model = GuestFacultyHonararium
    resource_class = HonarariumResource
    list_display = ('course','semester','program','guest_faculty','location','course_offer_status','honorarium_given')
    fields = ('course','semester','program','guest_faculty','location','course_offer_status','honorarium_given','honorarium_text','hon_issued_on_date','hon_issued_by','honorarium_payment_mode')
    readonly_fields = ('course','semester','program','guest_faculty','location','course_offer_status','program_coordinator','number_students_in_class')
    list_filter = ('semester','program',('location',admin.RelatedOnlyFieldListFilter),'course__course_name',)
    # Provide Add permissions for GuestFacultyHonararium role only and disable all others	
    def has_add_permission(self, request, obj=None):
        if request.user.groups.filter(name__in=['GuestFacultyHonararium']).exists():
            return True
        else:
            return False

    def get_queryset(self, request):
        qs = super(GuestFacultyHonarariumAdmin, self).get_queryset(request)
        return qs.filter(course_offer_status='Accepted')
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Honorarium List'}
        return super(GuestFacultyHonarariumAdmin, self).changelist_view(request, extra_context=extra_context)	
	

#admin.site.register(GuestFacultyHonararium,GuestFacultyHonarariumAdmin)

class GuestFacultyScoreAdmin(ImportExportMixin,admin.ModelAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]

    
    model = GuestFacultyScore
    resource_class = ScoreResource
    list_display = ('course','semester','program','guest_faculty','location','course_offer_status','assessment_score','number_students_in_class',)
    fields = ('course','semester','program','guest_faculty','location','course_offer_status','number_students_in_class','assessment_score','feedback')
    readonly_fields = ('course','semester','program','guest_faculty','location','course_offer_status','program_coordinator','number_students_in_class')
    list_filter = ('semester','program',('location',admin.RelatedOnlyFieldListFilter),'course__course_name')
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Feedback'}
        return super(GuestFacultyScoreAdmin, self).changelist_view(request, extra_context=extra_context)	

    def get_queryset(self, request):
        qs = super(GuestFacultyScoreAdmin, self).get_queryset(request)
        return qs.filter(course_offer_status='Accepted')
    # Provide Add permissions for Guest Faculty Teaching Assessment Score role only and disable all others	
    def has_add_permission(self, request, obj=None):
        if request.user.groups.filter(name__in=['Guest Faculty Teaching Assessment Score']).exists():
            return True
        else:
            return False  
    	
   

#admin.site.register(GuestFacultyScore,GuestFacultyScoreAdmin)


class FacultyClassAttendanceAdmin(ImportExportMixin,admin.ModelAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
 
    model = FacultyClassAttendance
    resource_class = FacultyClassAttendanceResource
    list_display = ('guest_faculty','course','semester','program','class_date','class_time_slot','absent')
    fields = ('course','semester','program','guest_faculty','class_date','class_time_slot','absent','comments_for_absence')
    #readonly_fields = ('course','semester','program','guest_faculty')
    list_filter = ('semester','program',('guest_faculty',admin.RelatedOnlyFieldListFilter),'course__course_name')

    # Make some fields readonly when editing and not while adding	
    def get_readonly_fields(self, request, obj=None):
        if obj: #This is the case when obj is already created i.e. it's an edit
            return ['course','semester','program','guest_faculty']
        else:
            return []
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Attendance Details'}
        return super(FacultyClassAttendanceAdmin, self).changelist_view(request, extra_context=extra_context)	

admin.site.register(FacultyClassAttendance,FacultyClassAttendanceAdmin)


class FeedbackSurveyAdmin(admin.ModelAdmin):
    list_display = ('survey_name','version_id','question_description',) 
    list_display_links = ('survey_name', 'version_id',)
    fields = ('survey_id','version_id','question_id','survey_name','question_description','question_type','mandatory',)
    readonly_fields = ('survey_id','version_id','question_id','survey_name','question_description','question_type','mandatory',)

    def has_add_permission(self, request, obj=None):
        return False	

    def has_delete_permission(self, request, obj=None):
        return False
		
#admin.site.register(FeedbackSurvey, FeedbackSurveyAdmin)

class GFFeedbackResultsAdmin(admin.ModelAdmin):
    list_display = ('guest_faculty_pan_number','semester','program','course','survey_id','survey_version_id','survey_question_id','student_choice','student_comments','answered_date')
    list_display_links = ('guest_faculty_pan_number',)
    fields = ('guest_faculty_pan_number','semester','program','course','survey_id','survey_version_id','survey_question_id','student_choice','student_comments','answered_date')
    readonly_fields = ('guest_faculty_pan_number','semester','program','course','survey_id','survey_version_id','survey_question_id','student_choice','student_comments','answered_date')

    def has_add_permission(self, request, obj=None):
        return False	

    def has_delete_permission(self, request, obj=None):
        return False

#admin.site.unregister(GuestFacultyFeedbackResults)		

admin.site.register(GuestFacultyFeedbackResults, GFFeedbackResultsAdmin)


    #change_actions = ('publish_this', )
    #objectactions = ('publish_this',)
def runprocess(self,request,queryset):
    form = None
    currentgftech=CurrentGFSemester.objects.values_list('current_semester',flat=True)[0]
    semyear=Semester.objects.filter(semester_id=currentgftech).values_list('year',flat=True)[0]
    semnum=Semester.objects.filter(semester_id=currentgftech).values_list('semester_number',flat=True)[0]
    #cur.execute("DELETE FROM guest_faculty_bucket")
    #cnx.commit()
    GuestFacultyBucket.objects.all().delete()
    for gfbucket in queryset:
        gfbucketid=gfbucket.bucket_id
        #connection with mysql db
        cursor1 = connection.cursor()
        gfcurflag=gfbucket.current_faculty_flag
        gfinactflag=gfbucket.inactive_faculty_flag
        lowerbound=gfbucket.lower_tech_interval_gap
        upperbound=gfbucket.upper_tech_interval_gap
        active_bucket_flag1=gfbucket.active_bucket_flag
        if gfcurflag==1:
            gfbucket.upper_bound_sem_nbr=semnum
            gfbucket.lower_bound_sem_nbr=None
            gfbucket.upper_bound_year=semyear
            gfbucket.lower_bound_year=None
            gfbucket.save()
            try:
                queary="select distinct gfco.guest_faculty_id,fbm.bucket_id from guest_faculty_course_offer gfco,faculty_bucket_master fbm,semester s where gfco.semester_id=s.semester_id and fbm.current_faculty_flag=1 and fbm.upper_bound_year=s.year and s.semester_number=fbm.upper_bound_sem_nbr and fbm.active_bucket_flag=1"
                cursor1.execute(queary)
            
                for row in cursor1.fetchall():
                    #inser into dynamic data
		    add_query = ("INSERT INTO guest_faculty_bucket "
		    "(faculty_bucket_id, guest_faculty_id, bucket_assigned_on) "
		    "VALUES (%s, %s, %s)")
		    data_query = (row[1], row[0], datetime.datetime.today())
		    cursor1.execute(add_query, data_query)   
		    connection.commit()
                    print data_query
            finally:
                cursor1.close()
        elif gfinactflag==1:
            cursor2 = connection.cursor()
            gfbucket.upper_bound_sem_nbr=None
            gfbucket.lower_bound_sem_nbr=None
            gfbucket.upper_bound_year=None
            gfbucket.lower_bound_year=None
            gfbucket.save()
            try:
                queary2="SELECT r.id,fc.bucket_id FROM faculty_bucket_master fc , guest_faculty r WHERE  NOT EXISTS (SELECT * FROM guest_faculty_course_offer re WHERE r.id = re.guest_faculty_id) AND fc.inactive_faculty_flag=1"
                cursor2.execute(queary2)
                for row in cursor2.fetchall():
		    add_query = ("INSERT INTO guest_faculty_bucket "
		    "(faculty_bucket_id, guest_faculty_id, bucket_assigned_on) "
		    "VALUES (%s, %s, %s)")
		    data_query = (row[1], row[0], datetime.datetime.today())
		    cursor2.execute(add_query, data_query)   
		    connection.commit()
               
            finally:
                cursor2.close()
        elif (gfcurflag==False and gfinactflag==False):
            if (lowerbound!=None and upperbound!=None and active_bucket_flag1==1) :
                if int(semnum)==1:
                    x=Decimal(lowerbound)/2
                    y=Decimal(upperbound)/2
                    #it will check the x value is 0.5,1.5,205,......based on np(install numpy)
                    if x in np.arange(0.5,int(lowerbound)):
                        z=Decimal(x)+Decimal('0.5')
                        gfbucket.lower_bound_year=int(semyear)-int(z)
                        gfbucket.save()
                    else:
                        gfbucket.lower_bound_year=int(semyear)-int(x)
                        gfbucket.save()
                    if y in np.arange(0.5,int(upperbound)):
                        z=Decimal(y)+Decimal('0.5')
                        gfbucket.upper_bound_year=int(semyear)-int(z)
                        gfbucket.save()
                    else:
                        gfbucket.upper_bound_year=int(semyear)-int(y)
                        gfbucket.save()
                    if int(lowerbound)%2 == 0:
                        gfbucket.lower_bound_sem_nbr=1
                        gfbucket.save()
                    if int(upperbound)%2 == 0:
                        gfbucket.upper_bound_sem_nbr=1
                        gfbucket.save()
                    if int(lowerbound)%2 != 0:
                        gfbucket.lower_bound_sem_nbr=2
                        gfbucket.save()
                    if int(upperbound)%2 != 0:
                        gfbucket.upper_bound_sem_nbr=2
                        gfbucket.save()
                if int(semnum)==2:
                    x=Decimal(lowerbound)/2
                    y=Decimal(upperbound)/2 
                    lower_sem_nbr1=int(lowerbound)/2
                    upper_sem_nbr1=int(upperbound)/2
                    if x in np.arange(0.5,int(lowerbound)):
                        z=Decimal(x)-Decimal('0.5')
                        gfbucket.lower_bound_year=int(semyear)-int(z)
                        gfbucket.save()
                    else:
                        gfbucket.lower_bound_year=int(semyear)-int(x)
                        gfbucket.save()
                    if y in np.arange(0.5,int(upperbound)):
                        z=Decimal(y)-Decimal('0.5')
                        gfbucket.upper_bound_year=int(semyear)-int(z)
                        gfbucket.save()
                    else:
                        gfbucket.upper_bound_year=int(semyear)-int(y)
                        gfbucket.save()
                    if int(lowerbound)%2==0:
                        gfbucket.lower_bound_sem_nbr=2
                        gfbucket.save()
                    if int(upperbound)%2==0:
                        gfbucket.upper_bound_sem_nbr=2
                        gfbucket.save()
                    if int(lowerbound)%2!=0:
                        gfbucket.lower_bound_sem_nbr=1
                        gfbucket.save()
                    if int(upperbound)%2!=0:
                        gfbucket.upper_bound_sem_nbr=1
                        gfbucket.save()
                cursor3 = connection.cursor()
                try:
                    queqry4="SELECT DISTINCT GFCO.guest_faculty_id, FBM.bucket_id,FBM.lower_bound_year,FBM.lower_bound_sem_nbr FROM guest_faculty_course_offer GFCO, semester S, faculty_bucket_master FBM WHERE GFCO.semester_id = S.semester_id AND (S.year > FBM.lower_bound_year AND S.year < FBM.upper_bound_year) OR (S.year = FBM.lower_bound_year AND S.semester_number >= FBM.lower_bound_sem_nbr) OR (S.year = FBM.upper_bound_year AND S.semester_number <= FBM.upper_bound_sem_nbr) AND FBM.ACTIVE_BUCKET_FLAG = 1 AND inactive_faculty_flag = 0 AND current_faculty_flag = 0 AND GFCO.course_offer_status='accepted' AND FBM.bucket_id='%s'" % gfbucketid
                    cursor3.execute(queqry4)
                    data4=cursor3.fetchall()
                    datalen=len(data4)
                    print "%s:%d" % (gfbucketid, datalen)
                    if datalen!=0:
                       #query5="SELECT FBM.bucket_id FROM guest_faculty_course_offer GFCO, semester S, faculty_bucket_master FBM WHERE GFCO.semester_id = S.semester_id AND ((S.year > FBM.lower_bound_year AND S.year < FBM.upper_bound_year) OR (S.year = FBM.lower_bound_year AND S.semester_number >= FBM.lower_bound_sem_nbr) OR (S.year = FBM.upper_bound_year AND S.SEMESTER_NUMBER <= FBM.upper_bound_sem_nbr)) AND FBM.ACTIVE_BUCKET_FLAG = 1 AND inactive_faculty_flag = 0 AND current_faculty_flag = 0 AND GFCO.course_offer_status='accepted' order by lower_bound_year,lower_bound_sem_nbr limit 1"
                        query5="SELECT FBM.bucket_id FROM guest_faculty_course_offer GFCO, semester S, faculty_bucket_master FBM WHERE GFCO.semester_id = S.semester_id AND (S.year > FBM.lower_bound_year AND S.year < FBM.upper_bound_year) OR (S.year = FBM.lower_bound_year AND S.semester_number >= FBM.lower_bound_sem_nbr) OR (S.year = FBM.upper_bound_year AND S.semester_number <= FBM.upper_bound_sem_nbr) AND FBM.ACTIVE_BUCKET_FLAG = 1 AND inactive_faculty_flag = 0 AND CURRENT_FACULTY_FLAG = 0 AND GFCO.course_offer_status='accepted' order by lower_tech_interval_gap limit 1"
                        cursor3.execute(query5)
                        data1=cursor3.fetchone()[0]
                        if (data1==gfbucketid):
                            query6=("SELECT FBM.bucket_id FROM faculty_bucket_master FBM,guest_faculty_bucket WHERE FBM.ACTIVE_BUCKET_FLAG = 1 AND inactive_faculty_flag = 0 AND current_faculty_flag = 0 and bucket_id=faculty_bucket_id and (bucket_id!='%s' and bucket_id!='%s') limit 1" %(data1,-1))
                            cursor3.execute(query6)
                            data6=cursor3.fetchall()
                            if data6>0:
                                for row in data6:
                                    qs=GuestFacultyBucket.objects.filter(faculty_bucket_id=row[0])
                                    qs.delete()
                            queqry3="SELECT DISTINCT GFCO.guest_faculty_id, FBM.bucket_id,FBM.lower_bound_year,FBM.lower_bound_sem_nbr FROM guest_faculty_course_offer GFCO, semester S, faculty_bucket_master FBM WHERE GFCO.semester_id = S.semester_id AND (S.year > FBM.lower_bound_year AND S.year < FBM.upper_bound_year) OR (S.year = FBM.lower_bound_year AND S.semester_number >= FBM.lower_bound_sem_nbr) OR (S.year = FBM.upper_bound_year AND S.semester_number <= FBM.upper_bound_sem_nbr) AND FBM.ACTIVE_BUCKET_FLAG = 1 AND inactive_faculty_flag = 0 AND current_faculty_flag = 0 AND GFCO.course_offer_status='accepted' AND FBM.bucket_id='%s'" % gfbucketid
                            cursor3.execute(queqry3)
                            data=cursor3.fetchall()
                            for row in data:
                                add_query = ("INSERT INTO guest_faculty_bucket "
                                "(faculty_bucket_id, guest_faculty_id, bucket_assigned_on) "
                                "VALUES (%s, %s, %s)")
                                data_query = (row[1], row[0], datetime.datetime.today())
                                cursor3.execute(add_query, data_query)
                            connection.commit()
                finally:
                    cursor3.close()
            else:
                try:
                    cursor4 = connection.cursor()
                    queary5="select id from guest_faculty where id not in(select guest_faculty_id from guest_faculty_bucket)"
                    cursor4.execute(queary5)
                    data5=cursor4.fetchall()
                    for row in data5:
                        add_query = ("INSERT INTO guest_faculty_bucket "
                        "(faculty_bucket_id, guest_faculty_id, bucket_assigned_on) "
                        "VALUES (%s, %s, %s)")
                        data_query = (-1, row[0], datetime.datetime.today())
                        cursor4.execute(add_query, data_query)
                    connection.commit()
                finally:
                    cursor4.close()

        else:
            return
            gfbucket.save()
    self.message_user(request, "GF Categorization Process Run Successfully")

runprocess.label = "Run GF Categorization Process"
runprocess.short_description = "Run GF Categorization Process"


class FacultyBucketMasterForm(forms.ModelForm):
    def clean(self):
        lower_limit = self.cleaned_data.get('lower_tech_interval_gap')
        upper_limit = self.cleaned_data.get('upper_tech_interval_gap')
        print lower_limit
        print upper_limit
        if(lower_limit!=None or upper_limit!=None):
            
            if(upper_limit <lower_limit ):
                raise forms.ValidationError("Please check lower and upper values")
        uppernewque=FacultyBucketMaster.objects.latest('bucket_id')
        print uppernewque.upper_tech_interval_gap
        print lower_limit
        lastuooertech=uppernewque.upper_tech_interval_gap
        if(lower_limit!=None or upper_limit!=None):
            if(lastuooertech >lower_limit):
                raise forms.ValidationError("Bucket entry not saved as it as an overlap with another existing bucket")
        lowerrange=FacultyBucketMaster.objects.all()
        for lwrange in lowerrange:
            print lwrange
            print lwrange.lower_tech_interval_gap
            print lwrange.upper_tech_interval_gap
            lwtech=FacultyBucketMaster.objects.filter(lower_tech_interval_gap__range=[lwrange.lower_tech_interval_gap,lwrange.upper_tech_interval_gap])
            print lwtech.query
        
   
                 
class FacultyBucketMasterAdmin(admin.ModelAdmin):
    #upper and lower bucket overlaping conditions js path (tem/adm/facultyapp/facultybucketmaster) 
    actions = None
    form = FacultyBucketMasterForm
    fields=('bucket_name','lower_tech_interval_gap','upper_tech_interval_gap',)
    list_display =('bucket_name','lower_tech_interval_gap','upper_tech_interval_gap','current_faculty_flag','inactive_faculty_flag',)
    list_editable = ('lower_tech_interval_gap','upper_tech_interval_gap','current_faculty_flag','inactive_faculty_flag',)
    #readonly_fields = ('lower_tech_interval_gap','upper_tech_interval_gap',)
    actions = [runprocess]	
    def save_model(self, request, obj, form, change):
        obj.updated_on=datetime.datetime.now()
        obj.updated_by=request.user.id
        obj.save()
        if(obj.current_faculty_flag==1):
           obj.lower_tech_interval_gap=None
           obj.upper_tech_interval_gap=None
           obj.lower_bound_year=None
           obj.lower_bound_sem_nbr=None
           obj.upper_bound_year=None
           obj.upper_bound_sem_nbr=None
           obj.inactive_faculty_flag=0
           obj.bucket_name='CURRENT FACULTY'
           obj.current_faculty_flag=1
           obj.active_bucket_flag=1
           obj.save()
        elif(obj.inactive_faculty_flag==1):
           obj.lower_tech_interval_gap=None
           obj.upper_tech_interval_gap=None
           obj.lower_bound_year=None
           obj.lower_bound_sem_nbr=None
           obj.upper_bound_year=None
           obj.upper_bound_sem_nbr=None
           obj.inactive_faculty_flag=1
           obj.bucket_name='INACTIVE FACULTY'
           obj.current_faculty_flag=0
           obj.active_bucket_flag=1
           obj.save()
        elif (obj.inactive_faculty_flag==None and obj.current_faculty_flag==None) or (obj.inactive_faculty_flag==0 and obj.current_faculty_flag==0):
           obj.lower_bound_year=None
           obj.lower_bound_sem_nbr=None
           obj.upper_bound_year=None
           obj.upper_bound_sem_nbr=None
           obj.inactive_faculty_flag=0
           obj.current_faculty_flag=0
           obj.active_bucket_flag=1
           obj.save()
        else:
           obj.save()
admin.site.register(FacultyBucketMaster, FacultyBucketMasterAdmin)

class GuestFacultyBucketAdmin(admin.ModelAdmin):
    model = GuestFacultyBucket
    list_display = ('guest_faculty','faculty_bucket','bucket_assigned_on',)
    fields = ('guest_faculty','faculty_bucket','bucket_assigned_on',)

    def get_queryset(self, request):
        qs = super(GuestFacultyBucketAdmin, self).get_queryset(request)
        if request.user.is_superuser :
            return qs
admin.site.register(GuestFacultyBucket, GuestFacultyBucketAdmin)




admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
#admin.site.register(User, UserAdmin)
#admin.site.register(get_user_model(), UserAdmin)


admin.site.disable_action('delete_selected') #disable action in MRA Action list

class CurrentGFSemesterAdmin(admin.ModelAdmin):
    #add button name change js path (tem/adm/facultyapp/currentgfsemester) 
    list_display = ('current_semester_id',)
    def save_model(self, request, obj, form, change):
        CurrentGFSemester.objects.all().delete()
        obj.save()

admin.site.register(CurrentGFSemester,CurrentGFSemesterAdmin)

# Create Separate Admin site for Non-Admin/Non-Staff Users
class UserAdminAuthenticationForm(AuthenticationForm):
    sdf=1

#Register Admin Site for Guest Faculty Candidates
class GFAppSite(AdminSite):
    site_header = 'Guest Faculty Online Application'
    site_title =  'Guest Faculty Online Application'
    site_url = None
    index_title = 'Guest Faculty Online Application'
    index_template = 'facultyapp/index.html'
    app_index_template = 'facultyapp/index.html'
    login_form = UserAdminAuthenticationForm

    def has_permission(self, request):
        return request.user.is_active
		
gf_app_site = GFAppSite(name='candidateapplication')
gf_app_site.register(GuestFacultyCandidate,GuestFacultyCandidateAdmin)
#gf_app_site.register(GuestFacultyCourseOffer, GuestFacultyCourseOfferAdmin)
#gf_app_site.disable_action('delete_selected') #disable action in MRA Action list

# End of New Admin Site



class AssessmentQuestionMasterAdmin(admin.ModelAdmin):
    list_display = ('question_id','question_description')
 
admin.site.register(AssessmentQuestionMaster,AssessmentQuestionMasterAdmin)

class AssessmentMasterAdmin(admin.ModelAdmin):
    list_display = ('assessment_id','assessment_identifier')
admin.site.register(AssessmentMaster,AssessmentMasterAdmin)

class GfAssessmentSummaryResource(resources.ModelResource):
    guest_faculty_id = fields.Field(column_name='guest faculty id', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'guest_faculty_id'))
    #guest_faculty_name = fields.Field(column_name='name', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'name'))
    #guest_faculty_location = fields.Field(column_name='location', attribute='guest_faculty__recruitment_location', widget=ForeignKeyWidget(Location, 'location_name'))
    #coordinator_email = fields.Field(column_name='coordinator email', attribute='coordinator_owner__coordinator', widget=ForeignKeyWidget(User, 'email'))
    #username1 = fields.Field(column_name='coordinator email', attribute='coordinator_owner', widget=ForeignKeyWidget(Coordinator, 'coordinator_name'))
    #username = fields.Field(column_name='program coordinator', attribute='program_coordinator__coordinator', widget=ForeignKeyWidget(User, 'username'))
    coordinatormail= fields.Field(column_name='coordinator email', attribute='coordinator', widget=ForeignKeyWidget(Coordinator, 'email'))
    #newusername = fields.Field(column_name='coordinator email', attribute='coordinator__coordinator', widget=ForeignKeyWidget(User, 'username'))
    #new_email = fields.Field(column_name='coordinator_email', attribute='coordinator__coordinator', widget=ForeignKeyWidget(User, 'username'))
    class Meta:
        model = GuestFacultyAssessmentSummary
        fields = ('guest_faculty_id','coordinatormail','assessment_date','assessment_identifier','overall_score','normalized_score','gf_strength','gf_weaknesses','assessor1_name','assessor2_name','assessor3_name','sme1_name','sme2_name','recommendations_comments','created_on','last_updated_on','last_updated_by',)
        import_id_fields = ['guest_faculty_id','assessment_identifier',]
        export_order=('guest_faculty_id','assessment_identifier','assessment_date',)

class GuestFacultyAssessmentSummaryAdmin(ImportExportMixin,admin.ModelAdmin):
    #template = "/admin/facultyapp/guestfacultyassessmentsummary/change_list.html"
    class Media:
       static_url = getattr(settings, 'STATIC_URL', '/static/')
       print static_url
       print "varna" 
       js = [ static_url+'admin/js/list_filter_collaps.js', ]
    resource_class = GfAssessmentSummaryResource
    fields = ('guest_faculty','assessment_identifier','assessment_date','assessment_location','overall_score','normalized_score','gf_strength','gf_weaknesses','recommendations_comments','assessor1_name','assessor2_name','assessor3_name','sme1_name','sme2_name','coordinator')
    list_display = ('guest_faculty','assessment_identifier','assessment_date','overall_score','normalized_score','coordinator1')
    list_filter = ('guest_faculty','assessment_location','coordinator','assessment_identifier',)

    def save_model(self, request, obj, form, change):
        obj.last_updated_on=datetime.datetime.now()
        obj.last_updated_by=request.user.id
        obj.save()

    def get_queryset(self, request):
        qs = super(GuestFacultyAssessmentSummaryAdmin, self).get_queryset(request)
        if  request.user.is_superuser:
            return qs
        if request.user.is_staff and request.user.groups.filter(name__in=['coordinator']):
            cl = Coordinator.objects.get(coordinator=request.user)
            return qs.filter(coordinator=cl)
        if request.user.groups.filter(name__in=['hr']):
            return qs


admin.site.register(GuestFacultyAssessmentSummary,GuestFacultyAssessmentSummaryAdmin)


class GfAssessmentDetailedResource(resources.ModelResource):
    guest_faculty_id = fields.Field(column_name='guest faculty id', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'guest_faculty_id'))
    #guest_faculty_name = fields.Field(column_name='name', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'name'))
    #guest_faculty_location = fields.Field(column_name='location', attribute='guest_faculty__recruitment_location', widget=ForeignKeyWidget(Location, 'location_name'))
    coordinatormail1 = fields.Field(column_name='coordinator email', attribute='assessment_identifier__coordinator__coordinator', widget=ForeignKeyWidget(Coordinator, 'email'))
    questiondesrciption = fields.Field(column_name='question desrciption', attribute='question', widget=ForeignKeyWidget(AssessmentQuestionMaster, 'question_id'))
    assessmentidentifier= fields.Field(column_name='assessment identifier', attribute='assessment_identifier', widget=ForeignKeyWidget(GuestFacultyAssessmentSummary, 'assessment_identifier'))
    class Meta:
        model = GuestFacultyDetailedAssessment
        fields = ('guest_faculty_id','questiondesrciption','coordinatormail1','assessment_score','key_observations','recommendations','created_on','last_updated_on','last_updated_by',)
        import_id_fields = ['guest_faculty_id']
        #export_order=('guest_faculty_id','coordinator','assessment_identifier','question_desrciption','assessment_score')


class GuestFacultyDetailedAssessmentAdmin(ImportExportMixin,admin.ModelAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
    fields = ('guest_faculty','assessment_identifier','question','assessment_score','key_observations','recommendations')
    list_display = ('guest_faculty','assessment_identifier','guestfacultyassessmentsummary_assessment_date','question1','assessment_score','key_observations','guestfacultyassessmentsummary_coordinator',)
    list_filter = ('guest_faculty','assessment_identifier__coordinator__coordinator','assessment_identifier','question',)

    resource_class = GfAssessmentDetailedResource

    def save_model(self, request, obj, form, change):
        obj.last_updated_on=datetime.datetime.now()
        obj.last_updated_by=request.user.id
        obj.save()
admin.site.register(GuestFacultyDetailedAssessment,GuestFacultyDetailedAssessmentAdmin)


class CategoryValueMasterAdmin(admin.ModelAdmin):
    fields = ('category_value',)
    list_display = ('category_value',)
    search_fields = ('category_value',)

admin.site.register(CategoryValueMaster,CategoryValueMasterAdmin)


class CategoryNameMasterAdmin(admin.ModelAdmin):
    fields = ('category_name',)
    list_display = ('category_name',)
    search_fields = ('category_name',)

admin.site.register(CategoryNameMaster,CategoryNameMasterAdmin)


class HrMasterResource(resources.ModelResource):

    category = fields.Field(column_name='category', attribute='category', widget=ForeignKeyWidget(CategoryNameMaster, 'category_name'))
    category1_value = fields.Field(column_name='category1_value', attribute='category1_value', widget=ForeignKeyWidget(CategoryValueMaster, 'category_value'))
    category2_value = fields.Field(column_name='category2_value', attribute='category2_value', widget=ForeignKeyWidget(CategoryValueMaster, 'category_value'))

    class Meta:
        model = HonorariumRateMaster

        fields = ('category','category1_value','category2_value','active_flag','honorarium_rate','honorarium_amount',)
        import_id_fields = ['category','category1_value','category2_value','active_flag','honorarium_rate','honorarium_amount',]
        export_order = ('category','category1_value','category2_value','active_flag','honorarium_rate','honorarium_amount',)

class HonorariumRateMasterForm(forms.ModelForm):
    def clean(self):
        honorariumrate= self.cleaned_data.get('honorarium_rate')
        honorariumamount = self.cleaned_data.get('honorarium_amount')
        
        if honorariumrate==0  :
            raise forms.ValidationError(" Honorarium Rate Cannot be Null and  greater than 0 ")
      
        if honorariumamount==0 :
            raise forms.ValidationError(" Honorarium Amount Cannot be Null and  greater than 0 ")
        
        

class HonorariumRateMasterAdmin(ImportExportMixin,admin.ModelAdmin):

    class Media:
       static_url = getattr(settings, 'STATIC_URL', '/static/')
       js = [ static_url+'admin/js/list_filter_collaps.js', ]
    resource_class = HrMasterResource
    model = HonorariumRateMaster
    form = HonorariumRateMasterForm
    fields = ('category','category1_value','category2_value','active_flag','honorarium_rate','honorarium_amount',)
    list_display = ('category','category1_value','category2_value','honorarium_rate','honorarium_amount',)
    list_filter = ('active_flag','category1_value',)

    def save_model(self, request, obj, form, change):
        obj.last_updated_on=datetime.datetime.now()
        obj.last_updated_by=request.user.id
        obj.save()

    def get_queryset(self, request):
        qs = super(HonorariumRateMasterAdmin, self).get_queryset(request)
        if  request.user.is_superuser:
            return qs

   

admin.site.register(HonorariumRateMaster,HonorariumRateMasterAdmin)

class HonorariumFieldKeyWordsAdmin(admin.ModelAdmin):
    fields = ('key_value','field_name')
    list_display = ('key_value','field_name')

admin.site.register(HonorariumFieldKeyWords,HonorariumFieldKeyWordsAdmin)


class AcOfferAttributesResource(resources.ModelResource):

    course = fields.Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'program_name'))
    guest_faculty = fields.Field(column_name='guest_faculty', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'name'))
    faculty_role = fields.Field(column_name='faculty_role', attribute='faculty_role', widget=ForeignKeyWidget(CategoryNameMaster, 'category_name'))
    qp_work_done = fields.Field(column_name='qp_work_dome', attribute='qp_work_dome', widget=ForeignKeyWidget(CategoryNameMaster, 'category_name'))
    dissertation_role = fields.Field(column_name='dissertation_role', attribute='dissertation_role', widget=ForeignKeyWidget(CategoryNameMaster, 'category_name'))

    class Meta:
        model = AdditionalCourseOfferAttributes
    
    fields = ('course','semester','program','guest_faculty','course_type','mid_sem_weightage','compre_weightage','assignment_weightage','number_of_students','number_of_lectures','faculty','mid_sem_evaluated_flag','assignment_evaluated_flag','compre_evaluated_flag','qp_work_done','course_location_section_detail','mid_sem_exam_students_count','dissertation1','dissertation_students_count','assignment_student_count','compre_exams_students_count','honorarium_calculated_flag',)
    import_id_fields = ['course','semester','program','guest_faculty','course_type','mid_sem_weightage','compre_weightage','assignment_weightage','number_of_students','number_of_lectures','faculty','mid_sem_evaluated_flag','assignment_evaluated_flag','compre_evaluated_flag','qp_work_done','course_location_section_detail','mid_sem_exam_students_count','dissertation','dissertation_students_count','assignment_student_count','compre_exams_students_count','honorarium_calculated_flag',]
    export_order = ('guest_faculty','course','semester',)



def Calculate_Honararium_Amounts(self,request,queryset):
    form=None
   # global r1,r2,r3,r4,r5,r6,r7,r8,r9,r10
    for calculate in queryset:
        cursor1 = connection.cursor()
        try:
            
            queary1 = "SELECT hrm.honorarium_rate FROM honorarium_rate_master hrm, honorarium_field_key_words hfkw, additional_course_offer_attributes acoa WHERE hrm.active_flag = 1 and hfkw.field_name = 'lecture_rate_used' AND acoa.faculty_role_id = hrm.category1_value_id " 
            cursor1.execute(queary1)
            r1= cursor1.fetchone()                        
            print r1
            
            queary2 = "select honorarium_amount from honorarium_rate_master hrm ,honorarium_field_key_words ,honorarium_category_master hcm where hrm.active_flag='1' and hrm.category_id=key_value_id and key_value_id=hcm.category_id and field_name= 'mid_sem_qp_rate_used'"
            cursor1.execute(queary2)                    
            r2=cursor1.fetchone()  
            print r2
            
            queary3= "select honorarium_amount from honorarium_rate_master hrm,honorarium_field_key_words,honorarium_category_master hcm where hrm.active_flag='1' and hrm.category_id=key_value_id and hcm.category_id=key_value_id and field_name= 'compre_qp_rate_used' "
            cursor1.execute(queary3)
            r3= cursor1.fetchone()                          
            print r3
           
            queary4 = "select honorarium_rate from honorarium_rate_master hrm,honorarium_field_key_words,additional_course_offer_attributes acoa,honorarium_category_master hcm where hrm.active_flag='1' and hrm.category_id=key_value_id and hcm.category_id=key_value_id and mid_sem_evaluated_flag='1' and field_name= 'mid_sem_eval_rate_used' limit 1"
            cursor1.execute(queary4)
            r4= cursor1.fetchone()                          
            print r4  
          

            queary5= " select honorarium_rate from honorarium_rate_master hrm,honorarium_field_key_words, additional_course_offer_attributes acoa,honorarium_category_master hcm where hrm.active_flag='1'  and hrm.category_id=key_value_id and hcm.category_id=key_value_id and compre_evaluated_flag='1' and field_name= 'compre_eval_rate_used'limit 1 "    
            cursor1.execute(queary5)
            r5= cursor1.fetchone()  
            print r5
           

            queary6 = " select honorarium_rate from honorarium_rate_master hrm,honorarium_field_key_words, additional_course_offer_attributes acoa,honorarium_category_master hcm where hrm.active_flag='1' and hrm.category_id=key_value_id and hcm.category_id=key_value_id and assignment_evaluated_flag='1' and field_name= 'assignment_eval_rate_used' limit 1  "  
            cursor1.execute(queary6)
            r6= cursor1.fetchone()
            print r6  
            
            sql = " select course_id,semester_id,program_id,guest_faculty_id from additional_course_offer_attributes "
            cursor1.execute(sql)
            for row in cursor1.fetchall():              
                       
                add_query= ("INSERT INTO guest_faculty_honorarium "
		    "(course_id,semester_id,program_id,guest_faculty_id,lecture_rate_used,mid_sem_qp_rate_used,compre_qp_rate_used,mid_sem_eval_rate_used,compre_eval_rate_used,assignment_eval_rate_used) "                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

                data_query = (row[0], row[1], row[2], row[3],r1,r2,r3,r4,r5,r6)
                cursor1.execute(add_query, data_query)  
	        cursor1.fetchall()  
                connection.commit()                
	      
	                        
        finally:
            cursor1.close()
        calculate.save()
    self.message_user(request, " Calculate_Honararium_Amounts Process Run Successfully")
    
class AdditionalCourseOfferAttributesAdmin(BaseDjangoObjectActions,ImportExportMixin,admin.ModelAdmin):

    class Media:
       static_url = getattr(settings, 'STATIC_URL', '/static/')
       js = [ static_url+'admin/js/list_filter_collaps.js', ]
    resource_class = AcOfferAttributesResource
    model = AdditionalCourseOfferAttributes    
    fields = ('course','semester','program','guest_faculty','course_type','mid_sem_weightage','compre_weightage','assignment_weightage','number_of_students','number_of_lectures','faculty_role','mid_sem_evaluated_flag','assignment_evaluated_flag','compre_evaluated_flag','qp_work_done','course_location_section_detail','mid_sem_exam_students_count','dissertation_role','dissertation_students_count','assignment_student_count','compre_exams_students_count','honorarium_calculated_flag',)
    list_display = ('guest_faculty','course','semester','course_type','faculty_role','course_location_section_detail','number_of_students','createddatetime',)
    list_filter =('course','semester','program','guest_faculty') 
    actions = [Calculate_Honararium_Amounts,]
   # readonly_fields = ('honorarium_calculated_flag',)
 
    def save_model(self, request, obj, form, change):
        obj.last_updated_on=datetime.datetime.now()
        obj.last_updated_by=request.user.id 
        obj.save()
        

    def get_queryset(self, request):
        qs = super(AdditionalCourseOfferAttributesAdmin, self).get_queryset(request)
        if  request.user.is_superuser:
            return qs
  
        
admin.site.register(AdditionalCourseOfferAttributes,AdditionalCourseOfferAttributesAdmin)



class GuestFacultyHonorariumAdmin(admin.ModelAdmin):
    class Media:
       static_url = getattr(settings, 'STATIC_URL', '/static/')
       js = [ static_url+'admin/js/list_filter_collaps.js', ]
    fields = ('course','semester','program','guest_faculty','lecture_rate_used','lecture_honorarium','mid_sem_qp_rate_used','compre_qp_rate_used','qp_honorarium','mid_sem_eval_rate_used','compre_eval_rate_used','assignment_eval_rate_used','evaluation_honorarium','dissertation_rate_used','dissertation_honorarium','course_type_section_location_honorarium','manualy_calculated_flag','course_type_rate_used','total_honorarium','additional_teaching_honorarium',)   
    list_display = ('course1','semester1','guestfaculty1','honorarium1','lecture1','qphonorarium1','evaluationhonorarium1','dissertationhonorarium1','teachinghonorarium1','totalhonorarium1',)
    list_filter = ('course','semester','program','guest_faculty',)

    def save_model(self, request, obj, form, change):
        obj.last_updated_on=datetime.datetime.now()
        obj.last_updated_by=request.user.id 
        obj.save()

    def get_queryset(self, request):
        qs = super(GuestFacultyHonorariumAdmin, self).get_queryset(request)
        if  request.user.is_superuser:
            return qs

    def has_add_permission(self, request, obj=None):
        return True	

admin.site.register(GuestFacultyHonorarium,GuestFacultyHonorariumAdmin)













