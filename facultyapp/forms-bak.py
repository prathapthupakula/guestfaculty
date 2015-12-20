from django import forms
from django.forms import ModelForm
from facultyapp.models import Location
from facultyapp.models import GuestFacultyCandidate


class NameForm(forms.Form):
	your_name = forms.EmailField(label='Your name', max_length=100)

class LocationForm(ModelForm):
	class Meta:
		model = Location
		fields = '__all__'
class GuestFacultyForm(ModelForm):
	class Meta:
		model = GuestFacultyCandidate
		fields = '__all__'		