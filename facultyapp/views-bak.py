from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .forms import NameForm
from .forms import LocationForm
from .forms import GuestFacultyForm

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

	
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'facultyapp/name.html', {'form': form})
	
def get_location(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LocationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			form.save()
            #return HttpResponseRedirect('faculty/location.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LocationForm()

    return render(request, 'facultyapp/location.html', {'form': form})	
  
def get_candidate(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GuestFacultyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
			form.save()
            #return HttpResponseRedirect('faculty/location.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GuestFacultyForm()

    return render(request, 'facultyapp/candidate.html', {'form': form})	  