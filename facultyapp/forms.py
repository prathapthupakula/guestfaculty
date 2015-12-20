from django import forms
from django.forms import Textarea
from django.forms.models import inlineformset_factory

from .models import Location, GuestFacultyCandidate, Program, CandidateQualification

def upper_case_name(obj):
    return ("%s %s" % (obj.location_state, obj.location_country)).upper()
upper_case_name.short_description = 'STATE CITY'


QualificationFormSet = inlineformset_factory(GuestFacultyCandidate,CandidateQualification, fields='__all__', can_delete=True, extra=1, min_num=1, validate_min=True)
	

class GuestFacultyForm(forms.ModelForm):
    class Meta:
        model = GuestFacultyCandidate
        fields = '__all__'
        widgets = {
            'address1': Textarea(attrs={'cols': 20, 'rows': 5}),
        }

