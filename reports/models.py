from __future__ import unicode_literals

from django.db import models
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import Group 
from facultyapp.models import GuestFacultyCandidate, GuestFaculty, GuestFacultyCourseOffer, GuestFacultyQualification, FacultyClassAttendance,GuestFacultyInterview
from gfplan.models import PlanningWindowStatus
from timetable.models import SemesterTimetableEditWindow
from timetable.models import SemesterPlanDetail,SemesterMilestonePlanMaster


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
        verbose_name, verbose_name_plural = u"Guest Faculty Listing with Affiliation", u"Guest Faculty Listing with Affiliation"
        proxy = True

		
class GuestFacultyActivityReport(GuestFacultyCourseOffer):
    class Meta:
        verbose_name, verbose_name_plural = u"Guest Faculty Teaching Activity", u"Guest Faculty Teaching Activity"
        proxy = True

class GuestFacultyQualificationReport(GuestFacultyQualification):
    class Meta:
        verbose_name, verbose_name_plural = u"Guest Faculty Listing With Qualification", u"Guest Faculty Listing With Qualification"
        proxy = True

class GuestFacultyAttendanceReport(FacultyClassAttendance):
    class Meta:
        verbose_name, verbose_name_plural = u"Guest Faculty Attendance", u"Guest Faculty Attendance"
        proxy = True
class PlanningWindowStatusReport(PlanningWindowStatus):
    class Meta:
        verbose_name, verbose_name_plural = u"GF Forecast Planning Windows", u"GF Forecast Planning Windows"
        proxy = True
class SemesterPlanDetailReport(SemesterPlanDetail):
    class Meta:
        verbose_name, verbose_name_plural = u"Milestone Plan Report", u" New Milestone Plan Report"
        proxy = True
class SemesterMilestonePlanMasterReport(SemesterMilestonePlanMaster):
    class Meta:
        verbose_name, verbose_name_plural = u"Timetable and Milestones Date report", u"Timetable and Milestones Date report"
        proxy = True
class SemesterTimetableEditWindowReport(SemesterTimetableEditWindow):
    class Meta:
        verbose_name, verbose_name_plural = u"Semester Timetable Edit Windows", u"Semester Timetable Edit Windows"
        proxy = True
class GuestFacultyDegreeDisciplineReport(GuestFaculty):
    class Meta:
        verbose_name, verbose_name_plural = u"Guest Faculty by Degree and Discipline", u"Guest Faculty by Degree and Discipline"
        proxy = True
class GuestFacultyInterviewReport(GuestFacultyInterview):
    class Meta:
        verbose_name, verbose_name_plural = u"Guest Faculty Candidate Interview Schedule", u"Guest Faculty Candidate Interview Schedule"
        proxy = True

