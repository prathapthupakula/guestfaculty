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
from .models import SemesterTimetableEditWindow
from .models import SemesterMilestonePlanMaster
#from django_object_actions import DjangoObjectActions
from django_object_actions import (DjangoObjectActions, takes_instance_or_queryset)
#from django_object_actions import BaseDjangoObjectActions
from django_object_actions import (BaseDjangoObjectActions, takes_instance_or_queryset)
from import_export import resources
from facultyapp.models import Semester,CourseLocationSemesterDetail,Coordinator,Location,Program,Course,Discipline
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



STATUS_LIST = (
    ('Created', 'Created'),
    ('Approved', 'Approved'),
    ('In Process', 'In Process'),	
    ('Rejected', 'Rejected'),
    ('Submitted','Submitted'),
    ('Escalated','Escalated'),
    ('Escalated/In Process','Escalated/In Process')
)


class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_id','batch_name','admission_year','expected_grad_year','total_admission_strength')
    list_display_links = ('batch_name',)
admin.site.register(Batch, BatchAdmin)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_id','organization_name','organization_long_name','start_year')
    list_display_links = ('organization_name',)
	
admin.site.register(Organization, OrganizationAdmin)
class SemesterMilestoneAdmin(admin.ModelAdmin):
    list_display = ('milestone_id','milestone_short_name','milestone_long_name','milestone_type')
    list_display_links = ('milestone_long_name',)
    pass
    
	
admin.site.register(SemesterMilestone,SemesterMilestoneAdmin)

class SemesterTimetableEditWindowAdminForm(forms.ModelForm):
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
 

class SemesterTimetableEditWindowAdmin(admin.ModelAdmin):
    form = SemesterTimetableEditWindowAdminForm
    model = SemesterTimetableEditWindow
    list_display = ('id','semester_id','status','program_id','location_id','timetable_owner_id','daeadline_submission_date','deadline_approval_date')
    readonly_fields = ('last_updated_on','last_updated_by',)
    list_editable = ('status','daeadline_submission_date','daeadline_submission_date','deadline_approval_date')
    list_display_links =None
    list_editable = ('status',)
    list_display_links =('id',)	
    #list_editable = (status)
    def save_model(self, request, obj, form, change): 
        #obj.last_updated_by = request.user
        obj.last_updated_on = datetime.datetime.now()
        obj.save()
admin.site.register(SemesterTimetableEditWindow, SemesterTimetableEditWindowAdmin)

class GFResource(resources.ModelResource):

    class Meta:
        model = SemesterMilestonePlanMaster

def send_gfemail(emailid, mailtemplate,mailtitle,c):
    msg_plain = render_to_string('%s' %mailtemplate, c)
    send_mail(mailtitle, msg_plain, settings.EMAIL_HOST_USER, emailid, fail_silently=True)	
    return True

class SemesterPlanDetailInlineForm(ModelForm):

    class Meta:
        model = SemesterPlanDetail
        fields = ('semester_milestone_plan_master','version_number','semester_milestone','start_date','end_date','event_date',)
        readonly_fields = ('version_number',)
        #fields = '__all__'
	
class SemesterPlanDetailInline(admin.TabularInline):
    model = SemesterPlanDetail
    form = SemesterPlanDetailInlineForm
    readonly_fields = ('version_number',)
    extra = 0
    verbose_name_plural = 'Semester PlanDetails'

    def get_max_num(self, request, obj=None, **kwargs):
        max_num = 0
        if not obj:
            
            return 0
        else:
            max_num = 5
            return max_num	

class SemesterMilestonePlanMasterAdminForm(forms.ModelForm):

    def clean(self):
        # If Insert then check the following validation	
        if not self.instance.pk:
            # Check if Open Window Plan and allow entry
            if SemesterTimetableEditWindow.objects.filter(timetable_owner=self.current_user.id).exists():
                open_check = SemesterTimetableEditWindow.objects.filter(status='Open',timetable_owner=self.current_user.id,semester=self.cleaned_data.get('semester'),program=self.cleaned_data.get('program'),location=self.cleaned_data.get('location'),dealine_creation_date__lte=datetime.datetime.today(), deadline_approval_date__gte=datetime.datetime.today()).count()
                if open_check < 1:
                    raise forms.ValidationError("The timetable entry for the status, location, program, semester,timetable owner is incorrect and please check dead line creation date and dead line approvel date .")
            else:
                raise forms.ValidationError("The timetable entry for the status, location, program, and semester is incorrect. Please enter correct data in SemesterMilestonePlanMaster")

            # Check if program/location/course/discipline/semester combination is valid and allow entry
            """clsd_check = CourseLocationSemesterDetail.objects.filter(semester=self.cleaned_data["semester"],program=self.cleaned_data["program"],location=self.cleaned_data["location"],discipline=self.cleaned_data["discipline"]).count()
            if clsd_check < 1:
                raise forms.ValidationError("The plan entry for the course, location, program, semester and discipline is incorrect. Please enter plan numbers for correct combinations only")"""

def timetable_action(obj):
    if SemesterTimetableEditWindow.objects.filter(daeadline_submission_date__lt=datetime.datetime.today(),location=obj.location,program=obj.program,semester=obj.semester,timetable_owner=obj.milestone_plan_owner).exists():
        if obj.timetable_status != "Submitted" and obj.timetable_status != "Approved" and obj.timetable_status != "Rejected":
            return "Delayed. Timetable should be Submitted for approval by now"
    if SemesterTimetableEditWindow.objects.filter(deadline_approval_date__lt=datetime.datetime.today(),location=obj.location,program=obj.program,semester=obj.semester,timetable_owner=obj.milestone_plan_owner).exists():
        if obj.timetable_status != "Approved" and obj.timetable_status != "Rejected":    
            return "Delayed. Timetable should be Approved by now"
    elif obj.timetable_status == "": 
        return "Not Created"

timetable_action.short_description = 'Statues'    

class SemesterMilestonePlanMasterAdmin(DjangoObjectActions,admin.ModelAdmin):
    form = SemesterMilestonePlanMasterAdminForm

    #get the current user
    def get_form(self, request,obj=None, **kwargs):
         form = super(SemesterMilestonePlanMasterAdmin, self).get_form(request,obj, **kwargs)
         form.current_user = request.user
         return form


    inlines = (SemesterPlanDetailInline,)
    model=SemesterMilestonePlanMaster
    fields = (('version_number','semester_plan_name','current_version_flag','timetable_status','timetable_comments',('location','degree'),('program','semester'),('batch','client_organization'),('discipline','milestone_plan_owner'),('alternate_owner','mode_of_delivery'),('registration_completed_in_wilp','student_strength')))   
    list_display = ('version_number','timetable_status','semester_plan_name','location_id','milestone_plan_owner_id','created_date','student_strength','current_version_flag',timetable_action)
    readonly_fields = ('version_number','timetable_status','milestone_plan_owner',)
    list_display_links = ('semester_plan_name',)
    """def changelist_view(self, request, extra_context=None):
        if request.user.groups.filter(name__in=['offcampusadmin']).exists() or request.user.is_superuser:
            self.list_display = ('version_number','timetable_status','semester_plan_name','location_id','milestone_plan_owner_id','created_date','student_strength','current_version_flag',timetable_action)
            self.list_display_links = ('semester_plan_name',)
        else:
            self.list_display = ('version_number','timetable_status','semester_plan_name','location_id','milestone_plan_owner_id','created_date','student_strength','current_version_flag')
            self.list_display_links = ('semester_plan_name',)
        return super(SemesterMilestonePlanMasterAdmin, self).changelist_view(request, extra_context=extra_context)"""


    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            # Check if Open record with Date range validity exists in Plan Window and allow Edit of the Record
            open_check = SemesterTimetableEditWindow.objects.filter(status='Open',semester=obj.semester,program=obj.program,location=obj.location).count()
            if open_check > 0 and obj.current_version_flag == 1:
                return self.readonly_fields + ('semester','program','location','timetable_owner','status','degree','client_organization','batch','discipline','mode_of_delivery')
            else:				
                return ['version_number','timetable_status','semester_plan_name','semester','degree','program','discipline','batch', 'client_organization','alternate_owner','milestone_plan_owner','created_date','student_strength''version_number','timetable_status','semester_plan_name','location','milestone_plan_owner','created_date','student_strength']                		# This is for All fields			
        return self.readonly_fields
    def get_queryset(self, request):
        qs = super(SemesterMilestonePlanMasterAdmin, self).get_queryset(request)
        if request.user.is_superuser :
            return qs
        elif  request.user.is_staff and request.user.groups.filter(name__in=['coordinator']):
            if Coordinator.objects.filter(coordinator=request.user,coordinator_for_location__isnull=False).exists():
                cl = Coordinator.objects.get(coordinator=request.user)
                return qs.filter(location=cl.coordinator_for_location).filter(Q(timetable_status="In Process") | Q(timetable_status="Submitted") | Q(timetable_status="Escalated/In Process") | Q(timetable_status="Created") | Q(timetable_status="Escalated"))
            else:
                pr =Program.objects.get(program_coordinator_id=request.user.id)
                return qs.filter(program=pr.program_id).filter(Q(timetable_status="In Process") | Q(timetable_status="Submitted") | Q(timetable_status="Escalated/In Process") | Q(timetable_status="Created") | Q(timetable_status="Escalated"))
        elif request.user.groups.filter(name__in=['offcampusadmin']):
            return qs.filter(Q(timetable_status="In Process") | Q(timetable_status="Submitted") | Q(timetable_status="Escalated/In Process") | Q(timetable_status="Created") | Q(timetable_status="Escalated") | Q(timetable_status="Approved") | Q(timetable_status="Rejected"))    
        else :
            return qs.filter(milestone_plan_owner_id=request.user)  

    def save_model(self, request, obj, form, change):
        # Allow edits/saves only on current record
        if change and obj.current_version_flag == 1:
            if obj.timetable_status == "Approved":
                obj.current_version_flag = 0;
                obj.save(update_fields=['current_version_flag'])
                gsmpm= SemesterMilestonePlanMaster(version_number=obj.version_number+1,semester_plan_name=obj.semester_plan_name,created_date=datetime.datetime.now(),last_updated_date=datetime.datetime.now(),last_update_by=request.user.id,timetable_status="In Process",current_version_flag=1,timetable_comments=obj.timetable_comments,location=obj.location,degree=obj.degree,program=obj.program,semester=obj.semester,batch=obj.batch,client_organization=obj.client_organization,discipline=obj.discipline,milestone_plan_owner=obj.milestone_plan_owner,alternate_owner=obj.alternate_owner,mode_of_delivery=obj.mode_of_delivery,registration_completed_in_wilp=obj.registration_completed_in_wilp,student_strength=obj.student_strength,approved_rejected_date=datetime.datetime.now(),approved_rejected_by=request.user.id,approval_rejection_comments=obj.approval_rejection_comments,escalated_on_date=datetime.datetime.now(),escalated_by=request.user.id,escalation_comments=obj.escalation_comments)
                gsmpm.save()
                mil_typ=SemesterMilestone.objects.filter(milestone_type='DEFAULT',active='1')
                for cq in mil_typ:
                    m=SemesterPlanDetail(semester_milestone_plan_master=gsmpm,version_number=obj.version_number+1,semester_milestone=cq,start_date=datetime.datetime.today(),end_date=datetime.datetime.today(),event_date=datetime.datetime.today(),date_editable='1',system_populated_date='0',created_by=request.user,created_date=datetime.datetime.today(),milestone_comments=obj.timetable_comments,last_updated_by=request.user,last_updated_date=datetime.datetime.today())
	            m.save()


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

        if not change:
            obj.timetable_status="Created"
            obj.milestone_plan_owner_id=request.user.id
            obj.created_date = datetime.datetime.now()
            obj.last_update_by = request.user
            obj.last_updated_date = datetime.datetime.now()
            obj.current_version_flag=1
            obj.approved_rejected_date=datetime.datetime.now()
            obj.escalated_on_date=datetime.datetime.now()
            obj.approved_rejected_by=request.user
            obj.save()
            mil_typ=SemesterMilestone.objects.filter(milestone_type='DEFAULT',active='1')
            for cq in mil_typ:
                mp=SemesterPlanDetail(semester_milestone_plan_master=obj,version_number='1',semester_milestone=cq,start_date=datetime.datetime.today(),end_date=datetime.datetime.today(),event_date=datetime.datetime.today(),date_editable='1',system_populated_date='0',created_by=request.user,created_date=datetime.datetime.today(),milestone_comments=obj.timetable_comments,last_updated_by=request.user,last_updated_date=datetime.datetime.today())
	        mp.save()
            template = 'createdemail.txt'
            c=Context({'username': request.user.username, 'application_url':settings.APPLICATION_URL,'degree':obj.degree,'location':obj.location,'batch':obj.batch,'program':obj.program,'semester':obj.semester,'organization':obj.client_organization,'discipline':obj.discipline})                    
            send_gfemail([request.user.email],template,'Re: BITS Guest Faculty Application',c) 					
                
            plural = ''
            count=1
            if count == 1:
                plural = 's'
            self.message_user(request, "Submitted %d timetable%s." % (count, plural))
            return "<script>window.history.back();</script>"


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
                print obj.timetable_status
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
                 #return HttpResponseRedirect(request.get_full_path())
                return "<script>window.history.back();</script>"

        if not form:
            form = self.EscalatedPlanforReviewForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        data = {'plan':obj,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/escalated_plan_for_review.html', data)
				
    escalated_plan_for_review.short_description = "Escalate/In Process"
    escalated_plan_for_review.label = "Escalate/In Process"

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
                 #return HttpResponseRedirect(request.get_full_path())
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
                 #return HttpResponseRedirect(request.get_full_path())
                return "<script>window.history.back();</script>"

        if not form:
            form = self.EscalatedForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        data = {'plan':obj,'form': form,} 
        data.update(csrf(request)) 
        return render_to_response('admin/escalated_plan_for_review.html', data)
				
    escalated_plan_for_review.short_description = "ESCALATE"
    escalated_plan_for_review.label = "ESCALATE"

    objectactions = ('submit_plan_for_review','approve_plan','reject_plan','escalated_plan_for_review','escalated')
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

class SemesterPlanDetailAdminForm(forms.ModelForm):

    def clean(self):
        # If Insert then check the following validation	
        if not self.instance.pk:
            # Check if Open Window Plan and allow entry
            if SemesterMilestone.objects.filter(milestone_short_name=obj.semester_milestone,is_duration_milestone__gt=0).exists():
                start_date= self.cleaned_data['start_date']
                end_date=self.cleaned_data['end_date']
                date =end_date-start_date
                duration=SemesterMilestone.objects.values_list("is_duration_milestone",flat=True)
                if end_date<start_date and  date<duration:
                    raise forms.ValidationError("Please Check Start Date and End Date")
            #if start_date-end_date < MAX_DURATION_IN_DAYS

def data(obj):
    if SemesterMilestone.objects.filter(milestone_short_name=obj.semester_milestone,is_duration_milestone=0):
        
        #return "Accept/Reject"
        return obj.event_date
    else: 
        return ""
data.short_description = 'Event Date'    

        #return ""
def data1(obj):
    if SemesterMilestone.objects.filter(milestone_short_name=obj.semester_milestone,is_duration_milestone=1):
        
        #return "Accept/Reject"
        return obj.start_date
    else: 
        return ""
data1.short_description = 'Start Date'    
def data2(obj):
    if SemesterMilestone.objects.filter(milestone_short_name=obj.semester_milestone,is_duration_milestone=1):
        
        #return "Accept/Reject"
        return obj.end_date
    else: 
        return ""
data2.short_description = 'End Date'    


class SemesterPlanDetailAdmin(admin.ModelAdmin):
    form = SemesterPlanDetailAdminForm
    fields = ('semester_milestone_plan_master','version_number','semester_milestone','start_date','end_date','event_date','date_editable','system_populated_date','milestone_comments')   
    list_display = ('semester_milestone_plan_master','version_number','semester_milestone',data,data1,data2)
    list_display_links = ('semester_milestone_plan_master',)
    readonly_fields = ('version_number',)
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            # Check if Open record with Date range validity exists in Plan Window and allow Edit of the Record
            open_check = SemesterMilestone.objects.filter(milestone_short_name=obj.semester_milestone,is_duration_milestone=1).count()
            print open_check
            if open_check > 0:
                
                return self.readonly_fields + ('event_date',)
                #return self.list_display + ('start_date','end_date', 'event_date',)
            else:
                				
                return ['start_date','end_date',]   # This is for All fields			
        return self.readonly_fields

    """def changelist_view(self, request, extra_context=None):
        sem=SemesterMilestone.objects.filter(is_duration_milestone=0).count()
        print sem
        if sem>1:
            self.list_display = ('semester_milestone','semester_milestone_plan_master','version_number','start_date','end_date')
            self.list_display_links = ('semester_milestone_plan_master')
        else:
            self.list_display = ('semester_milestone','semester_milestone_plan_master','version_number', 'event_date')
            self.list_display_links = ('semester_milestone_plan_master',)
        return super(SemesterPlanDetailAdmin, self).changelist_view(request, extra_context=extra_context)"""	
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
