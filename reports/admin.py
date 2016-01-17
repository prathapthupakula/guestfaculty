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
from django.core.mail import send_mail
from django.template import Context
from django.db.models import Q, F
from django.contrib.admin.helpers import ActionForm
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.conf import settings
from django.template.loader import render_to_string
from django.db import Error

from import_export import resources
#from import_export.admin import ExportActionModelAdmin
#from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportMixin, ImportMixin, ImportExportMixin
from import_export import fields,widgets
from import_export.widgets import ForeignKeyWidget, BooleanWidget

#from django_object_actions import DjangoObjectActions
from django_object_actions import (DjangoObjectActions, takes_instance_or_queryset)
#from django_object_actions import BaseDjangoObjectActions
from django_object_actions import (BaseDjangoObjectActions, takes_instance_or_queryset)

from django.contrib.admin import RelatedFieldListFilter

from django.contrib.admin import AdminSite

from django.db.models import Sum, Avg, Count, Min, Max


from .models import GFCandidateListReport, GFCandidateCountReport, GuestFacultyActivityReport, GuestFacultyListReport, GuestFacultyQualificationReport, GuestFacultyAttendanceReport
from admin_report.mixins import ChartReportAdmin

class AdminNoAddPermissionMixin(object):
    def has_add_permission(self, request):
        return False

class ReportGFCandidateAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    list_display = ('application_number','name','application_status','application_submission_date','current_location_id')	
    list_filter = ('application_status','application_submission_date','applying_for_discipline',('current_location',admin.RelatedOnlyFieldListFilter))	

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Candidate List'}
        return super(ReportGFCandidateAdmin, self).changelist_view(request, extra_context=extra_context)
		
admin.site.register(GFCandidateListReport, ReportGFCandidateAdmin)


class ReportGFCandidateCountAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    list_display = ('applying_for_discipline','show_application_count')	
    list_filter = ('applying_for_discipline',)
    #report_annotates = (('application_id', Count, "mycount"),('application_id', Sum, "mysum"))
    #report_aggregates = (('application_id', Count, "mycount"),('application_id', Sum, "mysum"))
    group_by = ('applying_for_discipline_id',)
    def get_queryset(self, request):
        qs = super(ReportGFCandidateCountAdmin, self).get_queryset(request)
        return qs.values('applying_for_discipline_id').annotate(application_count=Count('name')).order_by('application_count')
        #return []
        #return GFCandidateCountReport.objects.values('applying_for_discipline_id').annotate(application_count=Count('application_id')).order_by()
    def show_application_count(self, obj):
        return obj.application_count
    show_application_count.short_description = 'Application Count'
    #show_application_count.admin_order_field = 'application_count'

#admin.site.register(GFCandidateCountReport, ReportGFCandidateCountAdmin)

class ReportGuestFacultyListAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    list_display = ('guest_faculty_id','name','pan_number','recruitment_location','recruited_on_date', 'current_organization')	
    list_filter = ('recruited_on_date','current_organization',('recruitment_location',admin.RelatedOnlyFieldListFilter))

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Listing With Current Affiliation'}
        return super(ReportGuestFacultyListAdmin, self).changelist_view(request, extra_context=extra_context)
		
admin.site.register(GuestFacultyListReport, ReportGuestFacultyListAdmin)


class ReportGuestFacultyQualificationAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    list_display = ('guest_faculty','qualification','degree','qualification_discipline','year_of_completion','completed','highest_qualification','normalized_marks_cpi_cgpa')	
    list_filter = ('qualification','degree','qualification_discipline')

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Listing With Qualification'}
        return super(ReportGuestFacultyQualificationAdmin, self).changelist_view(request, extra_context=extra_context)
		
admin.site.register(GuestFacultyQualificationReport, ReportGuestFacultyQualificationAdmin)

class ReportGuestFacultyActivityAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    list_display = ('guest_faculty','course','semester','program','location')	
    list_filter = ('course','semester','program',('location',admin.RelatedOnlyFieldListFilter))	
	
    def get_queryset(self, request):
        qs = super(ReportGuestFacultyActivityAdmin, self).get_queryset(request) 
        return qs.filter(course_offer_status="Accepted")

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Listing With Teaching Activity'}
        return super(ReportGuestFacultyActivityAdmin, self).changelist_view(request, extra_context=extra_context)	
		
admin.site.register(GuestFacultyActivityReport, ReportGuestFacultyActivityAdmin)

class ReportGuestFacultyAttendanceAdmin(ExportMixin,AdminNoAddPermissionMixin,ChartReportAdmin):
    #change_list_template = 'admin/reports/change_list.html'
    list_display = ('guest_faculty','course','semester','program','class_date','class_time_slot','absent')	
    list_filter = ('class_date','course','semester','program')

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'Guest Faculty Attendance'}
        return super(ReportGuestFacultyAttendanceAdmin, self).changelist_view(request, extra_context=extra_context)	

	
admin.site.register(GuestFacultyAttendanceReport, ReportGuestFacultyAttendanceAdmin)

