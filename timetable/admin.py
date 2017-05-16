from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import datetime
from django.db.models import Q,F
from django import forms
from .models import Batch
from .models import Organization
from .models import SemesterMilestone
from .models import SemesterPlanDetail
from .models import SemesterPlanDetail1
from .models import SemesterTimetableEditWindow
from .models import SemesterMilestonePlanMaster
from .models import SemesterMilestonePlanMaster1
#from django_object_actions import DjangoObjectActions
from django_object_actions import (DjangoObjectActions, takes_instance_or_queryset)
#from django_object_actions import BaseDjangoObjectActions
from django_object_actions import (BaseDjangoObjectActions, takes_instance_or_queryset)
from import_export import resources
from facultyapp.models import Semester,CourseLocationSemesterDetail,Coordinator,Location,Program,Course,Discipline,Degree
from django.core.exceptions import MultipleObjectsReturned
from django.template.loader import render_to_string
from django.template import Context
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django_object_actions import DjangoObjectActions
from django.shortcuts import get_object_or_404
from django.db import Error
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.forms import TextInput, ModelForm, Textarea, Select
#from django.db import IntegrityError,transaction
from django.db import IntegrityError, transaction
from django.db.utils import OperationalError, ProgrammingError
from django.forms.models import BaseInlineFormSet
from django.forms.widgets import Widget
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.db import models
from django.forms import TextInput, Textarea
from django.db import models
from import_export.admin import ExportMixin, ImportMixin, ImportExportMixin
from import_export import fields,widgets
from import_export.widgets import ForeignKeyWidget, BooleanWidget
from django.utils.formats import get_format
from django.utils.dateformat import DateFormat
from django.utils import formats
from django.utils.translation import gettext as _

from django.contrib.admin import ModelAdmin, SimpleListFilter

from django.contrib.admin import RelatedFieldListFilter

from django.shortcuts import get_object_or_404





DELETION_FIELD_NAME = 'DELETE'

STATUS_LIST = (
    ('Created', 'Created'),
    ('Approved', 'Approved'),
    ('In Process', 'In Process'),	
    ('Rejected', 'Rejected'),
    ('Submitted','Submitted'),
    ('Escalated','Escalated'),
    ('Escalated/In Process','Escalated/In Process')
)
CHOICES=[('Default','Default'),
         ('Optional','Optional')]

class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_id','batch_name','admission_year','expected_grad_year','total_admission_strength')
    list_display_links = ('batch_name',)
admin.site.register(Batch, BatchAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_id','organization_name','organization_long_name','start_year')
    list_display_links = ('organization_name',)
	
admin.site.register(Organization, OrganizationAdmin)
class SemesterMilestoneAdminAdminForm(forms.ModelForm):
    milestone_type=forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    def clean(self):
      
        is_editable_by_owner=self.cleaned_data['is_editable_by_owner']
        if is_editable_by_owner==None:
            raise forms.ValidationError("Is Editable By Owner cannot be Unknown")
        
class SemesterMilestoneAdmin(admin.ModelAdmin):
    form =SemesterMilestoneAdminAdminForm
    list_display = ('milestone_id','milestone_short_name','milestone_long_name','milestone_type','max_duration_in_days')
    list_display_links = ('milestone_short_name',)
    fields = ('milestone_short_name','milestone_long_name','milestone_type','is_editable_by_owner','active','max_duration_in_days') 
    
admin.site.register(SemesterMilestone,SemesterMilestoneAdmin)
class EditResource(resources.ModelResource):
    location = fields.Field(column_name='location', attribute='location', widget=ForeignKeyWidget(Location, 'location_name'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'program_name'))
    class Meta:
        model = SemesterTimetableEditWindow
        fields = ('id','semester_id','status','program','location','timetable_owner','dealine_creation_date','daeadline_submission_date','deadline_approval_date')   
        import_id_fields = ['program','location','semester',]
        export_order=('id','semester_id','status','program','location','timetable_owner','dealine_creation_date','daeadline_submission_date','deadline_approval_date',)


class SemesterTimetableEditWindowAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SemesterTimetableEditWindowAdminForm, self).__init__(*args, **kwargs)
        choices = [self.fields['program'].choices.__iter__().next()]
        for program in self.fields['program'].queryset:
            choices.append(
                (program.program_id,''.join([program.program_code+'-', program.program_name]))
            )
        self.fields['program'].choices = choices
    def clean(self):      
        if  self.instance.pk:
            if self.data.get("deadline_approval_date") < self.data.get("dealine_creation_date"):
                raise forms.ValidationError("Dead line approval date should be greater than dead line creation date ")
            if self.data.get("daeadline_submission_date") < self.data.get("dealine_creation_date"):
                raise forms.ValidationError("Dead line submission date should be greater than dead line creation date ")
        if not self.instance.pk:
            if self.data.get("deadline_approval_date") < self.data.get("dealine_creation_date"):
                raise forms.ValidationError("Dead line approval date should be greater than dead line creation date ")
            if self.data.get("daeadline_submission_date") < self.data.get("dealine_creation_date"):
                raise forms.ValidationError("Dead line submission date should be greater than dead line creation date ")
 

class SemesterTimetableEditWindowAdmin(ImportExportMixin,admin.ModelAdmin):
    form = SemesterTimetableEditWindowAdminForm
    model = SemesterTimetableEditWindow
    resource_class = EditResource
    list_display = ('id','semester_id','status','program1','program','location','timetable_owner','dealine_creation_date','daeadline_submission_date','deadline_approval_date')
    readonly_fields = ('last_updated_on','last_updated_by',)
    list_editable = ('status',)
    list_display_links =('id',)	
    #list_editable = (status)
    def save_model(self, request, obj, form, change): 
        obj.last_updated_on = datetime.datetime.now()
        try:
            obj.save()
        except IntegrityError,OperationalError:
            message_bit = "This combination of semester,program,location"
            self.message_user(request, "%s Record exits ." % message_bit)
        
           
admin.site.register(SemesterTimetableEditWindow, SemesterTimetableEditWindowAdmin)


class GFResource(resources.ModelResource):
    class Meta:
        model = SemesterMilestonePlanMaster

class PlanResource(resources.ModelResource):

    #course = fields.Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    location = fields.Field(column_name='location', attribute='location', widget=ForeignKeyWidget(Location, 'location_name'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    discipline = fields.Field(column_name='discipline', attribute='discipline', widget=ForeignKeyWidget(Discipline, 'discipline_long_name'))
    degree = fields.Field(column_name='degree', attribute='degree', widget=ForeignKeyWidget(Degree, 'degree_short_name'))
    batch = fields.Field(column_name='batch', attribute='batch', widget=ForeignKeyWidget(Batch, 'batch_name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'program_name'))
    
    #client_organization = fields.Field(column_name='client_organization', attribute='client_organization', widget=ForeignKeyWidget(Organization, 'organization_name'))
    milestone_plan_owner= fields.Field(column_name='milestone_plan_owner', attribute='milestone_plan_owner', widget=ForeignKeyWidget(Coordinator, 'coordinator_name'))
    secondary_owner= fields.Field(column_name='secondary_owner', attribute='secondary_owner', widget=ForeignKeyWidget(Coordinator, 'coordinator_name'))
      
    
    #delete = fields.Field(widget=widgets.BooleanWidget())
    
    class Meta:
        model = SemesterMilestonePlanMaster
        #fields = ('location')
        fields = ('location','version_number','semester_plan_name','timetable_status','timetable_comments','degree','program','semester','batch','client_organization','discipline','milestone_plan_owner','secondary_owner','mode_of_delivery','registration_completed_in_wilp','student_strength','approval_rejection_comments','escalation_comments')   
        import_id_fields = ['location','degree','program','semester','batch','client_organization','discipline','semester_plan_name','milestone_plan_owner',]
		


def send_gfemail(emailid, mailtemplate,mailtitle,c):
    msg_plain = render_to_string('%s' %mailtemplate, c)
    send_mail(mailtitle, msg_plain, settings.EMAIL_HOST_USER, emailid, fail_silently=True)	
    return True


class SemesterPlanDetailInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super(SemesterPlanDetailInlineFormset, self).clean()
        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            data = form.cleaned_data
            sem = data.get('semester_milestone',0)
            eventdate=data.get('event_date',0)
            startdate=data.get('start_date',0)
            enddate=data.get('end_date',0)
            is_milestone=data.get('is_milestone',0)
            
            if sem==0:
                raise forms.ValidationError('Please select the milestone')
            #if eventdate==None:                        
                #raise forms.ValidationError('Please select the milestone event date')
            if SemesterMilestone.objects.filter(milestone_short_name=sem,is_duration_milestone=1):
                if is_milestone!=True:
                    raise forms.ValidationError('Please Check Is Duration Milestone as there is check for Is Duration Milestone at Milestone Masters')
                if eventdate!=None:
                    raise forms.ValidationError('Event Dates cannot be entered for duration milestones')
            if SemesterMilestone.objects.filter(milestone_short_name=sem,is_duration_milestone=0):
                if is_milestone!=False:
                    raise forms.ValidationError('Please Uncheck Is Duration Milestone as there is no check for Is Duration Milestone at Milestone Masters')
                if startdate!=0:
                    raise forms.ValidationError('Start and End Dates cannot be entered for event milestones')
                if enddate!=0:
                    raise forms.ValidationError('Start and End Dates cannot be entered for event milestones')
                if startdate!=0 and enddate!=0:
                    raise forms.ValidationError('Start and End Dates cannot be entered for event milestones')


class ReadOnlyInput(Widget):

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type='hidden',
                                       name=name, value=value)
        return format_html('<input{} />{}', flatatt(final_attrs), value)

class SemesterPlanDetailAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SemesterPlanDetailAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['semester_milestone'].widget = ReadOnlyInput()
            #self.fields['event_date'].widget = ReadOnlyInput()



class SemesterPlanDetailInline(admin.TabularInline):
    formset = SemesterPlanDetailInlineFormset
    form=SemesterPlanDetailAdminForm
    model = SemesterPlanDetail
    template = "admin/tabular.html"
    extra = 0
    verbose_name_plural = 'Semester PlanDetails'
    fields = ['semester_milestone','event_date','milestone_comments']
    #readonly_fields = ('event_date',)


class SemesterMilestonePlanMasterAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SemesterMilestonePlanMasterAdminForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            choices = [self.fields['program'].choices.__iter__().next()]
            for program in self.fields['program'].queryset:
                choices.append(
                    (program.program_id,''.join([program.program_code+'-', program.program_name]))
                )
            self.fields['program'].choices = choices

    def clean(self):
        # If Insert then check the following validation 
        if not self.instance.pk:
            mydate=[]
            sem1=self.cleaned_data.get('semester')
            loc1=self.cleaned_data.get('location')
            prg1=self.cleaned_data.get('program')
            
            # Check if Open Window Plan and allow entry
            semdat1=SemesterTimetableEditWindow.objects.values('dealine_creation_date').filter(status='Open',semester=sem1,program=prg1,location=loc1).values('deadline_approval_date')
            semdat2=SemesterTimetableEditWindow.objects.values('deadline_approval_date').filter(status='Open',semester=sem1,program=prg1,location=loc1).values('deadline_approval_date')
            open_check = SemesterTimetableEditWindow.objects.filter(status='Open',semester=self.cleaned_data.get('semester'),program=self.cleaned_data.get('program'),location=self.cleaned_data.get('location'),dealine_creation_date__lte=semdat2).count()
            #print open_check
            if open_check < 1:
                raise forms.ValidationError("The timetable for the location, program combination is not allowed as the edit window might be closed or you do not have suitable rights.")



def timetable_action(obj):
    if SemesterTimetableEditWindow.objects.filter(daeadline_submission_date__lt=datetime.datetime.today(),location=obj.location,program=obj.program,semester=obj.semester).exists():
        if obj.timetable_status != "Submitted" and obj.timetable_status != "Approved" and obj.timetable_status != "Rejected":
            return "Delayed. Timetable should be Submitted for approval by now"
    if SemesterTimetableEditWindow.objects.filter(deadline_approval_date__lt=datetime.datetime.today(),location=obj.location,program=obj.program,semester=obj.semester).exists():
        if obj.timetable_status != "Approved" and obj.timetable_status != "Rejected":    
            return "Delayed. Timetable should be Approved by now"
    elif obj.timetable_status == "": 
        return "Not Created"
timetable_action.short_description = 'Submission Status' 


class SemesterMilestonePlanMasterAdmin(ImportExportMixin,DjangoObjectActions,admin.ModelAdmin):
    template = "/admin/timetable/change_list.html"
    print template
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
        template = "/admin/timetable/change_list.html"
        print template
 
    resource_class = PlanResource
    form = SemesterMilestonePlanMasterAdminForm
    inlines = (SemesterPlanDetailInline,)
    search_fields = ('semester_plan_name', 'client_organization__organization_name', 'milestone_plan_owner__coordinator_name', 'secondary_owner__coordinator_name', 'batch__batch_name', 'program__program_name', 'discipline__discipline_long_name', 'mode_of_delivery',)
    #search_fields = ('username', 'first_name', 'last_name', 'email')
    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if isinstance(inline, SemesterPlanDetailInline) and obj is None:
                continue
            yield inline.get_formset(request, obj), inline

    model=SemesterMilestonePlanMaster
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
    }

    fields = (('program_code1','semester_plan_name','timetable_status','timetable_comments',('location','degree'),('program','semester'),('batch','client_organization'),('discipline','milestone_plan_owner'),('secondary_owner','mode_of_delivery'),('registration_completed_in_wilp','student_strength')))   
    list_display = ('semester_plan_name','timetable_status','client_organization','location_id','program1','program','milestone_plan_owner_id','secondary_owner_id','last_updated_date',timetable_action)
    readonly_fields = ('timetable_status','program_code1',)
    list_filter = ('semester','program','timetable_status','milestone_plan_owner_id','secondary_owner_id',('location',admin.RelatedOnlyFieldListFilter))
    list_display_links = ('semester_plan_name',)
    #objectactions = ('semtimetable',)
    #objectactions = [make_published]
    objectactions = ('submit_plan_for_review','approve_plan','reject_plan','escalated_plan_for_review','escalated')
    def get_form(self, request, obj=None, **kwargs):
        form = super(SemesterMilestonePlanMasterAdmin, self).get_form(request, obj, **kwargs)
        print form
        return form
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            # Check if Open record with Date range validity exists in time table edit Window and allow Edit of the Record
            open_check = SemesterTimetableEditWindow.objects.filter(status='Open',semester=obj.semester,program=obj.program,location=obj.location).count()
            if open_check > 0 and obj.current_version_flag == 1:
                return self.readonly_fields + ('semester','program','location','status','degree','client_organization','batch','discipline','mode_of_delivery')
            else:			
                return ['program_code1','timetable_status','semester_plan_name','semester','degree','program','discipline','batch', 'client_organization','created_date','timetable_status','semester_plan_name','location','created_date','student_strength']                		# This is for All fields
        else:
            return self.readonly_fields + ('milestone_plan_owner',)		
        return self.readonly_fields
    def save_model(self, request, obj, form, change):
        # Allow edits/saves only on current record
        if change and obj.current_version_flag == 1:
            print obj.program.program_code
            obj.program_code1=obj.program.program_code                    
            if obj.timetable_status == "Approved":
                obj.current_version_flag = 0;
                obj.save(update_fields=['current_version_flag'])
                gsmpm= SemesterMilestonePlanMaster(program_code1=obj.program.program_code,version_number=obj.version_number+1,semester_plan_name=obj.semester_plan_name,created_date=datetime.datetime.now(),last_updated_date=datetime.datetime.now(),last_update_by=request.user.id,timetable_status="In Process",current_version_flag=1,timetable_comments=obj.timetable_comments,location=obj.location,degree=obj.degree,program=obj.program,semester=obj.semester,batch=obj.batch,client_organization=obj.client_organization,discipline=obj.discipline,milestone_plan_owner=obj.milestone_plan_owner,secondary_owner=obj.secondary_owner,mode_of_delivery=obj.mode_of_delivery,registration_completed_in_wilp=obj.registration_completed_in_wilp,student_strength=obj.student_strength,approved_rejected_date=datetime.datetime.now(),approved_rejected_by=request.user.id,approval_rejection_comments=obj.approval_rejection_comments,escalated_on_date=datetime.datetime.now(),escalated_by=request.user.id,escalation_comments=obj.escalation_comments)
                gsmpm.save()
                if SemesterMilestone.objects.filter(milestone_type='Default',active='1',is_duration_milestone='1'):
                    mil_typ=SemesterMilestone.objects.filter(milestone_type='Default',active='1',is_duration_milestone='1')
                    for cq in mil_typ:
                        mp=SemesterPlanDetail(semester_milestone_plan_master=gsmpm,version_number=obj.version_number+1,semester_milestone=cq,start_date=datetime.datetime.today(),end_date=datetime.datetime.today(),event_date=None,date_editable='1',is_milestone=True,system_populated_date='0',created_by=request.user,created_date=datetime.datetime.today(),milestone_comments=obj.timetable_comments,last_updated_by=request.user,last_updated_date=datetime.datetime.today())
	                mp.save()
                if SemesterMilestone.objects.filter(milestone_type='Default',active='1',is_duration_milestone='0'):
                    mil_typ=SemesterMilestone.objects.filter(milestone_type='Default',active='1',is_duration_milestone='0')
                    for cq in mil_typ:
                        mp1=SemesterPlanDetail(semester_milestone_plan_master=gsmpm,version_number=obj.version_number+1,semester_milestone=cq,start_date=None,end_date=None,event_date=None,date_editable='1',is_milestone=False,system_populated_date='0',created_by=request.user,created_date=datetime.datetime.today(),milestone_comments=obj.timetable_comments,last_updated_by=request.user,last_updated_date=datetime.datetime.today())
	                mp1.save()


            elif obj.timetable_status == "Submitted":
                obj.timetable_status="Submitted"
                obj.created_date = datetime.datetime.now()
                obj.last_update_by = request.user.id
                obj.last_updated_date = datetime.datetime.now()
                obj.current_version_flag=1
                obj.approved_rejected_date=datetime.datetime.now()
                obj.escalated_on_date=datetime.datetime.now()
                obj.approved_rejected_by=request.user.id
                obj.save()
            elif obj.timetable_status == "Escalated":
                obj.timetable_status="Escalated/In Process"
                obj.created_date = datetime.datetime.now()
                obj.last_update_by = request.user.id
                obj.last_updated_date = datetime.datetime.now()
                obj.current_version_flag=1
                obj.approved_rejected_date=datetime.datetime.now()
                obj.escalated_on_date=datetime.datetime.now()
                obj.approved_rejected_by=request.user.id
                obj.save()
            elif obj.timetable_status == "Escalated/In Process":
                obj.timetable_status="Escalated/In Process"
                obj.created_date = datetime.datetime.now()
                obj.last_update_by = request.user.id
                obj.last_updated_date = datetime.datetime.now()
                obj.current_version_flag=1
                obj.approved_rejected_date=datetime.datetime.now()
                obj.escalated_on_date=datetime.datetime.now()
                obj.approved_rejected_by=request.user.id
                obj.save()
            elif obj.timetable_status == "Rejected":
                obj.timetable_status="Rejected"
                obj.created_date = datetime.datetime.now()
                obj.last_update_by = request.user.id
                obj.last_updated_date = datetime.datetime.now()
                obj.current_version_flag=1
                obj.approved_rejected_date=datetime.datetime.now()
                obj.escalated_on_date=datetime.datetime.now()
                obj.approved_rejected_by=request.user.id
                obj.save()
            else:
                obj.timetable_status="In Process"
                obj.created_date = datetime.datetime.now()
                obj.last_update_by = request.user.id
                obj.last_updated_date = datetime.datetime.now()
                obj.current_version_flag=1
                obj.approved_rejected_date=datetime.datetime.now()
                obj.escalated_on_date=datetime.datetime.now()
                obj.approved_rejected_by=request.user.id
                obj.save()
                """if SemesterMilestone.objects.filter(milestone_type='DEFAULT',active='1',is_duration_milestone='1'):
                    mil_typ=SemesterMilestone.objects.filter(milestone_type='DEFAULT',active='1',is_duration_milestone='1')
                    for cq in mil_typ:
                        mp=SemesterPlanDetail(semester_milestone_plan_master=obj,version_number='1',semester_milestone=cq,start_date=datetime.datetime.today(),end_date=datetime.datetime.today(),event_date=None,date_editable='1',is_milestone=True,system_populated_date='0',created_by=request.user,created_date=datetime.datetime.today(),milestone_comments=obj.timetable_comments,last_updated_by=request.user,last_updated_date=datetime.datetime.today())
	                mp.save()
                if SemesterMilestone.objects.filter(milestone_type='DEFAULT',active='1',is_duration_milestone='0'):
                    mil_typ=SemesterMilestone.objects.filter(milestone_type='DEFAULT',active='1',is_duration_milestone='0')
                    for cq in mil_typ:
                        mp1=SemesterPlanDetail(semester_milestone_plan_master=obj,version_number='1',semester_milestone=cq,start_date=None,end_date=None,event_date=datetime.datetime.today(),date_editable='1',is_milestone=False,system_populated_date='0',created_by=request.user,created_date=datetime.datetime.today(),milestone_comments=obj.timetable_comments,last_updated_by=request.user,last_updated_date=datetime.datetime.today())
	                mp1.save()"""

        if not change:
            obj.timetable_status="Created"
            sem=SemesterTimetableEditWindow.objects.filter(semester=obj.semester,program=obj.program,location=obj.location).values_list('timetable_owner',flat=True)
            for se in sem:
                obj.milestone_plan_owner_id=se
            obj.created_date = datetime.datetime.now()
            obj.last_update_by = request.user
            obj.last_updated_date = datetime.datetime.now()
            obj.current_version_flag=1
            obj.approved_rejected_date=datetime.datetime.now()
            obj.escalated_on_date=datetime.datetime.now()
            obj.approved_rejected_by=request.user
            obj.program_code1=obj.program.program_code
            obj.save()
            if SemesterMilestone.objects.filter(milestone_type='Default',active='1',is_duration_milestone='1'):
                mil_typ=SemesterMilestone.objects.filter(milestone_type='Default',active='1',is_duration_milestone='1')
                for cq in mil_typ:
                    mp=SemesterPlanDetail(semester_milestone_plan_master=obj,version_number='1',semester_milestone=cq,start_date=datetime.datetime.today(),end_date=datetime.datetime.today(),event_date=None,date_editable='1',is_milestone=True,system_populated_date='0',created_by=request.user,created_date=datetime.datetime.today(),milestone_comments=obj.timetable_comments,last_updated_by=request.user,last_updated_date=datetime.datetime.today())
	            mp.save()
            if SemesterMilestone.objects.filter(milestone_type='Default',active='1',is_duration_milestone='0'):
                mil_typ=SemesterMilestone.objects.filter(milestone_type='Default',active='1',is_duration_milestone='0')
                for cq in mil_typ:
                    mp1=SemesterPlanDetail(semester_milestone_plan_master=obj,version_number='1',semester_milestone=cq,start_date=None,end_date=None,event_date=None,date_editable='1',is_milestone=False,system_populated_date='0',created_by=request.user,created_date=datetime.datetime.today(),milestone_comments=obj.timetable_comments,last_updated_by=request.user,last_updated_date=datetime.datetime.today())
	            mp1.save()
            template = 'createdemail.txt'
            c=Context({'username': request.user.username, 'application_url':settings.APPLICATION_URL,'degree':obj.degree,'location':obj.location,'batch':obj.batch,'program':obj.program,'semester':obj.semester,'organization':obj.client_organization,'discipline':obj.discipline})                    
            send_gfemail([request.user.email],template,'Re: BITS Guest Faculty Application',c) 					
                
            plural = ''
            count=1
            if count == 1:
                plural = 's'
            self.message_user(request, "Created %d timetable%s." % (count, plural))
            return "<script>window.history.back();</script>"
    def get_queryset(self, request):
        qs = super(SemesterMilestonePlanMasterAdmin, self).get_queryset(request)
        #qs.update()
        if request.user.is_superuser :
            return qs.filter(current_version_flag=1)
        elif  request.user.is_staff and request.user.groups.filter(name__in=['coordinator']):
            return qs.filter(Q(milestone_plan_owner=request.user.id) | Q(secondary_owner=request.user.id)).filter(Q(timetable_status="In Process") | Q(timetable_status="Submitted") | Q(timetable_status="Escalated/In Process") | Q(timetable_status="Created") | Q(timetable_status="Escalated"))
        elif request.user.groups.filter(name__in=['offcampusadmin']):
            return qs.filter(current_version_flag=1).filter(Q(timetable_status="In Process") | Q(timetable_status="Submitted") | Q(timetable_status="Escalated/In Process") | Q(timetable_status="Created") | Q(timetable_status="Escalated") | Q(timetable_status="Approved") | Q(timetable_status="Rejected"))    
        else :
            return qs.filter(current_version_flag=1)


    class SubmitPlanforReviewForm(forms.Form):
        submission_comments = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': '30','rows' : '5'}))
		
    def submit_plan_for_review(self, request, obj):
        form = None
        if 'update' in request.POST:
            form = self.SubmitPlanforReviewForm(request.POST)
            if form.is_valid():
                count=1
                submission_comments = form.cleaned_data['submission_comments']
                obj.approval_rejection_comments = submission_comments
                obj.timetable_status='Submitted'
                obj.save()
                template = 'submittedemail.txt'
                c = Context({'username': request.user.username, 'application_url':settings.APPLICATION_URL,'degree':obj.degree,'location':obj.location,'batch':obj.batch,'program':obj.program,'semester':obj.semester,'organization':obj.client_organization,'discipline':obj.discipline,'comments':submission_comments})                    
                send_gfemail([request.user.email],template,'Re: BITS Guest Faculty Application',c) 					
                
                plural = ''
                if count == 1:
                    plural = 's'
                self.message_user(request, "Submitted %d timetable%s." % (count, plural))
                count1=0
                group = Group.objects.get(name="offcampusadmin")
                usersList = group.user_set.all().values_list("email",flat=True)
                for email in usersList:
                    count1 += 1
                    template = 'submittedemail.txt'
                    c = Context({'username': request.user.username, 'application_url':settings.APPLICATION_URL,'degree':obj.degree,'location':obj.location,'batch':obj.batch,'program':obj.program,'semester':obj.semester,'organization':obj.client_organization,'discipline':obj.discipline,'comments':submission_comments})                    
                    send_gfemail([email],template,'Re: BITS Guest Faculty Application',c)
                plural = ''
                if count1 == 1:
                    plural = 's'
                self.message_user(request, "Submitted %d timetable%s." % (count1, plural))
                return "<script>window.history.back();</script>" 

        if not form:
            form = self.SubmitPlanforReviewForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
  
        data = {'plan': obj,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/submit_plan_for_review.html', data)
				
    submit_plan_for_review.short_description = "Submit for Review"
    submit_plan_for_review.label = "Submit for Review"
    class EscalatedPlanforReviewForm(forms.Form):
        escalation_comments = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': '30','rows' : '5'}))

    def escalated_plan_for_review(self, request, obj):
        form = None
        if 'update' in request.POST:
            form = self.EscalatedPlanforReviewForm(request.POST)
            if form.is_valid():
                count = 1
                escalation_comments = form.cleaned_data['escalation_comments']
                obj.escalation_comments = escalation_comments
                obj.timetable_status='Escalated/In Process'
                obj.escalated_on_date=datetime.datetime.now()
                obj.escalated_by=request.user.id
                obj.save()
                template = 'escalatedemail.txt'
                c = Context({'username': request.user.username, 'application_url':settings.APPLICATION_URL,'degree':obj.degree,'location':obj.location,'batch':obj.batch,'program':obj.program,'semester':obj.semester,'organization':obj.client_organization,'discipline':obj.discipline,'comments':escalation_comments})                    
                send_gfemail([request.user.email],template,'Re: BITS Guest Faculty Application',c) 					
                
                plural = ''
                if count == 1:
                    plural = 's'
                self.message_user(request, "Successfully Escalated %d timetable%s." % (count, plural))
                return "<script>window.history.back();</script>"

        if not form:
            form = self.EscalatedPlanforReviewForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        data = {'plan':obj,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/escalated_plan_for_review.html', data)
				
    escalated_plan_for_review.short_description = "Escalate"
    escalated_plan_for_review.label = "Escalate"

    class ApprovePlanForm(forms.Form):
        approve_comments = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': '30','rows' : '5'}))
    def approve_plan(self, request, obj):
        form = None
        if 'update' in request.POST:
            form = self.ApprovePlanForm(request.POST)
            if form.is_valid():
                count=1
                approve_comments = form.cleaned_data['approve_comments']
                obj.timetable_status='Approved'
                obj.approval_rejection_comments = approve_comments
                obj.approved_rejected_date = datetime.datetime.now()
                obj.approved_rejected_by=request.user.id
                obj.save()
                template = 'approvedemail.txt'
                c = Context({'username': request.user.username, 'application_url':settings.APPLICATION_URL,'location':obj.location,'batch':obj.batch,'program':obj.program,'semester':obj.semester,'organization':obj.client_organization,'discipline':obj.discipline,'degree':obj.degree,'comments':approve_comments})                     
                send_gfemail([request.user.email],template,'Re: BITS Guest Faculty Application',c) 					
                
                plural = ''
                if count == 1:
                    plural = 's'
                self.message_user(request, "Successfully Approved %d timetable%s." % (count, plural))
                count1=0
                group = Group.objects.get(name="offcampusadmin")
                usersList = group.user_set.all().values_list("email",flat=True)
                for email in usersList:
                    count1 += 1
                    template = 'approvedemail.txt'
                    c = Context({'username': request.user.username, 'application_url':settings.APPLICATION_URL,'degree':obj.degree,'location':obj.location,'batch':obj.batch,'program':obj.program,'semester':obj.semester,'organization':obj.client_organization,'discipline':obj.discipline,'comments':approve_comments})                    
                    send_gfemail([email],template,'Re: BITS Guest Faculty Application',c)
                plural = ''
                if count1 == 1:
                    plural = 's'
                self.message_user(request, "Successfully Approved %d timetable%s." % (count1, plural))
                return "<script>window.history.back();</script>"

        if not form:
            form = self.ApprovePlanForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        data = {'plan':obj,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/approve_plan.html', data)
    approve_plan.short_description = "Approved"
    approve_plan.label = "Approved"

    class RejectPlanForm(forms.Form):
        reject_comments = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': '30','rows' : '5'}))
		
    def reject_plan(self, request, obj):
        form = None
        if 'update' in request.POST:
            form = self.RejectPlanForm(request.POST)
            if form.is_valid():
                count=1
                reject_comments = form.cleaned_data['reject_comments']
                obj.timetable_status='Rejected'
                obj.approval_rejection_comments = reject_comments
                obj.approved_rejected_date = datetime.datetime.now()
                obj.approved_rejected_by=request.user.id
                obj.save()
                template = 'rejectedemail.txt'
                c = Context({'username': request.user.username, 'application_url':settings.APPLICATION_URL,'degree':obj.degree,'location':obj.location,'batch':obj.batch,'program':obj.program,'semester':obj.semester,'organization':obj.client_organization,'discipline':obj.discipline,'comments':reject_comments})                    
                send_gfemail([request.user.email],template,'Re: BITS Guest Faculty Application',c) 					
                
                plural = ''
                if count == 1:
                    plural = 's'
                self.message_user(request, "Successfully Rejected %d timetable%s." % (count, plural))
                count1=0
                group = Group.objects.get(name="offcampusadmin")
                usersList = group.user_set.all().values_list("email",flat=True)
                for email in usersList:
                    count1 += 1
                    template = 'rejectedemail.txt'
                    c = Context({'username': request.user.username, 'application_url':settings.APPLICATION_URL,'degree':obj.degree,'location':obj.location,'batch':obj.batch,'program':obj.program,'semester':obj.semester,'organization':obj.client_organization,'discipline':obj.discipline,'comments':reject_comments})                    
                    send_gfemail([email],template,'Re: BITS Guest Faculty Application',c)
                plural = ''
                if count1 == 1:
                    plural = 's'
                self.message_user(request, "Successfully Rejected %d timetable%s." % (count1, plural))
                return "<script>window.history.back();</script>"

        if not form:
            form = self.RejectPlanForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
  
        data = {'plan': obj,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/reject_plan.html', data)
				
    reject_plan.short_description = "Rejected"
    reject_plan.label = "Rejected"
    class EscalatedForm(forms.Form):
        escalation_comments = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': '30','rows' : '5'}))
    def escalated(self, request, obj):
        form = None
        if 'update' in request.POST:
            form = self.EscalatedForm(request.POST)
            if form.is_valid():
                count = 1
                escalation_comments = form.cleaned_data['escalation_comments']
                obj.escalation_comments = escalation_comments
                obj.timetable_status='Escalated'
                obj.escalated_on_date=datetime.datetime.now()
                obj.escalated_by=request.user.id
                obj.save()
                template = 'escalatedemail.txt'
                c = Context({'username': request.user.username, 'application_url':settings.APPLICATION_URL,'degree':obj.degree,'location':obj.location,'batch':obj.batch,'program':obj.program,'semester':obj.semester,'organization':obj.client_organization,'discipline':obj.discipline,'comments':escalation_comments})                     
                send_gfemail([request.user.email],template,'Re: BITS Guest Faculty Application',c) 					
                
                plural = ''
                if count == 1:
                    plural = 's'
                self.message_user(request, "Successfully Escalated %d timetable%s." % (count, plural))
                return "<script>window.history.back();</script>"

        if not form:
            form = self.EscalatedForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        data = {'plan':obj,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/escalated_plan_for_review.html', data)
				
    escalated.short_description = "escalate"
    escalated.label = "escalate"

    def get_object_actions(self, request, context, **kwargs):
        objectactions = []
        obj = context['original']		
        if obj:
            if request.user.is_superuser:
                if SemesterTimetableEditWindow.objects.filter(daeadline_submission_date__lt=datetime.datetime.today(),location=obj.location,program=obj.program,semester=obj.semester).exists():
                    if obj.timetable_status=="Created" and obj.current_version_flag== 1:
                        objectactions.extend(['escalated',])
                if SemesterTimetableEditWindow.objects.filter(daeadline_submission_date__lt=datetime.datetime.today(),location=obj.location,program=obj.program,semester=obj.semester).exists():
                    if obj.timetable_status=="In Process" and obj.current_version_flag==1:
                        objectactions.extend(['escalated_plan_for_review',])
                    elif obj.timetable_status=="In Process" or obj.timetable_status=="Escalated/In Process" and obj.current_version_flag==1:
                        objectactions.extend(['submit_plan_for_review',])
                    elif  obj.timetable_status=="Submitted" and obj.current_version_flag==1:
                        objectactions.extend(['approve_plan',])
                        objectactions.extend(['reject_plan',])

                elif obj.timetable_status=="In Process" or obj.timetable_status=="Escalated/In Process" and obj.current_version_flag==1:
                        objectactions.extend(['submit_plan_for_review',])
                elif obj.timetable_status=="Submitted":
                    objectactions.extend(['approve_plan',])
                    objectactions.extend(['reject_plan',])
            elif request.user.is_staff and request.user.groups.filter(name__in=['coordinator']).exists():

                if obj.timetable_status=="In Process" or obj.timetable_status=="Escalated/In Process" and obj.current_version_flag==1:
                    objectactions.extend(['submit_plan_for_review',])

            elif request.user.groups.filter(name__in=['offcampusadmin']):
                if SemesterTimetableEditWindow.objects.filter(daeadline_submission_date__lt=datetime.datetime.today(),location=obj.location,program=obj.program,semester=obj.semester).exists():
                    if obj.timetable_status=="Created" and obj.current_version_flag== 1:
                        objectactions.extend(['escalated',])
                if SemesterTimetableEditWindow.objects.filter(daeadline_submission_date__lt=datetime.datetime.today(),location=obj.location,program=obj.program,semester=obj.semester).exists():
                    if obj.timetable_status=="In Process" and obj.current_version_flag==1:
                        objectactions.extend(['escalated_plan_for_review',])
                    elif obj.timetable_status=="Submitted":
                        objectactions.extend(['approve_plan',])
                        objectactions.extend(['reject_plan',])
                elif obj.timetable_status=="Submitted":
                    objectactions.extend(['approve_plan',])
                    objectactions.extend(['reject_plan',])
        return objectactions
admin.site.register(SemesterMilestonePlanMaster, SemesterMilestonePlanMasterAdmin)


"""class SemesterPlanDetailAdminForm(forms.ModelForm):
    def clean(self):
        # If Insert then check the following validation	
        if not self.instance.pk:
            # Check if Open Window timetableedit and allow entry
            if SemesterMilestone.objects.filter(milestone_short_name=self.cleaned_data.get('semester_milestone'),is_duration_milestone__gt=0).exists():
                start_date= self.cleaned_data['start_date']
                end_date=self.cleaned_data['end_date']
                date =end_date-start_date
                duration=SemesterMilestone.objects.values_list("is_duration_milestone",flat=True)
                if end_date<start_date and  date>duration:
                    raise forms.ValidationError("Please Check Start Date and End Date")"""

class SemesterPlanDetailAdmin(admin.ModelAdmin):
    #form = SemesterPlanDetailAdminForm
    fields = ('semester_milestone_plan_master','version_number','semester_milestone','start_date','end_date','event_date','date_editable','is_milestone','system_populated_date','milestone_comments',)   
    list_display = ('semester_milestone_plan_master','version_number','semester_milestone','start_date','end_date','event_date','is_milestone',)
    list_display_links = ('semester_milestone_plan_master',)
    readonly_fields = ('version_number',)
    
    def has_add_permission(self, request, obj=None):
        return False
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            # Check if Open record with Date range validity exists in Time Table Edit Window and allow Edit of the Record
            open_check = SemesterMilestone.objects.filter(milestone_short_name=obj.semester_milestone,is_duration_milestone=1).count()
            if open_check > 0:
                
                return self.readonly_fields + ('event_date',)
            else:
                				
                return ['start_date','end_date',]			
        return self.readonly_fields
    def save_model(self, request, obj, form, change): 
        if change:
            obj.last_update_by = request.user.id
            obj.created_date=datetime.datetime.now()
            obj.last_updated_date=datetime.datetime.now()
            obj.created_by=request.user.id
            obj.save()
        if not change:
            obj.last_update_by = request.user
            obj.created_date=datetime.datetime.now()
            obj.last_updated_date=datetime.datetime.now()
            obj.created_by=request.user
            obj.save()
admin.site.register(SemesterPlanDetail,SemesterPlanDetailAdmin)
#admin.site.unregister(SemesterPlanDetail)

class  Location1(SimpleListFilter):
    title = 'Location'
    parameter_name = 'location1'

    def lookups(self, request, model_admin):
        semesters = set([s for s in Location.objects.all()])
        return [(s.location_id,s.location_name) for s in semesters]
    def queryset(self, request, queryset):
        if self.value():
            print "jajajajaj"
            return queryset.filter(location_id=self.value())    

            
 
class RelatedOnlyFieldListFilter(RelatedFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.request = request
        self.model_admin = model_admin
        super(RelatedOnlyFieldListFilter, self).__init__(field, request, params, model, model_admin, field_path)

    def choices(self, cl):
        limit_choices_to = set(self.model_admin.queryset(self.request).values_list(self.field.name, flat=True))
        self.lookup_choices = [(pk_val, val) for pk_val, val in self.lookup_choices if pk_val in limit_choices_to]
        return super(RelatedOnlyFieldListFilter, self).choices(cl)


def milestone_name(obj):
    planeven1 = SemesterMilestone.objects.filter(milestone_short_name=obj.semester_milestone,milestone_type="Default").values_list('milestone_short_name',flat=True)
    planeven3=planeven1.exists()
    if planeven3==False:
        return " "
    else:
        for planeven2 in planeven1:
            return planeven2



class SemesterMilestonePlanMasterInline(admin.TabularInline):
    #formset=SemesterPlanDetailInline1FormSet
    model = SemesterMilestonePlanMaster
    fields = ['location','batch','program']
    def has_add_permission(self, request, obj=None):
        if request.user.groups.filter(name__in=['registrant']).exists():
            return True
        else:
            return False	


class SemDataResource(resources.ModelResource):

    id=fields.Field(column_name='id', attribute='id')
    semester_milestone_plan_master=fields.Field(column_name='semester_milestone_plan_master', attribute='semester_milestone_plan_master', widget=ForeignKeyWidget(SemesterMilestonePlanMaster, 'semester_plan_name'))
    semester_milestone=fields.Field(column_name='semester_milestone', attribute='semester_milestone', widget=ForeignKeyWidget(SemesterMilestone, 'milestone_short_name'))
    location = fields.Field(column_name='location', attribute='semester_milestone_plan_master__location', widget=ForeignKeyWidget(Location, 'location_name'))
    #semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    discipline = fields.Field(column_name='discipline', attribute='semester_milestone_plan_master__discipline', widget=ForeignKeyWidget(Discipline, 'discipline_long_name'))
    #degree = fields.Field(column_name='degree', attribute='degree', widget=ForeignKeyWidget(Degree, 'degree_short_name'))
    batch = fields.Field(column_name='batch', attribute='semester_milestone_plan_master__batch', widget=ForeignKeyWidget(Batch, 'batch_name'))
    program = fields.Field(column_name='program', attribute='semester_milestone_plan_master__program', widget=ForeignKeyWidget(Program, 'program_name'))
    programcode = fields.Field(column_name='program code', attribute='semester_milestone_plan_master__program_program_code', widget=ForeignKeyWidget(Program, 'program_code'))
    client_organization = fields.Field(column_name='organization', attribute='semester_milestone_plan_master__client_organization', widget=ForeignKeyWidget(Organization, 'organization_name'))
    student_strength=fields.Field(column_name='student_strength', attribute='semester_milestone_plan_master__student_strength')
    milestone_plan_owner= fields.Field(column_name='primary owner', attribute='semester_milestone_plan_master__milestone_plan_owner', widget=ForeignKeyWidget(Coordinator, 'coordinator_name'))
    secondary_owner= fields.Field(column_name='secondary_owner', attribute='semester_milestone_plan_master__secondary_owner', widget=ForeignKeyWidget(Coordinator, 'coordinator_name'))

    class Meta:
        model = SemesterPlanDetail
        
        fields = ('id','semester_milestone_plan_master','version_number','semester_milestone','event_date','start_date','end_date','date_editable','is_milestone',
'system_populated_date','created_by','created_date','milestone_comments','last_updated_by','last_updated_date','location','program','discipline','batch',
'client_organization','student_strength','milestone_plan_owner','secondary_owner','programcode',)
        export_order=('id','program','discipline','programcode','batch','location','client_organization','student_strength','semester_milestone','event_date','semester_milestone_plan_master',
'milestone_plan_owner','secondary_owner',)

class SemesterPlanDetail1Admin(ExportMixin,admin.ModelAdmin):
    template = "change_list.html"
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
    resource_class = SemDataResource

    #inlines = (SemesterMilestonePlanMasterInline,)
    list_display = ('id','semestermilestoneplanmaster_program','semestermilestoneplanmaster_discipline','semestermilestoneplanmaster_program_code',
'semestermilestoneplanmaster_batch','semestermilestoneplanmaster_location','semestermilestoneplanmaster_client_organization',
'semestermilestoneplanmaster_student_strength','event_date','semestermilestoneplanmaster_milestone_plan_owner','semestermilestoneplanmaster_secondary_owner',)	
    list_filter = ['semester_milestone','semester_milestone_plan_master__program','semester_milestone_plan_master__discipline','semester_milestone_plan_master__location','semester_milestone_plan_master__client_organization']
    list_display_links =None



    def has_add_permission(self, request, obj=None):
        if request.user.groups.filter(name__in=['registrant']).exists():
            return True
        else:
            return False	


    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Timetable and Milestones Date report'}
        return super(SemesterPlanDetail1Admin, self).changelist_view(request, extra_context=extra_context)
		
admin.site.register(SemesterPlanDetail1, SemesterPlanDetail1Admin)
class SemesterPlanDetailInline1FormSet(BaseInlineFormSet):
    """
    Makes the delete field a hidden input rather than the default checkbox
    
    inlineformset_factory(Book, Page, formset=HiddenDeleteBaseInlineFormSet, can_delete=True)
    """
    def add_fields(self, form, index):
        super(SemesterPlanDetailInline1FormSet, self).add_fields(form, index)
        if self.can_delete:
            form.fields[DELETION_FIELD_NAME] = forms.BooleanField(
                label=_('Delete'),
                required=False,
                widget=forms.HiddenInput
            )



class SemesterPlanDetailInline1(admin.TabularInline):
    formset=SemesterPlanDetailInline1FormSet
    model = SemesterPlanDetail1
    template = "admin/tabular.html"
    extra = 0
    verbose_name_plural = 'Semester PlanDetails'
    fields = ['semester_milestone','event_date','milestone_comments']
    readonly_fields = ('semester_milestone',)
    def has_add_permission(self, request, obj=None):
        if request.user.groups.filter(name__in=['registrant']).exists():
            return True
        else:
            return False	


def event_date(obj):
    planeven = SemesterPlanDetail1.objects.filter(semester_milestone_plan_master=obj.id).values_list('event_date',flat=True)
    for peven in planeven:
        return planeven

def milestone_name(obj):
    planeven1 = SemesterPlanDetail1.objects.filter(semester_milestone_plan_master=obj.id).values_list('semester_milestone__milestone_short_name',flat=True)
    return planeven1
         

class SemesterMilestonePlanMaster1Admin(ExportMixin,admin.ModelAdmin):
    class Media:
        static_url = getattr(settings, 'STATIC_URL', '/static/') 
        js = [ static_url+'admin/js/list_filter_collaps.js', ]
  
    inlines = (SemesterPlanDetailInline1,)
    fields = (('version_number','semester_plan_name','timetable_status','timetable_comments',('location','degree'),('program','semester'),('batch','client_organization'),('discipline','milestone_plan_owner'),('secondary_owner','mode_of_delivery'),('student_strength')))   
    list_display = ('id','program','discipline','batch','location','client_organization','student_strength','milestone_plan_owner','secondary_owner','semesterplandetail1.semester_milestone',)
    ordering = ('id',)

    readonly_fields = ('version_number','timetable_status','location','degree','program','semester','batch','client_organization','discipline','mode_of_delivery',)
    list_filter = ('semester','program','milestone_plan_owner','secondary_owner','location',)

    def has_add_permission(self, request, obj=None):
        if request.user.groups.filter(name__in=['registrant']).exists():
            return True
        else:
            return False	
 
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Timetable and Milestones Date report'}
        return super(SemesterMilestonePlanMaster1Admin, self).changelist_view(request, extra_context=extra_context)
	
#admin.site.register(SemesterMilestonePlanMaster1, SemesterMilestonePlanMaster1Admin)



from models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    fields = ('employee_name','employee_id','location','gender','address')
    list_display = ('employee_name','employee_id','location','address',)
    list_filter = ('employee_name','employee_id','location',)
    radio_fields = {"gender":admin.HORIZONTAL}
    widget = {
              'address':Textarea(attrs={'cols':20,'rows':5}),
    }

admin.site.register(Employee,EmployeeAdmin)






