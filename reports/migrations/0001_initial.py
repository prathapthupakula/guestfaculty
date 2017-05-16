# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facultyapp', '0002_auto_20160818_1134'),
        ('gfplan', '0001_initial'),
        ('timetable', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GFCandidateCountReport',
            fields=[
            ],
            options={
                'verbose_name': 'Guest Faculty Candidate Count',
                'proxy': True,
                'verbose_name_plural': 'Guest Faculty Candidate Count',
            },
            bases=('facultyapp.guestfacultycandidate',),
        ),
        migrations.CreateModel(
            name='GFCandidateListReport',
            fields=[
            ],
            options={
                'verbose_name': 'Guest Faculty Candidate List',
                'proxy': True,
                'verbose_name_plural': 'Guest Faculty Candidate List',
            },
            bases=('facultyapp.guestfacultycandidate',),
        ),
        migrations.CreateModel(
            name='GuestFacultyActivityReport',
            fields=[
            ],
            options={
                'verbose_name': 'Guest Faculty Teaching Activity',
                'proxy': True,
                'verbose_name_plural': 'Guest Faculty Teaching Activity',
            },
            bases=('facultyapp.guestfacultycourseoffer',),
        ),
        migrations.CreateModel(
            name='GuestFacultyAttendanceReport',
            fields=[
            ],
            options={
                'verbose_name': 'Guest Faculty Attendance',
                'proxy': True,
                'verbose_name_plural': 'Guest Faculty Attendance',
            },
            bases=('facultyapp.facultyclassattendance',),
        ),
        migrations.CreateModel(
            name='GuestFacultyListReport',
            fields=[
            ],
            options={
                'verbose_name': 'Guest Faculty Listing with Affiliation',
                'proxy': True,
                'verbose_name_plural': 'Guest Faculty Listing with Affiliation',
            },
            bases=('facultyapp.guestfaculty',),
        ),
        migrations.CreateModel(
            name='GuestFacultyQualificationReport',
            fields=[
            ],
            options={
                'verbose_name': 'Guest Faculty Listing With Qualification',
                'proxy': True,
                'verbose_name_plural': 'Guest Faculty Listing With Qualification',
            },
            bases=('facultyapp.guestfacultyqualification',),
        ),
        migrations.CreateModel(
            name='PlanningWindowStatusReport',
            fields=[
            ],
            options={
                'verbose_name': 'GF Forecast Planning Windows',
                'proxy': True,
                'verbose_name_plural': 'GF Forecast Planning Windows',
            },
            bases=('gfplan.planningwindowstatus',),
        ),
        migrations.CreateModel(
            name='SemesterMilestonePlanMasterReport',
            fields=[
            ],
            options={
                'verbose_name': 'Timetable and Milestones Date report',
                'proxy': True,
                'verbose_name_plural': 'Timetable and Milestones Date report',
            },
            bases=('timetable.semestermilestoneplanmaster',),
        ),
        migrations.CreateModel(
            name='SemesterPlanDetailReport',
            fields=[
            ],
            options={
                'verbose_name': 'Milestone Plan Report',
                'proxy': True,
                'verbose_name_plural': ' New Milestone Plan Report',
            },
            bases=('timetable.semesterplandetail',),
        ),
        migrations.CreateModel(
            name='SemesterTimetableEditWindowReport',
            fields=[
            ],
            options={
                'verbose_name': 'Semester Timetable Edit Windows',
                'proxy': True,
                'verbose_name_plural': 'Semester Timetable Edit Windows',
            },
            bases=('timetable.semestertimetableeditwindow',),
        ),
    ]
