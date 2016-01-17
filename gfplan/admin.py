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
import math
import re, string,sys
from django.core.mail import send_mail
from django.template import Context
from django.db.models import Q,F
from django.contrib.admin.helpers import ActionForm
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import IntegrityError,transaction
from django.conf import settings
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

from import_export import resources
#from import_export.admin import ExportActionModelAdmin
#from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportMixin, ImportMixin
#from django_object_actions import DjangoObjectActions
from django_object_actions import (DjangoObjectActions, takes_instance_or_queryset)
#from django_object_actions import BaseDjangoObjectActions
from django_object_actions import (BaseDjangoObjectActions, takes_instance_or_queryset)
from django.shortcuts import get_object_or_404
from django.contrib.admin import RelatedFieldListFilter

from django.contrib.admin import AdminSite
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


from facultyapp.models import Coordinator, Course, Discipline, Location, Program, Semester, CourseLocationSemesterDetail
from .models import BufferType, GuestFacultyPlanningNumbers, PlanningWindowStatus, ApplicationUsers,CurrentSemester

from import_export import resources
#from import_export.admin import ExportActionModelAdmin
#from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportMixin, ImportMixin, ImportExportMixin
from import_export import fields,widgets
from import_export.widgets import ForeignKeyWidget, BooleanWidget



class BufferTypeAdmin(admin.ModelAdmin):
    model = BufferType
    list_display = ('buffer_calc_id','buffer_name','buffer_percentage')
admin.site.register(BufferType, BufferTypeAdmin)

class GuestFacultyPlanningNumbersAdminForm(forms.ModelForm):

    def clean(self):
        if not self.instance.pk:
            admin=self.current_user.is_superuser

            if Coordinator.objects.filter(coordinator=self.current_user.id,coordinator_for_location=self.cleaned_data.get('location')).exists():
                
                aplocation=Coordinator.objects.filter(coordinator=self.current_user.id,coordinator_for_location=self.cleaned_data.get('location')).count()
                if aplocation==0:
                    raise forms.ValidationError("User doesn't have the rights to make this plan entry")
            elif Program.objects.filter(program_coordinator=self.current_user.id,program_name=self.cleaned_data.get('program')).exists():
                approgram=Program.objects.filter(program_coordinator=self.current_user.id,program_name=self.cleaned_data.get('program')).count()
                if approgram==0:
                    raise forms.ValidationError("User doesn't have the rights to make this plan entry")
            elif admin==True:
                return
            else:
                raise forms.ValidationError("User doesn't have the rights to make this plan entry")
                      
            #check for status/semester/program
            open_check = PlanningWindowStatus.objects.filter(status='Open',semester=self.cleaned_data.get('semester'),program=self.cleaned_data.get('program'),start_date__lte=datetime.datetime.today(),end_date__gte= datetime.datetime.today()).count()
            #print open_check
            if open_check < 1:
                raise forms.ValidationError("Forecast Entry for the semester and program is not allowed as the window is closed or there no window entry made.")
  
            # Check if program/location/course/discipline/semester combination is valid and allow entry
            clsd_check = CourseLocationSemesterDetail.objects.filter(semester=self.cleaned_data.get('semester'),program=self.cleaned_data.get('program'),course=self.cleaned_data["course"],location=self.cleaned_data.get('location'),discipline=self.cleaned_data["discipline"]).count()
            #print clsd_check
            if clsd_check < 1:
                raise forms.ValidationError("The plan entry for the course, location, program, semester and discipline is incorrect. Please enter plan numbers for correct combinations only")
        		

#using customized list_filter
class  CurrentSemesterFilter(SimpleListFilter):
    title = 'currentsemester'
    parameter_name = 'currentsemester'

    def lookups(self, request, model_admin):
        semesters = set([s for s in Semester.objects.all()])
        return [(s.semester_id,s.semester_name) for s in semesters]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(semester_id=self.value())    
        elif self.value() == None:
            currentsem=CurrentSemester.objects.values_list("currentsemester",flat=True)
            return queryset.filter(semester_id=currentsem,current_plan_flag=1)
        else:
            return qs

class PlanningNumbers(resources.ModelResource):
    course = fields.Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    location = fields.Field(column_name='location', attribute='location', widget=ForeignKeyWidget(Location, 'location_name'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'program_name'))

    class Meta:
        model = GuestFacultyPlanningNumbers
	fields = ('location','program','course','semester','plan_status','faculty_in_database','total_faculty_required','to_be_recruited_with_buffer','version_number','current_plan_flag')	
	
class GuestFacultyPlanningNumbersAdmin(DjangoObjectActions,ExportMixin,admin.ModelAdmin):
    resource_class = PlanningNumbers
    form = GuestFacultyPlanningNumbersAdminForm
    #get the current user
    def get_form(self, request,obj=None, **kwargs):
         form = super(GuestFacultyPlanningNumbersAdmin, self).get_form(request,obj, **kwargs)
         form.current_user = request.user
         return form

    model = GuestFacultyPlanningNumbers
    #resource_class = PlanningNumbers
    list_display = ('id','location','program','course','semester','plan_status','buffer_number','faculty_to_be_recruited','to_be_recruited_with_buffer','version_number','current_plan_flag')
    fields = (('location','program','course'),('semester','discipline'),('faculty_in_database','total_faculty_required'),('buffer_type','buffer_number','faculty_to_be_recruited','to_be_recruited_with_buffer'),'planning_comments',('program_coordinator','plan_status'),'version_number')
    readonly_fields = ('faculty_to_be_recruited','current_plan_flag','to_be_recruited_with_buffer','buffer_number','version_number','plan_status', 'program_coordinator','created_by','created_on','version_number')
    list_filter = ('program','course',CurrentSemesterFilter,'current_plan_flag','plan_status',('location',admin.RelatedOnlyFieldListFilter))

    """def get_list_filter(self,request):
        ids=Semester.objects.values_list('semester_id',flat=True)
        if CurrentSemester.objects.filter(semester_id=ids).exists():
            #print "prathap"
            return self.list_filter + ('semester',)
        else:
            return ['program','course','current_plan_flag','plan_status',('location',admin.RelatedOnlyFieldListFilter)]"""
        
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            # Check if Open record with Date range validity exists in Plan Window and allow Edit of the Record
            open_check = PlanningWindowStatus.objects.filter(status='Open',semester=obj.semester,program=obj.program,start_date__lte=datetime.datetime.today(),end_date__gte= datetime.datetime.today()).count()
            if open_check > 0 and obj.current_plan_flag == 1:
                return self.readonly_fields + ('location','program','course','semester','discipline','version_number')
             
            else:
            	
                return ['location','program','course','semester','discipline','faculty_in_database','total_faculty_required','buffer_type','buffer_number','faculty_to_be_recruited','to_be_recruited_with_buffer','planning_comments','program_coordinator','plan_status','version_number'] # This is for All fields			
        return self.readonly_fields
           
            			
    def save_model(self, request, obj, form, change):
        # Allow edits/saves only on current record
        if change and obj.current_plan_flag == 1:
            if obj.plan_status == "Approved":
                # This is an approved record. Do not allow and updates to existing record. Set current plan flag to 0 and only save that attribute
                obj.current_plan_flag = 0;
                obj.save(update_fields=['current_plan_flag'])
                # Create a new record with new version number and latest values
                if obj.total_faculty_required>obj.faculty_in_database:
                    gfpn = GuestFacultyPlanningNumbers(program_coordinator=obj.program_coordinator,location=obj.location,course=obj.course,program=obj.program,semester=obj.semester,discipline=obj.discipline,version_number=obj.version_number+1,buffer_type=obj.buffer_type,current_plan_flag=1,plan_status="In Process",total_faculty_required=obj.total_faculty_required,faculty_in_database=obj.faculty_in_database,faculty_to_be_recruited=obj.total_faculty_required - obj.faculty_in_database,buffer_number=int(math.ceil((obj.buffer_type.buffer_percentage * (obj.total_faculty_required - obj.faculty_in_database)/100))),to_be_recruited_with_buffer=int(math.ceil((obj.buffer_type.buffer_percentage * (obj.total_faculty_required - obj.faculty_in_database)/100))) 
				+ (obj.total_faculty_required - obj.faculty_in_database),planning_comments=obj.planning_comments,created_by=request.user,created_on=datetime.datetime.now(),updated_by = request.user,last_updated_on = datetime.datetime.now())
                    gfpn.save()
                else:
                    gfpn = GuestFacultyPlanningNumbers(program_coordinator=obj.program_coordinator,location=obj.location,course=obj.course,program=obj.program,semester=obj.semester,discipline=obj.discipline,version_number=obj.version_number+1,buffer_type=obj.buffer_type,current_plan_flag=1,plan_status="In Process",total_faculty_required=obj.total_faculty_required,faculty_in_database=obj.faculty_in_database,faculty_to_be_recruited=0,buffer_number=0,to_be_recruited_with_buffer=0
,planning_comments=obj.planning_comments,created_by=request.user,created_on=datetime.datetime.now(),updated_by = request.user,last_updated_on = datetime.datetime.now())
                    gfpn.save()
        if change and obj.plan_status == "In Process":
            faculty_to_recruit = obj.total_faculty_required - obj.faculty_in_database
            if faculty_to_recruit <0:
               faculty_to_recruit=0 	
            obj.faculty_to_be_recruited = faculty_to_recruit
            obj.buffer_number = int(math.ceil((obj.buffer_type.buffer_percentage * faculty_to_recruit)/100))
            obj.to_be_recruited_with_buffer = obj.buffer_number + faculty_to_recruit
            obj.program_coordinator_id = request.user.id
            obj.plan_status = "In Process"
            obj.version_number = 1
            obj.current_plan_flag = 1
            obj.plan_status = "In Process"
            obj.created_by = request.user
            obj.created_on = datetime.datetime.now()
            obj.updated_by = request.user
            obj.last_updated_on = datetime.datetime.now()
            obj.save()
        if change and obj.plan_status == "Submitted":
            faculty_to_recruit = obj.total_faculty_required - obj.faculty_in_database
            if faculty_to_recruit <0:
               faculty_to_recruit=0 	
            obj.faculty_to_be_recruited = faculty_to_recruit
            obj.buffer_number = int(math.ceil((obj.buffer_type.buffer_percentage * faculty_to_recruit)/100))
            obj.to_be_recruited_with_buffer = obj.buffer_number + faculty_to_recruit
            obj.program_coordinator_id = request.user.id
            obj.plan_status = "In Process"
            obj.version_number = 1
            obj.current_plan_flag = 1
            obj.plan_status = "In Process"
            obj.created_by = request.user
            obj.created_on = datetime.datetime.now()
            obj.updated_by = request.user
            obj.last_updated_on = datetime.datetime.now()
            obj.save()

        if not change:
            faculty_to_recruit = obj.total_faculty_required - obj.faculty_in_database
            if faculty_to_recruit <0:
               faculty_to_recruit=0 	
            obj.faculty_to_be_recruited = faculty_to_recruit
            obj.buffer_number = int(math.ceil((obj.buffer_type.buffer_percentage * faculty_to_recruit)/100))
            obj.to_be_recruited_with_buffer = obj.buffer_number + faculty_to_recruit
            obj.program_coordinator_id = request.user.id
            obj.plan_status = "In Process"
            obj.version_number = 1
            obj.current_plan_flag = 1
            obj.plan_status = "In Process"
            obj.created_by = request.user
            obj.created_on = datetime.datetime.now()
            obj.updated_by = request.user
            obj.last_updated_on = datetime.datetime.now()
            obj.save()


    def get_queryset(self, request):
        qs = super(GuestFacultyPlanningNumbersAdmin, self).get_queryset(request)
        if  request.user.is_superuser:
            return qs
        elif request.user.is_staff and request.user.groups.filter(name__in=['coordinator']):

            if Coordinator.objects.filter(coordinator=request.user,coordinator_for_location__isnull=False).exists():
                       
                cl = Coordinator.objects.get(coordinator=request.user)    
                return qs.filter(location=cl.coordinator_for_location).filter(Q(plan_status="In Process") | Q(plan_status="Submitted"))
            elif Program.objects.filter(program_coordinator_id=request.user.id).exists():
                pr =Program.objects.get(program_coordinator_id=request.user.id)
                return qs.filter(program=pr.program_id).filter(Q(plan_status="In Process") | Q(plan_status="Submitted"))
            else:
                #print "nopanl"
                return ""
            
        elif request.user.groups.filter(name__in=['offcampusadmin']):
            #print request.user.id
            return qs.filter(Q(plan_status="Submitted") | Q(plan_status="Approved") | Q(plan_status="Rejected"))
        else:
            return qs

   
    class SubmitPlanforReviewForm(forms.Form):
        submission_comments = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': '30','rows' : '5'}))
		
    def submit_plan_for_review(self, request, obj):
        form = None
        if 'update' in request.POST:
            form = self.SubmitPlanforReviewForm(request.POST)
            if form.is_valid():
                submission_comments = form.cleaned_data['submission_comments']
                obj.plan_status='Submitted'
                obj.planning_comments = submission_comments
                obj.last_updated_on = datetime.datetime.now()
                obj.save()
                message_bit = "Plan was"
                self.message_user(request, "%s successfully Submitted for Review ." % message_bit)
                return "<script>window.history.back();</script>"
                #return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.SubmitPlanforReviewForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
  
        data = {'plan': obj,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/submit_plan_for_review.html', data)
				
    submit_plan_for_review.short_description = "Submit for Review"
    submit_plan_for_review.label = "Submit for Review"

    class ApprovePlanForm(forms.Form):
        approve_comments = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': '30','rows' : '5'}))
		
    def approve_plan(self, request, obj):
        form = None
        if 'update' in request.POST:
            form = self.ApprovePlanForm(request.POST)
            if form.is_valid():
                approve_comments = form.cleaned_data['approve_comments']
                obj.plan_status='Approved'
                obj.approver_comments = approve_comments
                obj.approved_rejected_by = request.user
                obj.approved_rejected_on = datetime.datetime.now()
                obj.save()
                message_bit = "Plan was"
                self.message_user(request, "%s successfully Approved ." % message_bit)
                return "<script>window.history.back();</script>"
                #return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.ApprovePlanForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
  
        data = {'plan': obj,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/approve_plan.html', data)
				
    approve_plan.short_description = "Approve Plan"
    approve_plan.label = "Approve Plan"

    class RejectPlanForm(forms.Form):
        reject_comments = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': '30','rows' : '5'}))
    def reject_plan(self, request, obj):
        try:
            form = None
            if 'update' in request.POST:
                form = self.RejectPlanForm(request.POST)
                if form.is_valid():
                    reject_comments = form.cleaned_data['reject_comments']
                    obj.plan_status='Rejected'
                    obj.approver_comments = reject_comments
                    obj.approved_rejected_by = request.user
                    obj.approved_rejected_on = datetime.datetime.now()
                    obj.save()
                    message_bit = "Plan was"
                    self.message_user(request, "%s successfully Rejected ." % message_bit)
                    return "<script>window.history.back();</script>"
        except IntegrityError:
            message_bit = "Plan was"
            self.message_user(request, "%s successfully Rejected ." % message_bit)
            return "<script>window.history.back();</script>"
           
                #return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.RejectPlanForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
  
        data = {'plan': obj,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/reject_plan.html', data)
				
    reject_plan.short_description = "Reject Plan"
    reject_plan.label = "Reject Plan"

    objectactions = ('submit_plan_for_review','approve_plan','reject_plan')	
    def get_object_actions(self, request, context, **kwargs):
        objectactions = []
        obj = context['original']		
        #if request.user.groups.filter(name__in=['guestfaculty']).exists():
        if obj:
            if request.user.is_superuser:
                if obj.current_plan_flag == 1 and obj.plan_status == "In Process":
                    objectactions.extend(['submit_plan_for_review',])
                elif obj.current_plan_flag == 1 and obj.plan_status == "Submitted":
                    objectactions.extend(['approve_plan',])
                    objectactions.extend(['reject_plan',])		
            elif request.user.is_staff and request.user.groups.filter(name__in=['coordinator']).exists():
                if obj.current_plan_flag == 1 and obj.plan_status == "In Process":
                    objectactions.extend(['submit_plan_for_review',])				
            elif  request.user.groups.filter(name__in=['offcampusadmin']):
                if obj.plan_status == "Submitted":
                    objectactions.extend(['approve_plan',])
                    objectactions.extend(['reject_plan',])	
        return objectactions              
admin.site.register(GuestFacultyPlanningNumbers, GuestFacultyPlanningNumbersAdmin)

class PlanningWindowStatusAdminForm(forms.ModelForm):
    def clean(self):
        if not self.instance.pk:
            currenstsem=CurrentSemester.objects.filter(currentsemester=self.cleaned_data.get('semester')).count()
            if currenstsem==0:
                    raise forms.ValidationError("Please Select current semester")
            if self.data.get("end_date") < self.data.get("start_date"):
                raise forms.ValidationError("End date should be greater than Start date")

class  CurrentSemesterFilter1(SimpleListFilter):
    title = 'currentsemester'
    parameter_name = 'currentsemester'

    def lookups(self, request, model_admin):
        semesters = set([s for s in Semester.objects.all()])
        return [(s.semester_id,s.semester_name) for s in semesters]
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(semester_id=self.value())    
        elif self.value() == None:
            currentsem=CurrentSemester.objects.values_list("currentsemester",flat=True)
            return queryset.filter(semester_id=currentsem)
        else:
            return qs
class PlanningWindowStatusAdmin(admin.ModelAdmin):
    form=PlanningWindowStatusAdminForm   
    model = PlanningWindowStatus
    list_display = ('semester','program','status','start_date','end_date','last_updated_date','updated_by')
    fields = ('semester','program','status','start_date','end_date','last_updated_date','updated_by')
    readonly_fields = ('updated_by','last_updated_date')
    list_editable = ('status','start_date','end_date')
    list_display_links =None
    list_filter = (CurrentSemesterFilter1,)
    def save_model(self, request, obj, form, change):
        if not change:
            obj.updated_by = request.user
            obj.last_updated_date = datetime.datetime.now()
            obj.save()
        if change:
            obj.updated_by = request.user
            obj.last_updated_date = datetime.datetime.now()
            obj.save()


admin.site.register(PlanningWindowStatus, PlanningWindowStatusAdmin)

class ApplicationUsersAdminForm(forms.ModelForm):
    def clean(self):
        cd = self.cleaned_data.get('user')
        matchObject = re.match('^[a-zA-Z0-9_@.]*$', cd)
        if matchObject:
            print "The string '"+cd+"' is alphanumeric"
        else:
            #print "The string '"+cd+"' is not alphanumeric"
            raise forms.ValidationError("Please Check The User")

class ApplicationUsersAdmin(admin.ModelAdmin):
    form = ApplicationUsersAdminForm
    model = ApplicationUsers
    readonly_fields = ('application_name',)
    list_display = ('application_name','user','role_name','created_on','created_by','last_updated_on','last_updated_by')
    fields = ('application_name','user','role_name',)

    def save_model(self, request, obj, form, change): 
        if not change:
            obj.created_on = datetime.datetime.today()
            obj.last_updated_on=datetime.datetime.today()
            obj.last_updated_by=request.user.id
            obj.created_by = request.user.id
            apuser=User.objects.filter(username=obj.user).count()
            if apuser==0:
                user = User.objects.create_user(obj.user)
                user.is_staff = True
		user.groups.add(Group.objects.get(name='coordinator'))
                user.save()
            else:
                #ApplicationUsers.objects.update(obj.user)
                s = ApplicationUsers.objects.latest('id')
                sd=s.id
                ApplicationUsers.objects.filter(id=sd).update(user=obj.user)
                #ApplicationUsers.objects.all().update(id=sd+1)
            obj.save()
            
        elif change:
            obj.created_on = datetime.datetime.today()
            obj.last_updated_on=datetime.datetime.today()
            obj.last_updated_by=request.user.id
            obj.created_by = request.user.id	
            obj.save()

                
admin.site.register(ApplicationUsers, ApplicationUsersAdmin)

class CurrentSemesterAdmin(admin.ModelAdmin):
    model = CurrentSemester
    list_display = ('currentsemester','created_on_date')
   
    def save_model(self, request, obj, form, change):
        CurrentSemester.objects.all().delete()
        obj.save()
           

admin.site.register(CurrentSemester, CurrentSemesterAdmin)
