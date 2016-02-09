from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse

from .models import GuestFacultyCandidate, CandidateQualification
from .forms import GuestFacultyForm, QualificationFormSet

def index(request):
    #return render(request, 'facultyapp/home.html')
    return render_to_response('facultyapp/home.html', context_instance=RequestContext(request))


	

  
def get_candidate(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GuestFacultyForm(request.POST)
        qualification_formset = QualificationFormSet(instance=GuestFacultyCandidate())
        # check whether it's valid:
        if form.is_valid():

            candidate = form.save(commit=False)
            qualification_formset = QualificationFormSet(request.POST, instance=candidate, auto_id=False)
            if qualification_formset.is_valid():
                candidate.save()
                qualification_formset.save()
                return HttpResponseRedirect(reverse('get_candidate'))		

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GuestFacultyForm()
        qualification_formset = QualificationFormSet(instance=GuestFacultyCandidate())
    return render_to_response("facultyapp/candidate.html", {
        "form": form,
        "qualification_formset": qualification_formset,
    }, context_instance=RequestContext(request))
