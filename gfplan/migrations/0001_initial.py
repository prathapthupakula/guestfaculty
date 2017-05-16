# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationUsers',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('application_name', models.CharField(default='GF PLANNING APP', max_length=50)),
                ('user', models.CharField(max_length=200)),
                ('role_name', models.CharField(max_length=20, choices=[('Location Cordinator', 'Location Cordinator'), ('Program Cordinator', 'Program Cordinator')])),
                ('role_parameters', models.CharField(max_length=200)),
                ('created_on', models.DateTimeField()),
                ('created_by', models.CharField(max_length=50)),
                ('last_updated_on', models.DateTimeField()),
                ('last_updated_by', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Application Users',
                'db_table': 'application_users',
                'managed': False,
                'verbose_name_plural': 'Application Users',
            },
        ),
        migrations.CreateModel(
            name='BufferType',
            fields=[
                ('buffer_calc_id', models.AutoField(verbose_name='ID', serialize=False, editable=False, primary_key=True)),
                ('buffer_percentage', models.DecimalField(verbose_name='Percentage', max_digits=10, decimal_places=2)),
                ('buffer_name', models.CharField(max_length=20, verbose_name='Name')),
            ],
            options={
                'db_table': 'buffer_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CurrentSemester',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('created_on_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name': 'Current Semester',
                'db_table': 'current_semester',
                'managed': False,
                'verbose_name_plural': 'Current Semester',
            },
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('d_id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=225)),
                ('company_name', models.CharField(max_length=225)),
                ('role', models.CharField(max_length=225)),
            ],
            options={
                'verbose_name': 'Designation example',
                'db_table': 'gfdesignation',
                'managed': False,
                'verbose_name_plural': 'gfplan designation example',
            },
        ),
        migrations.CreateModel(
            name='DesignationResource',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=225)),
            ],
            options={
                'verbose_name': 'resource ',
                'db_table': 'design_resource',
                'managed': False,
                'verbose_name_plural': 'Resource example',
            },
        ),
        migrations.CreateModel(
            name='GfPlanExample',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=225)),
                ('mobilenum', models.CharField(max_length=225)),
                ('email', models.CharField(max_length=225)),
                ('location', models.CharField(max_length=225)),
            ],
            options={
                'verbose_name': 'example list',
                'db_table': 'gfplanexample',
                'managed': False,
                'verbose_name_plural': 'Exapmple list details',
            },
        ),
        migrations.CreateModel(
            name='GuestFacultyPlanningNumbers',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('version_number', models.IntegerField(verbose_name='Version')),
                ('current_plan_flag', models.BooleanField(verbose_name='Current')),
                ('plan_status', models.CharField(max_length=15, verbose_name='Status')),
                ('total_faculty_required', models.IntegerField(verbose_name='Faculty Reqd')),
                ('faculty_in_database', models.IntegerField(verbose_name='Faculty in DB')),
                ('faculty_to_be_recruited', models.IntegerField(null=True, verbose_name='To Recruit', blank=True)),
                ('buffer_number', models.IntegerField(null=True, verbose_name='Buffer', blank=True)),
                ('to_be_recruited_with_buffer', models.IntegerField(null=True, verbose_name='Recruit with Buffer', blank=True)),
                ('planning_comments', models.CharField(max_length=2000, null=True, blank=True)),
                ('created_on', models.DateTimeField()),
                ('last_updated_on', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('approver_comments', models.CharField(max_length=2000, null=True, blank=True)),
                ('approved_rejected_on', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'guest_faculty_planning_numbers',
                'verbose_name': 'Forecast Plan',
                'verbose_name_plural': 'Forecast Plans',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlanningWindowStatus',
            fields=[
                ('planning_id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('status', models.CharField(max_length=15, choices=[('Open', 'Open'), ('Closed', 'Closed')])),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('last_updated_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Last Updated', editable=False)),
            ],
            options={
                'db_table': 'planning_window_status',
                'verbose_name': 'Plan Window',
                'verbose_name_plural': 'Plan Window',
                'managed': False,
            },
        ),
    ]
