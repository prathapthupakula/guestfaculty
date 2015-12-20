from __future__ import unicode_literals

from django.db import models
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import Group 
from facultyapp.models import GuestFacultyCandidate, GuestFaculty, GuestFacultyCourseOffer, GuestFacultyQualification, FacultyClassAttendance


class GFCandidateListReport(GuestFacultyCandidate):
    class Meta:
        verbose_name, verbose_name_plural = u"Guest Faculty Candidate List", u"Guest Faculty Candidate List"
        proxy = True

class GFCandidateCountReport(GuestFacultyCandidate):
    class Meta:
        verbose_name, verbose_name_plural = u"Guest Faculty Candidate Count", u"Guest Faculty Candidate Count"
        proxy = True
		
class GuestFacultyListReport(GuestFaculty):
    class Meta:
        verbose_name, verbose_name_plural = u"Guest Faculty Analysis", u"Guest Faculty Analysis"
        proxy = True

		
class GuestFacultyActivityReport(GuestFacultyCourseOffer):
    class Meta:
        verbose_name, verbose_name_plural = u"Guest Faculty Activity", u"Guest Faculty Activity"
        proxy = True

class GuestFacultyQualificationReport(GuestFacultyQualification):
    class Meta:
        verbose_name, verbose_name_plural = u"Guest Faculty Qualification", u"Guest Faculty Qualification"
        proxy = True

class GuestFacultyAttendanceReport(FacultyClassAttendance):
    class Meta:
        verbose_name, verbose_name_plural = u"Guest Faculty Attendance", u"Guest Faculty Attendance"
        proxy = True
		