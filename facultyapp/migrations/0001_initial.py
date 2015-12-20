# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BufferType',
            fields=[
                ('buffer_calc_id', models.IntegerField(serialize=False, primary_key=True)),
                ('buffer_percentage', models.DecimalField(max_digits=10, decimal_places=2)),
                ('buffer_name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'buffer_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CandidateEvaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('evaluation_id', models.IntegerField()),
                ('evaluation_seq_no', models.IntegerField()),
                ('evaluation_type', models.CharField(max_length=50)),
                ('evaluator_names_list', models.CharField(max_length=200)),
                ('evaluation_comments', models.CharField(max_length=1000, db_column='evaluation comments')),
                ('evaluation_date', models.DateTimeField(null=True, blank=True)),
                ('evaluation_venue', models.CharField(max_length=200, null=True, blank=True)),
                ('evaluation_time_slot', models.CharField(max_length=45, null=True, blank=True)),
                ('evaluation_result', models.CharField(max_length=45, null=True, blank=True)),
                ('letter_for_evaluation_rnd_sent', models.IntegerField(null=True, blank=True)),
                ('assessment_score', models.DecimalField(null=True, max_digits=10, decimal_places=5, blank=True)),
                ('regret_letter_sent', models.IntegerField()),
                ('selected_letter_sent', models.IntegerField()),
                ('insert_datetime', models.DateTimeField()),
                ('update_datetime', models.DateTimeField()),
            ],
            options={
                'db_table': 'candidate_evaluation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CandidateQualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('college', models.CharField(max_length=200)),
                ('year_of_completion', models.IntegerField(null=True, blank=True)),
                ('highest_qualification', models.IntegerField()),
                ('completed', models.IntegerField()),
                ('percent_marks_cpi_cgpa', models.DecimalField(max_digits=10, decimal_places=5)),
                ('max_marks_cpi_cgpa', models.DecimalField(max_digits=10, decimal_places=5)),
                ('normalized_marks_cpi_cgpa', models.DecimalField(max_digits=10, decimal_places=5)),
            ],
            options={
                'db_table': 'candidate_qualification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Coordinator',
            fields=[
                ('coordinator_id', models.IntegerField(serialize=False, primary_key=True)),
                ('coordinator_name', models.CharField(max_length=45)),
                ('coordinator_address', models.CharField(max_length=500)),
                ('phone', models.IntegerField(null=True, blank=True)),
                ('mobile', models.IntegerField(null=True, blank=True)),
                ('email', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'coordinator',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('course_name', models.CharField(max_length=100)),
                ('course_description', models.CharField(max_length=500, null=True, blank=True)),
                ('number_of_lectures', models.IntegerField()),
                ('dissertation_project_work', models.IntegerField()),
            ],
            options={
                'db_table': 'course',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CourseLocationSemesterDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_faculty_count', models.IntegerField()),
                ('number_of_students_in_class', models.IntegerField()),
                ('number_of_sections', models.IntegerField(db_column='number _of_sections')),
            ],
            options={
                'db_table': 'course_location_semester_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('degree_id', models.IntegerField(serialize=False, primary_key=True)),
                ('degree_full_name', models.CharField(max_length=200, null=True, blank=True)),
                ('degree_short_name', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'degree',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('discipline_id', models.IntegerField(serialize=False, primary_key=True)),
                ('discipline_long_name', models.CharField(max_length=200, null=True, blank=True)),
                ('discipline_short_name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'discipline',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FacultyClassAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('class_date', models.DateTimeField()),
                ('class_time_slot', models.CharField(max_length=45)),
                ('absent', models.IntegerField()),
                ('comments_for_absence', models.CharField(max_length=45, null=True, blank=True)),
                ('insert_datetime', models.DateTimeField()),
                ('update_datetime', models.DateTimeField()),
            ],
            options={
                'db_table': 'faculty_class_attendance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FeedbackSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('survey_id', models.IntegerField()),
                ('version_id', models.CharField(max_length=45)),
                ('question_id', models.CharField(max_length=45)),
                ('survey_name', models.CharField(max_length=45, null=True, blank=True)),
                ('question_description', models.CharField(max_length=45, null=True, blank=True)),
                ('question_type', models.CharField(max_length=45, null=True, blank=True)),
                ('mandatory', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'feedback_survey',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GfInterestedInDiscipline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('areas_of_expertise', models.CharField(max_length=1000, null=True, blank=True)),
                ('courses_can_handle', models.CharField(max_length=1000, null=True, blank=True)),
                ('insert_date_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'gf_interested_in_discipline',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuestFaculty',
            fields=[
                ('pan_number', models.CharField(max_length=10)),
                ('guest_faculty_id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=10)),
                ('date_of_birth', models.DateTimeField()),
                ('email', models.CharField(max_length=100)),
                ('total_experience_in_months', models.IntegerField(null=True, blank=True)),
                ('phone', models.DecimalField(null=True, max_digits=10, decimal_places=5, blank=True)),
                ('mobile', models.DecimalField(null=True, max_digits=10, decimal_places=5, blank=True)),
                ('address1', models.CharField(max_length=500)),
                ('teach_experience_in_months', models.IntegerField(null=True, blank=True)),
                ('current_organization', models.CharField(max_length=100)),
                ('current_org_designation', models.CharField(max_length=100, null=True, blank=True)),
                ('months_in_curr_org', models.IntegerField(null=True, blank=True)),
                ('recruited_on_date', models.DateTimeField()),
                ('last_updated_date', models.DateTimeField()),
                ('inserted_date', models.DateTimeField()),
                ('updated_by', models.CharField(max_length=100)),
                ('confidentiality_requested', models.IntegerField()),
                ('uploaded_cv_file_name', models.CharField(max_length=200)),
                ('payment_bank_name', models.CharField(max_length=200)),
                ('bank_account_number', models.CharField(max_length=45)),
                ('ifsc_code', models.CharField(max_length=15)),
                ('bank_address', models.CharField(max_length=500)),
                ('account_type', models.CharField(max_length=20)),
                ('beneficiary_name', models.CharField(max_length=10)),
                ('industry_exp_in_months', models.IntegerField(null=True, blank=True)),
                ('nature_of_current_job', models.CharField(max_length=500, null=True, blank=True)),
                ('certifications', models.CharField(max_length=2000, null=True, blank=True)),
                ('awards_and_distinctions', models.CharField(max_length=2000, null=True, blank=True)),
                ('publications', models.CharField(max_length=2000, null=True, blank=True)),
                ('membership_of_prof_bodies', models.CharField(max_length=2000, null=True, blank=True)),
                ('courses_taught', models.CharField(max_length=1000, null=True, blank=True)),
                ('areas_of_expertise', models.CharField(max_length=2000, null=True, blank=True)),
                ('taught_in_institutions', models.CharField(max_length=1000, null=True, blank=True)),
                ('industry_projects_done', models.CharField(max_length=1000, null=True, blank=True)),
                ('past_organizations', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
                'db_table': 'guest_faculty',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuestFacultyCandidate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('application_id', models.IntegerField()),
                ('pan_number', models.CharField(unique=True, max_length=10)),
                ('name', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=10)),
                ('date_of_birth', models.DateTimeField()),
                ('email', models.CharField(max_length=100)),
                ('total_experience_in_months', models.IntegerField()),
                ('phone', models.DecimalField(null=True, max_digits=10, decimal_places=5, blank=True)),
                ('mobile', models.DecimalField(null=True, max_digits=10, decimal_places=5, blank=True)),
                ('address1', models.CharField(max_length=500)),
                ('teach_experience_in_months', models.IntegerField(null=True, blank=True)),
                ('current_organization', models.CharField(max_length=100)),
                ('current_org_designation', models.CharField(max_length=100)),
                ('months_in_curr_org', models.IntegerField()),
                ('application_status', models.CharField(max_length=45)),
                ('reapplication', models.IntegerField()),
                ('received_status', models.IntegerField(null=True, blank=True)),
                ('application_ack_sent', models.IntegerField(null=True, blank=True)),
                ('application_submission_date', models.DateTimeField(null=True, blank=True)),
                ('uploaded_cv_file_name', models.CharField(max_length=200, null=True, blank=True)),
                ('industry_exp_in_months', models.IntegerField(null=True, blank=True)),
                ('nature_of_current_job', models.CharField(max_length=200, null=True, blank=True)),
                ('areas_of_expertise', models.CharField(max_length=2000, null=True, blank=True)),
                ('certifications', models.CharField(max_length=1000, null=True, blank=True)),
                ('awards_and_distinctions', models.CharField(max_length=1000, null=True, blank=True)),
                ('publications', models.CharField(max_length=2000, null=True, blank=True)),
            ],
            options={
                'db_table': 'guest_faculty_candidate',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuestFacultyCourseOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('program_id', models.IntegerField()),
                ('course_offer_status', models.CharField(max_length=10)),
                ('sequence_number', models.IntegerField()),
                ('program_coordinator_id', models.IntegerField()),
                ('offer_to_faculty_date', models.DateTimeField()),
                ('number_students_in_class', models.DecimalField(max_digits=10, decimal_places=5)),
                ('section', models.CharField(max_length=20, null=True, blank=True)),
                ('honorarium_given', models.IntegerField()),
                ('honorarium_text', models.CharField(max_length=1000, null=True, blank=True)),
                ('hon_issued_on_date', models.DateTimeField(null=True, blank=True)),
                ('hon_issued_by', models.CharField(max_length=200, null=True, blank=True)),
                ('honorarium_payment_mode', models.CharField(max_length=45, null=True, blank=True)),
                ('insert_datetime', models.DateTimeField()),
                ('update_datetime', models.DateTimeField()),
                ('max_faculty_count_reached', models.IntegerField()),
                ('assessment_score', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('feedback', models.CharField(max_length=1000, null=True, blank=True)),
            ],
            options={
                'db_table': 'guest_faculty_course_offer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuestFacultyFeedbackResults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('student_choice', models.CharField(max_length=45, null=True, blank=True)),
                ('student_comments', models.CharField(max_length=1000, null=True, blank=True)),
                ('answered_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'guest_faculty_feedback_results',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuestFacultyHasLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'guest_faculty_has_location',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuestFacultyHasQualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'guest_faculty_has_qualification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuestFacultyPlanningNumbers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version_number', models.IntegerField()),
                ('current_plan_flag', models.IntegerField()),
                ('plan_status', models.CharField(max_length=15)),
                ('total_faculty_required', models.IntegerField()),
                ('faculty_in_database', models.IntegerField()),
                ('faculty_to_be_recruited', models.IntegerField(null=True, blank=True)),
                ('buffer_number', models.IntegerField(null=True, blank=True)),
                ('to_be_recruited_with_buffer', models.IntegerField(null=True, blank=True)),
                ('planning_comments', models.CharField(max_length=2000, null=True, blank=True)),
                ('created_by', models.CharField(max_length=45)),
                ('created_on', models.DateTimeField()),
            ],
            options={
                'db_table': 'guest_faculty_planning_numbers',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuestFacultyQualification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('college', models.CharField(max_length=200)),
                ('year_of_completion', models.IntegerField()),
                ('completed', models.IntegerField()),
                ('highest_qualification', models.IntegerField()),
                ('percent_marks_cpi_cgpa', models.DecimalField(max_digits=10, decimal_places=5)),
                ('max_marks_cpi_cgpa', models.DecimalField(max_digits=10, decimal_places=5)),
                ('inserted_date', models.DateTimeField()),
                ('normalized_marks_cpi_cgpa', models.DecimalField(max_digits=10, decimal_places=5)),
            ],
            options={
                'db_table': 'guest_faculty_qualification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location_id', models.IntegerField(serialize=False, primary_key=True)),
                ('location_name', models.CharField(max_length=45)),
                ('location_state', models.CharField(max_length=45, null=True, blank=True)),
                ('location_region', models.CharField(max_length=45, null=True, blank=True)),
                ('location_country', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'location',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlanningWindowStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('planning_id', models.IntegerField()),
                ('status', models.CharField(max_length=15)),
                ('updated_by', models.CharField(max_length=100)),
                ('last_updated_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'planning_window_status',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('program_id', models.IntegerField(serialize=False, primary_key=True)),
                ('program_name', models.CharField(max_length=200)),
                ('specific_program', models.IntegerField()),
                ('client_organization', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'program',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProgramHasCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'program_has_course',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('qualification_id', models.IntegerField(serialize=False, primary_key=True)),
                ('qualification_name', models.CharField(max_length=45)),
                ('qualification_level', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'qualification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('semester_id', models.IntegerField(serialize=False, primary_key=True)),
                ('semester_name', models.CharField(max_length=45)),
                ('semester_number', models.CharField(max_length=45)),
                ('year', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'semester',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ValueLists',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('value_domain', models.CharField(max_length=45, db_column='value domain')),
                ('value', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'value_lists',
                'managed': False,
            },
        ),
    ]
