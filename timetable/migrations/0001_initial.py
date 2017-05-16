# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('batch_id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('batch_name', models.CharField(max_length=45)),
                ('admission_year', models.CharField(max_length=4)),
                ('expected_grad_year', models.CharField(max_length=4)),
                ('duration', models.IntegerField()),
                ('total_admission_strength', models.IntegerField()),
            ],
            options={
                'ordering': ('batch_name',),
                'verbose_name': 'Batch',
                'db_table': 'batch',
                'managed': False,
                'verbose_name_plural': 'Batches',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('employee_name', models.CharField(max_length=100)),
                ('employee_id', models.CharField(unique=True, max_length=10)),
                ('gender', models.CharField(max_length=10, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('address', models.TextField(max_length=500, blank=True)),
            ],
            options={
                'db_table': 'employee',
                'managed': False,
                'verbose_name_plural': 'Employee',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('organization_id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('organization_name', models.CharField(max_length=100)),
                ('organization_long_name', models.CharField(max_length=200)),
                ('association_duration_in_months', models.IntegerField()),
                ('start_year', models.IntegerField()),
            ],
            options={
                'ordering': ('organization_name',),
                'db_table': 'organization',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SemesterMilestone',
            fields=[
                ('milestone_id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('milestone_short_name', models.CharField(max_length=45)),
                ('milestone_long_name', models.CharField(max_length=200, null=True, blank=True)),
                ('milestone_type', models.CharField(max_length=45, verbose_name=b'Milestone Type')),
                ('is_duration_milestone', models.BooleanField(default=0)),
                ('is_editable_by_owner', models.NullBooleanField(default=0)),
                ('active', models.BooleanField()),
                ('max_duration_in_days', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ('milestone_short_name',),
                'db_table': 'semester_milestone',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SemesterMilestonePlanMaster',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('program_code1', models.CharField(max_length=200, null=True, verbose_name=b'program code', blank=True)),
                ('version_number', models.IntegerField(default=1)),
                ('semester_plan_name', models.CharField(max_length=200, verbose_name=b'plan name')),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('last_updated_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'last updated on', editable=False)),
                ('last_update_by', models.CharField(max_length=100)),
                ('timetable_status', models.CharField(blank=True, max_length=45, null=True, verbose_name=b'current state', choices=[(b'Created', b'Created'), (b'Approved', b'Approved'), (b'In Process', b'In Process'), (b'Rejected', b'Rejected'), (b'Submitted', b'Submitted'), (b'Escalated', b'Escalated'), (b'Escalated/In Process', b'Escalated/In Process')])),
                ('current_version_flag', models.BooleanField(default=1)),
                ('timetable_comments', models.CharField(max_length=200, null=True, blank=True)),
                ('mode_of_delivery', models.CharField(max_length=100, choices=[(b'Diss', b'Diss'), (b'DTVC', b'DTVC'), (b'Class Room', b'Class Room'), (b'Class Room With Tandberg', b'Class Room With Tandberg'), (b'DTVC/Interaction', b'DTVC/Interaction'), (b'Dissertation', b'Dissertation'), (b'Polycom/Class Room', b'Polycom/Class Room'), (b'Technology bassed', b'Technology based'), (b'Class Room (Diss)', b'Class Room (Diss)'), (b'Class Room/flipped', b'Class Room/flipped')])),
                ('registration_completed_in_wilp', models.BooleanField()),
                ('student_strength', models.IntegerField()),
                ('approved_rejected_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Rejected Date', editable=False)),
                ('approved_rejected_by', models.CharField(max_length=100, verbose_name=b'Rejected By')),
                ('approval_rejection_comments', models.CharField(max_length=200)),
                ('escalated_on_date', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('escalated_by', models.CharField(max_length=200)),
                ('escalation_comments', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Semester Milestone Calendar',
                'db_table': 'semester_milestone_plan_master',
                'managed': False,
                'verbose_name_plural': 'Semester Milestone Calendar',
            },
        ),
        migrations.CreateModel(
            name='SemesterMilestonePlanMaster1',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('version_number', models.IntegerField(default=1)),
                ('semester_plan_name', models.CharField(max_length=200, verbose_name=b'plan name')),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('last_updated_date', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('last_update_by', models.CharField(max_length=100)),
                ('timetable_status', models.CharField(blank=True, max_length=45, null=True, verbose_name=b'current state', choices=[(b'Created', b'Created'), (b'Approved', b'Approved'), (b'In Process', b'In Process'), (b'Rejected', b'Rejected'), (b'Submitted', b'Submitted'), (b'Escalated', b'Escalated'), (b'Escalated/In Process', b'Escalated/In Process')])),
                ('current_version_flag', models.BooleanField(default=1)),
                ('timetable_comments', models.CharField(max_length=200, null=True, blank=True)),
                ('mode_of_delivery', models.CharField(max_length=100, choices=[(b'Diss', b'Diss'), (b'DTVC', b'DTVC'), (b'Class Room', b'Class Room'), (b'Class Room With Tandberg', b'Class Room With Tandberg'), (b'DTVC/Interaction', b'DTVC/Interaction'), (b'Dissertation', b'Dissertation'), (b'Polycom/Class Room', b'Polycom/Class Room'), (b'Technology bassed', b'Technology based'), (b'Class Room (Diss)', b'Class Room (Diss)'), (b'Class Room/flipped', b'Class Room/flipped')])),
                ('registration_completed_in_wilp', models.BooleanField()),
                ('student_strength', models.IntegerField()),
                ('approved_rejected_date', models.DateTimeField(verbose_name=b'Rejected Date')),
                ('approved_rejected_by', models.CharField(max_length=100, verbose_name=b'Rejected By')),
                ('approval_rejection_comments', models.CharField(max_length=200)),
                ('escalated_on_date', models.DateTimeField()),
                ('escalated_by', models.CharField(max_length=200)),
                ('escalation_comments', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Semester Milestone Plan Master report',
                'db_table': 'semester_milestone_plan_master',
                'managed': False,
                'verbose_name_plural': 'Timetable and Milestones Date report',
            },
        ),
        migrations.CreateModel(
            name='SemesterPlanDetail',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('version_number', models.IntegerField(default=1)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('event_date', models.DateField(null=True, blank=True)),
                ('date_editable', models.BooleanField(default=1)),
                ('is_milestone', models.BooleanField(default=0, verbose_name=b'Is Duration Milestone')),
                ('system_populated_date', models.BooleanField(default=1)),
                ('created_by', models.CharField(max_length=45)),
                ('created_date', models.DateField()),
                ('milestone_comments', models.CharField(max_length=45, null=True, blank=True)),
                ('last_updated_by', models.CharField(max_length=45)),
                ('last_updated_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Last Updated', editable=False)),
            ],
            options={
                'db_table': 'semester_milestone_plan_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SemesterPlanDetail1',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('version_number', models.IntegerField(default=1)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('event_date', models.DateField(null=True, blank=True)),
                ('date_editable', models.BooleanField(default=1)),
                ('is_milestone', models.BooleanField(default=0, verbose_name=b'Is Duration Milestone')),
                ('system_populated_date', models.BooleanField(default=1)),
                ('created_by', models.CharField(max_length=45)),
                ('created_date', models.DateField()),
                ('milestone_comments', models.CharField(max_length=45, null=True, blank=True)),
                ('last_updated_by', models.CharField(max_length=45)),
                ('last_updated_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Last Updated', editable=False)),
            ],
            options={
                'verbose_name': 'Timetable and Milestones Date report',
                'db_table': 'semester_milestone_plan_detail',
                'managed': False,
                'verbose_name_plural': 'Timetable and Milestones Date report',
            },
        ),
        migrations.CreateModel(
            name='SemesterTimetableEditWindow',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('status', models.CharField(max_length=15, choices=[(b'Open', b'Open'), (b'Closed', b'Closed')])),
                ('last_updated_on', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Last Updated', editable=False)),
                ('last_updated_by', models.CharField(max_length=45)),
                ('dealine_creation_date', models.DateField(verbose_name=b'deadline creation date')),
                ('daeadline_submission_date', models.DateField(verbose_name=b'deadline submission date')),
                ('deadline_approval_date', models.DateField()),
                ('exam_date', models.DateTimeField(null=True, blank=True)),
                ('days_before_exam', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'semester_timetable_edit_window',
                'managed': False,
            },
        ),
    ]
