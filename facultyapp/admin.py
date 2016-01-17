from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.admin import UserAdmin, GroupAdmin
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
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.template.loader import render_to_string
from django.db import Error
from django.db import IntegrityError,transaction
from import_export import resources
#from import_export.admin import ExportActionModelAdmin
#from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportMixin, ImportMixin, ImportExportMixin
from import_export import fields,widgets
from import_export.widgets import ForeignKeyWidget, BooleanWidget

from django.core.exceptions import ValidationError

#from django_object_actions import DjangoObjectActions
from django_object_actions import (DjangoObjectActions, takes_instance_or_queryset)
#from django_object_actions import BaseDjangoObjectActions
from django_object_actions import (BaseDjangoObjectActions, takes_instance_or_queryset)

from django.contrib.admin import RelatedFieldListFilter

from django.contrib.contenttypes.models import ContentType

from django.contrib.admin import AdminSite

from admin_report.mixins import ChartReportAdmin

from .models import Location, GuestFacultyCandidate, Program, CandidateQualification, CandidateEvaluation, GuestFaculty, GuestFacultyQualification, GfInterestedInDiscipline, Course, Discipline, Semester, CourseLocationSemesterDetail, Coordinator, GuestFacultyCourseOffer, GuestFacultyHonararium, FacultyClassAttendance, FeedbackSurvey, GuestFacultyFeedbackResults, GuestFacultyScore


STATUS_LIST = (
    ('Submitted', 'Submitted'),
    ('Shortlisted', 'Shortlisted'),
    ('In Process', 'In Process'),	
    ('Selected', 'Selected'),
    ('Rejected', 'Rejected'),
)


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
    #delete = fields.Field(widget=widgets.BooleanWidget())
	
    class Meta:
        model = GuestFacultyCourseOffer
        fields = ('course','location','semester','program','guest_faculty','honorarium_given','honorarium_text','hon_issued_on_date','hon_issued_by','honorarium_payment_mode','course_offer_status')
        import_id_fields = ('course', 'semester', 'program', 'guest_faculty', 'location','course_offer_status')

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
    #delete = fields.Field(widget=widgets.BooleanWidget())
	
    class Meta:
        model = GuestFacultyCourseOffer
        fields = ('course','location','semester','program','guest_faculty','course_offer_status','assessment_score','feedback',)
        import_id_fields = ('course', 'semester', 'program', 'guest_faculty', 'location','course_offer_status')

    #def for_delete(self, row, instance):
    #    return self.fields['delete'].clean(row)
		
class CLSResource(resources.ModelResource):

    course = fields.Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    location = fields.Field(column_name='location', attribute='location', widget=ForeignKeyWidget(Location, 'location_name'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    discipline = fields.Field(column_name='discipline', attribute='discipline', widget=ForeignKeyWidget(Discipline, 'discipline_long_name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'program_name'))
    delete = fields.Field(widget=widgets.BooleanWidget())
	
    class Meta:
        model = CourseLocationSemesterDetail
        fields = ('course','location','semester','discipline','program','max_faculty_count','number_of_students_in_class','number_of_sections')
        import_id_fields = ('course','location','semester')

    def for_delete(self, row, instance):
        return self.fields['delete'].clean(row)
		

class GFCOResource(resources.ModelResource):

    course = fields.Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    location = fields.Field(column_name='location', attribute='location', widget=ForeignKeyWidget(Location, 'location_name'))
    semester = fields.Field(column_name='semester', attribute='semester', widget=ForeignKeyWidget(Semester, 'semester_name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'program_name'))
    guest_faculty = fields.Field(column_name='guest_faculty', attribute='guest_faculty', widget=ForeignKeyWidget(GuestFaculty, 'guest_faculty_id'))
    program_coordinator = fields.Field(column_name='program_coordinator', attribute='program_coordinator', widget=ForeignKeyWidget(Coordinator, 'coordinator_name'))
    delete = fields.Field(widget=widgets.BooleanWidget())
	
    class Meta:
        model = GuestFacultyCourseOffer
        fields = ('course','location','semester','program','guest_faculty','course_offer_status','sequence_number','program_coordinator','offer_to_faculty_date','number_students_in_class','section','honorarium_given','honorarium_text','hon_issued_on_date','hon_issued_by','assessment_score','feedback')
        import_id_fields = ('course', 'semester', 'guest_faculty')

    def for_delete(self, row, instance):
        return self.fields['delete'].clean(row)

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
    list_filter = ['location_country','location_state']
    list_display = ('location_name','location_state','location_country')	# Field Value Modification while displaying
    list_display_links = ('location_name',)
    #list_display = ('location_id','location_name',upper_case_name)	# Field Value Modification while displaying
    #list_editable = ('location_name',)	  #Editable Grid
#    readonly_fields = ('location_id',)    # Making Read-Only. THis can also be set in the Model file
    #search_fields = ('^location_name','location_id')	#enable search bar (= for %, @ for fulltext. recommended is ^)
# search_fields = ['foreign_key__related_fieldname']	This is for foreign_key search
#    save_on_top = True
#    fields = ('location_name', 'location_state', 'location_country')


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


# Create Inline Form for Candidate Qualifications to display as Stack
class CandidateQualificationInlineForm(ModelForm):

    class Meta:
        model = CandidateQualification
        fields = ('degree_degree','college','discipline','qualification','year_of_completion','percent_marks_cpi_cgpa','max_marks_cpi_cgpa','normalized_marks_cpi_cgpa','highest_qualification','completed')
        #list_filter=['highest_qualification']
		
class CandidateQualificationInline(admin.TabularInline):
    model = CandidateQualification
    readonly_fields = ('normalized_marks_cpi_cgpa',)
    list_filter=('highest_qualification',)
    form = CandidateQualificationInlineForm
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

# Main Form	
class GuestFacultyCandidateAdmin(BaseDjangoObjectActions,ExportMixin,admin.ModelAdmin):

    site_header = 'Guest Faculty Application'
    site_title =  'Guest Faculty Application'
    site_url = None
    index_title = 'Guest Faculty Application'
    resource_class = GFResource
    
    model = GuestFacultyCandidate
    fieldsets = (
        ('Personal Details', {
            'fields': ('application_number',('name','pan_number'),('date_of_birth','gender'),('phone','mobile'),('address1','current_location'),('applying_for_discipline', 'reapplication','application_status'))
        }),
		   ('Current Experience', {
            'fields': (('current_organization','current_org_designation'),('months_in_curr_org','teach_experience_in_months'),('industry_exp_in_months','total_experience_in_months'),('nature_of_current_job','areas_of_expertise'),('certifications','awards_and_distinctions'),'publications','uploaded_cv_file_name')
        }),
    )
    list_display = ('application_number','name','application_status','application_submission_date','current_location_id')
    radio_fields = {"gender": admin.HORIZONTAL}
    readonly_fields = ('application_id','application_number','reapplication','application_status')
    widgets = {
            'address1': Textarea(attrs={'cols': 20, 'rows': 5}),
    }
    inlines = (CandidateQualificationInline,)
	
    list_filter = ('application_status','application_submission_date','applying_for_discipline',('current_location',admin.RelatedOnlyFieldListFilter))
    actions = ['update_candidate_status','interview_candidate_call','update_candidate_selection','convert_to_guestfaculty']
    objectactions = ['update_candidate_selection','update_candidate_status']
	
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
    def changelist_view(self, request, extra_context=None):
        if not request.user.is_staff:
            self.list_filter = tuple()
        extra_context = {'title': 'Guest Faculty Candidate List'}
        return super(GuestFacultyCandidateAdmin, self).changelist_view(request, extra_context=extra_context)

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
            return qs.filter(by_user_id=request.user)  
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
        return objectactions		

    class UpdateCandidateStatusForm(forms.Form):
        status = forms.ChoiceField(choices=(('Shortlisted', 'Shortlisted'), ('Rejected', 'Rejected'),))
        comments = forms.CharField(required=True, widget=forms.Textarea(attrs={'cols': '30','rows' : '5'}))
        
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
        location = forms.ChoiceField(choices=[ (o.location_id, o.location_name) for o in Location.objects.all()])		
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
        score = forms.DecimalField(max_digits=10, decimal_places=1,initial=10,help_text='(maximum score value = 10.0)',min_value=0.0, max_value=10.0 )
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
    update_candidate_selection.label = "Select/Reject Candidate"
    update_candidate_selection.short_description = "Select/Reject Candidate"

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
                    
                    gf = GuestFaculty(pan_number=candidate.pan_number,name=candidate.name,gender=candidate.gender,date_of_birth=candidate.date_of_birth,email=candidate.email,total_experience_in_months=candidate.total_experience_in_months,phone=candidate.phone,mobile=candidate.mobile,address1=candidate.address1,teach_experience_in_months=candidate.teach_experience_in_months,current_organization=candidate.current_organization,months_in_curr_org=candidate.months_in_curr_org,recruited_on_date=datetime.datetime.today(),current_location=candidate.current_location,uploaded_cv_file_name=candidate.uploaded_cv_file_name,recruitment_location=ev.evaluation_location,industry_exp_in_months=candidate.industry_exp_in_months,nature_of_current_job=candidate.nature_of_current_job,certifications=candidate.certifications,awards_and_distinctions=candidate.awards_and_distinctions,publications=candidate.publications,areas_of_expertise=candidate.areas_of_expertise,confidentiality_requested=0,updated_by=candidate.by_user.id)
					
                    gf.save()
                    gf.guest_faculty_id = 'GF' + str(gf.id)
                    gf.save()
					
                    cqs = CandidateQualification.objects.filter(application=candidate)					
                    for cq in cqs:
					
                        gq = GuestFacultyQualification(guest_faculty=gf,qualification=cq.qualification,degree=cq.degree_degree,qualification_discipline=cq.discipline,guest_faculty_pan_number=gf.pan_number,college=cq.college,year_of_completion=cq.year_of_completion,completed=cq.completed,highest_qualification=cq.highest_qualification,percent_marks_cpi_cgpa=cq.percent_marks_cpi_cgpa,max_marks_cpi_cgpa=cq.max_marks_cpi_cgpa,inserted_date=datetime.datetime.today(),normalized_marks_cpi_cgpa=cq.normalized_marks_cpi_cgpa)
                        gq.save()
					
                    candidate.application_status = "Recruited"
                    candidate.save()

                    # modify the role so they can access only their GF details and not the application.
                    candidate.by_user.groups.remove(Group.objects.get(name='candidate'))
                    candidate.by_user.groups.add(Group.objects.get(name='guestfaculty'))   	
					
                    template = 'selectedemail.txt'
                    c = Context({'username': candidate.name, 'application_url':settings.APPLICATION_URL})                    
                    send_gfemail([candidate.email],template,'Re: BITS Guest Faculty Application',c) 					
                
                plural = ''
                if count != 1:
                    plural = 's'
                self.message_user(request, "Successfully Converted %d candidate%s." % (count, plural))
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




class GuestFacultyQualificationInlineForm(ModelForm):

    class Meta:
        model = GuestFacultyQualification
        fields = ('degree','college','qualification_discipline','qualification','year_of_completion','percent_marks_cpi_cgpa','max_marks_cpi_cgpa','normalized_marks_cpi_cgpa','highest_qualification','completed')
        #fields = '__all__'
	
class GuestFacultyQualificationInline(admin.TabularInline):
    model = GuestFacultyQualification
    form = GuestFacultyQualificationInlineForm
    extra = 1
    max_num = 5	
    verbose_name_plural = 'Qualifications'

    #def get_readonly_fields(self, request, obj=None):
    #    if obj: # editing an existing object
    #        #return self.readonly_fields + ('name',) # This is used for each field selectively
    #        return self.get_fields(request,obj=None) # This is for All fields			
    #    return self.readonly_fields	

    #def get_extra(self, request, obj=None, **kwargs):
    #    extra = 1
    #    if obj:
    #       max_num = 0
    #       return 0
    #    return extra
		
    #def get_max_num(self, request, obj=None, **kwargs):
    #    max_num = 5
    #    if obj:
    #        return 0
    #   return max_num		

class GfInterestedInDisciplineInlineForm(ModelForm):

    class Meta:
        model = GfInterestedInDiscipline
        fields = ('discipline', 'areas_of_expertise','courses_can_handle')
        #fields = '__all__'
	
class GfInterestedInDisciplineInline(admin.TabularInline):
    model = GfInterestedInDiscipline
    form = GfInterestedInDisciplineInlineForm
    extra = 1
    max_num = 5	
    verbose_name_plural = 'Disciplines Interested'
	
class GuestFacultyAdmin(DjangoObjectActions,admin.ModelAdmin):
    model = GuestFaculty
    fieldsets = (
        ('Personal Details', {
            'fields': (('guest_faculty_id','recruited_on_date'),('name','pan_number'),('date_of_birth','gender'),('phone','mobile'),('address1','current_location'))
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
    list_display = ('guest_faculty_id','name','recruited_on_date','pan_number','current_location')
    radio_fields = {"gender": admin.HORIZONTAL}
    readonly_fields = ('guest_faculty_id','recruited_on_date','name','pan_number','date_of_birth','gender')
    list_filter = (('current_location',admin.RelatedOnlyFieldListFilter),)
    actions = ['assign_course']
	
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
                           attrs={'rows': 2,
                                  'cols': 20})},
    }	
    inlines = (GuestFacultyQualificationInline,GfInterestedInDisciplineInline)
	
    #list_filter = ('application_status','application_submission_date',('current_location',admin.RelatedOnlyFieldListFilter))
    def get_queryset(self, request):
        qs = super(GuestFacultyAdmin, self).get_queryset(request)
        if  request.user.is_superuser:
            return qs
        elif request.user.is_staff and request.user.groups.filter(name__in=['coordinator']):
            cl = Coordinator.objects.get(coordinator=request.user)
            return qs.filter(current_location=cl.coordinator_for_location)
        # get application's "owner"
        else :
            return qs.filter(updated_by=request.user.id)
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

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'WILP Guest Faculty List'}
        return super(GuestFacultyAdmin, self).changelist_view(request, extra_context=extra_context)	
		
		
admin.site.register(GuestFaculty, GuestFacultyAdmin)

class Coure(resources.ModelResource):
    #course = fields.Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    class Meta:
        model = Course
	fields = ('course_id','course_name','course_description','number_of_lectures','dissertation_project_work',)	


class CourseAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = Coure
    list_display = ('course_id','course_name','number_of_lectures','dissertation_project_work')
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Course Master'}
        return super(CourseAdmin, self).changelist_view(request, extra_context=extra_context)	
	
admin.site.register(Course, CourseAdmin)

class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('discipline_long_name','discipline_short_name')
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Academic Discipline Master'}
        return super(DisciplineAdmin, self).changelist_view(request, extra_context=extra_context)	
	
admin.site.register(Discipline, DisciplineAdmin)

class SemesterAdmin(admin.ModelAdmin):
    list_display = ('semester_name','semester_number','year','start_date','end_date')
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Semester Master'}
        return super(SemesterAdmin, self).changelist_view(request, extra_context=extra_context)
	
admin.site.register(Semester, SemesterAdmin)

class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ('coordinator','coordinator_name','coordinator_for_location')
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Location Coordinator List'}
        return super(CoordinatorAdmin, self).changelist_view(request, extra_context=extra_context)	
admin.site.register(Coordinator, CoordinatorAdmin)

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('program_name','specific_program','client_organization','program_coordinator')
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Program Master'}
        return super(ProgramAdmin, self).changelist_view(request, extra_context=extra_context)	
	
admin.site.register(Program, ProgramAdmin)

def accept_reject(obj):
    if obj.course_offer_status == "Offered":
        return "Accept/Reject"
    else: 
        return ""
accept_reject.short_description = ''

class GuestFacultyCourseOfferAdmin(ImportExportMixin,DjangoObjectActions,admin.ModelAdmin):
    model = GuestFacultyCourseOffer
    resource_class = GFCOResource
    fields = ('course','semester','program','guest_faculty','location','program_coordinator','number_students_in_class','course_offer_status','assessment_score')
    readonly_fields = ('course','semester','program','guest_faculty','location','course_offer_status','program_coordinator','number_students_in_class','assessment_score',)
    list_filter = ('course','semester','program','course_offer_status',('location',admin.RelatedOnlyFieldListFilter), )
    ordering = ['-update_datetime']
     	
	
    def has_add_permission(self, request, obj=None):
        return False	

    def has_delete_permission(self, request, obj=None):
        return False	
		
    def changelist_view(self, request, extra_context=None):
        if request.user.groups.filter(name__in=['guestfaculty']).exists():
            self.list_display = ('course','semester','program','guest_faculty','location','number_students_in_class','course_offer_status','assessment_score',accept_reject)
            self.list_display_links = ('None', accept_reject)
        else:
            self.list_display = ('course','semester','program','guest_faculty','location','number_students_in_class','course_offer_status','assessment_score')
            self.list_display_links = ('None',)
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
            # Increment Accepted Count in Course Location Semester Details
            ls = CourseLocationSemesterDetail.objects.filter(course=obj.course,location=obj.location,semester=obj.semester,program=obj.program)
            ls.update(accepted_count=F('accepted_count') + 1)
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

class CourseLocationSemesterDetailAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ('course','location','semester','discipline','program', 'max_faculty_count','assigned_count','accepted_count')
    list_filter = (('location',admin.RelatedOnlyFieldListFilter),('semester',admin.RelatedOnlyFieldListFilter),('discipline',admin.RelatedOnlyFieldListFilter),('program',admin.RelatedOnlyFieldListFilter),)
    readonly_fields = ('assigned_count', 'accepted_count')	
    actions = ['assign_course']
	
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
        else :
	    # get application's "owner" 
            return qs.filter(guest_faculty__updated_by=request.user.id)

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Add/Edit Course Location Semester Details. Assign Course to Faculty'}
        return super(CourseLocationSemesterDetailAdmin, self).changelist_view(request, extra_context=extra_context)	
    class AssignCourseForm(forms.Form):
        guestfaculty = forms.ModelChoiceField(label='Guest Faculty',queryset=GuestFaculty.objects.all())
			
    @takes_instance_or_queryset		
    def assign_course(self,request,queryset):
        form = None
        if 'update' in request.POST:
            form = self.AssignCourseForm(request.POST)
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
                            c = Context({'username': guestfaculty.name, 'application_url':settings.APPLICATION_URL})                    
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
                return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.AssignCourseForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
				
   
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
    model = GuestFacultyHonararium
    resource_class = HonarariumResource
    list_display = ('course','semester','program','guest_faculty','location','course_offer_status','honorarium_given')
    fields = ('course','semester','program','guest_faculty','location','course_offer_status','honorarium_given','honorarium_text','hon_issued_on_date','hon_issued_by','honorarium_payment_mode')
    readonly_fields = ('course','semester','program','guest_faculty','location','course_offer_status','program_coordinator','number_students_in_class')
    list_filter = ('course','semester','program',('location',admin.RelatedOnlyFieldListFilter),)

    #def has_add_permission(self, request, obj=None):
    #    return False	

    def get_queryset(self, request):
        qs = super(GuestFacultyHonarariumAdmin, self).get_queryset(request)
        return qs.filter(course_offer_status='Accepted')
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Honorarium List'}
        return super(GuestFacultyHonarariumAdmin, self).changelist_view(request, extra_context=extra_context)	
	

admin.site.register(GuestFacultyHonararium,GuestFacultyHonarariumAdmin)

class GuestFacultyScoreAdmin(ImportExportMixin,admin.ModelAdmin):
    model = GuestFacultyScore
    resource_class = ScoreResource
    list_display = ('course','semester','program','guest_faculty','location','course_offer_status','assessment_score','number_students_in_class',)
    fields = ('course','semester','program','guest_faculty','location','course_offer_status','number_students_in_class','assessment_score','feedback')
    readonly_fields = ('course','semester','program','guest_faculty','location','course_offer_status','program_coordinator','number_students_in_class')
    list_filter = ('course','semester','program',('location',admin.RelatedOnlyFieldListFilter),)
    #def has_add_permission(self, request, obj=None):
    #    return False	
    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Feedback'}
        return super(GuestFacultyScoreAdmin, self).changelist_view(request, extra_context=extra_context)	

    def get_queryset(self, request):
        qs = super(GuestFacultyScoreAdmin, self).get_queryset(request)
        return qs.filter(course_offer_status='Accepted')	

admin.site.register(GuestFacultyScore,GuestFacultyScoreAdmin)


class FacultyClassAttendanceAdmin(ImportExportMixin,admin.ModelAdmin):
    model = FacultyClassAttendance
    resource_class = FacultyClassAttendanceResource
    list_display = ('guest_faculty','course','semester','program','class_date','class_time_slot','absent')
    fields = ('course','semester','program','guest_faculty','class_date','class_time_slot','absent','comments_for_absence')
    #readonly_fields = ('course','semester','program','guest_faculty')
    list_filter = ('course','semester','program',('guest_faculty',admin.RelatedOnlyFieldListFilter),)

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
		
admin.site.register(FeedbackSurvey, FeedbackSurveyAdmin)

class GFFeedbackResultsAdmin(admin.ModelAdmin):
    list_display = ('guest_faculty_pan_number','semester','program','course','survey_id','survey_version_id','survey_question_id','student_choice','student_comments','answered_date')
    list_display_links = ('guest_faculty_pan_number',)
    fields = ('guest_faculty_pan_number','semester','program','course','survey_id','survey_version_id','survey_question_id','student_choice','student_comments','answered_date')
    readonly_fields = ('guest_faculty_pan_number','semester','program','course','survey_id','survey_version_id','survey_question_id','student_choice','student_comments','answered_date')

    def has_add_permission(self, request, obj=None):
        return False	

    def has_delete_permission(self, request, obj=None):
        return False
		
admin.site.register(GuestFacultyFeedbackResults, GFFeedbackResultsAdmin)


# Register User/Groups
admin.site.register(User,UserAdmin)
admin.site.register(Group,GroupAdmin)

admin.site.disable_action('delete_selected') #disable action in MRA Action list


# Create Separate Admin site for Non-Admin/Non-Staff Users
#class UserAdminAuthenticationForm(AuthenticationForm):
#    sdf=1

# Register Admin Site for Guest Faculty Candidates
#class GFAppSite(AdminSite):
#    site_header = 'Guest Faculty Online Application'
#    site_title =  'Guest Faculty Online Application'
#    site_url = None
#    index_title = 'Guest Faculty Online Application'
#    index_template = 'facultyapp/index.html'
#    app_index_template = 'facultyapp/index.html'
#    login_form = UserAdminAuthenticationForm

#    def has_permission(self, request):
#        return request.user.is_active and not request.user.is_staff
		
#gf_app_site = GFAppSite(name='gfapp')
#gf_app_site.register(GuestFacultyCandidate, GuestFacultyCandidateAdmin)
#gf_app_site.register(GuestFaculty, GuestFacultyAdmin)
#gf_app_site.register(GuestFacultyCourseOffer, GuestFacultyCourseOfferAdmin)
#gf_app_site.disable_action('delete_selected') #disable action in MRA Action list

# End of New Admin Site
