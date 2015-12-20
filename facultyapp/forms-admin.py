from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, ModelForm, Textarea, Select

from .models import Location, GuestFacultyCandidate, Program, CandidateQualification

def upper_case_name(obj):
    return ("%s %s" % (obj.location_state, obj.location_country)).upper()
upper_case_name.short_description = 'STATE CITY'

#class LocationForm(ModelForm):
#    class Meta:
#	    model = Location
#        widgets = {
#            'code': TextInput(attrs={'class': 'input-mini'}),
#            'population': TextInput(attrs={'class': 'input-medium'}),
#            'independence_day': SuitDateWidget,
#        }

class LocationAdmin(admin.ModelAdmin):
    list_filter = ['location_name']
    list_display = ('location_id','location_name',upper_case_name)	# Field Value Modification while displaying
    list_editable = ('location_name',)	  #Editable Grid
#    readonly_fields = ('location_id',)    # Making Read-Only. THis can also be set in the Model file
    search_fields = ('^location_name',)	#enable search bar (= for %, @ for fulltext. recommended is ^)
# search_fields = ['foreign_key__related_fieldname']	This is for foreign_key search
#    save_on_top = True
#    fields = ('location_name', 'location_state', 'location_country')



class CandidateQualificationInlineForm(ModelForm):
    class Meta:
        model = CandidateQualification
#        fields = '__all__'
        fields = ('degree_degree','college','discipline','qualification','year_of_completion','percent_marks_cpi_cgpa','max_marks_cpi_cgpa','highest_qualification','completed')
		
class CandidateQualificationInline(admin.TabularInline):
    model = CandidateQualification
    form = CandidateQualificationInlineForm
    extra = 1
    verbose_name_plural = 'Candidate Qualifications'	

class GuestFacultyAdmin(admin.ModelAdmin):
    radio_fields = {"gender": admin.HORIZONTAL}
    readonly_fields = ('application_status', 'application_submission_date')
    inlines = (CandidateQualificationInline,)

class GuestFacultyAdminForm(ModelForm):
    class Meta:
        model = GuestFacultyCandidate
        fields = '__all__'	
	

# Register your models here.
