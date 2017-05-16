# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('facultyapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalCourseOfferAttributes',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('course_type', models.CharField(max_length=225, verbose_name='Course Type', choices=[('regular', 'Regular'), ('flipped', 'Flipped'), ('none', 'None')])),
                ('mid_sem_weightage', models.DecimalField(verbose_name='Mid Sem Weightage', max_digits=10, decimal_places=2)),
                ('compre_weightage', models.DecimalField(verbose_name='Compre Weightage', max_digits=10, decimal_places=2)),
                ('assignment_weightage', models.DecimalField(verbose_name='Assignment Weightage', max_digits=10, decimal_places=2)),
                ('number_of_students', models.IntegerField(max_length=11, verbose_name='Number of Students attending lectures')),
                ('number_of_lectures', models.IntegerField(max_length=11, verbose_name='Number of Lectures taken')),
                ('mid_sem_evaluated_flag', models.BooleanField(verbose_name='Midsem evaluation done')),
                ('assignment_evaluated_flag', models.BooleanField(verbose_name='Assignment Evaluation Done')),
                ('compre_evaluated_flag', models.BooleanField(verbose_name='Compre Exam evaluation done')),
                ('course_location_section_detail', models.CharField(max_length=225, verbose_name='Course Location And Semester Type', choices=[('single location multiple sections', 'Single Location multiple sections'), ('multiple locations multiple sections', 'multiple locations multiple sections'), ('single location single section', 'Single Location single Section'), ('multiple locations single section', 'Multiple locations single section'), ('none', 'None')])),
                ('mid_sem_exam_students_count', models.IntegerField(default=0, max_length=11, verbose_name='Number of Students taking Mid Sem', blank=True)),
                ('dissertation_students_count', models.IntegerField(default=0, max_length=11, verbose_name='Number of students taking dissertation')),
                ('assignment_student_count', models.IntegerField(default=0, max_length=11, verbose_name='Number of students doing assignments', blank=True)),
                ('compre_exams_students_count', models.IntegerField(default=0, max_length=11, verbose_name='Number of Students taking Compre', blank=True)),
                ('honorarium_calculated_flag', models.BooleanField(default=False, verbose_name='Honorarium Calculated Flag')),
                ('last_updated_on_datetime', models.DateTimeField(default=datetime.datetime.now, verbose_name='Last updated date time', editable=False)),
                ('created_on_datetime', models.DateTimeField(default=datetime.datetime.now, verbose_name='Created Date Time', editable=False)),
                ('last_updated_by', models.CharField(max_length=225, verbose_name='Last updated by')),
            ],
            options={
                'verbose_name': 'Guest Faculty Honorarium Input Data',
                'db_table': 'additional_course_offer_attributes',
                'managed': False,
                'verbose_name_plural': 'Guest Faculty Honorarium Input Data',
            },
        ),
        migrations.CreateModel(
            name='AssessmentMaster',
            fields=[
                ('assessment_id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('assessment_identifier', models.CharField(max_length=80, verbose_name='Assessment Identifier')),
            ],
            options={
                'verbose_name': 'Guest Faculty Assessment Scores Master',
                'db_table': 'assessment_master',
                'managed': False,
                'verbose_name_plural': 'Guest Faculty Assessment Scores Master',
            },
        ),
        migrations.CreateModel(
            name='AssessmentQuestionMaster',
            fields=[
                ('question_id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('question_description', models.TextField(max_length=80, verbose_name='Question Name', blank=True)),
            ],
            options={
                'verbose_name': 'Assessment Question Master',
                'db_table': 'assessment_question',
                'managed': False,
                'verbose_name_plural': 'Assessment Question Master',
            },
        ),
        migrations.CreateModel(
            name='CategoryNameMaster',
            fields=[
                ('category_id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('category_name', models.CharField(unique=True, max_length=225)),
            ],
            options={
                'verbose_name': 'Category Name Master',
                'db_table': 'honorarium_category_master',
                'managed': False,
                'verbose_name_plural': 'Category Name Master',
            },
        ),
        migrations.CreateModel(
            name='CategoryValueMaster',
            fields=[
                ('value_id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('category_value', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Category Value Master',
                'db_table': 'honorarium_category_value_master',
                'managed': False,
                'verbose_name_plural': 'Category Value Master',
            },
        ),
        migrations.CreateModel(
            name='CurrentGFSemester',
            fields=[
                ('current_semester', models.ForeignKey(primary_key=True, serialize=False, to='facultyapp.Semester')),
            ],
            options={
                'verbose_name': 'CurrentGFSemester',
                'db_table': 'current_gf_teaching_semester',
                'managed': False,
                'verbose_name_plural': 'Current GF Teaching Semester',
            },
        ),
        migrations.CreateModel(
            name='FacultyBucketMaster',
            fields=[
                ('bucket_id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('bucket_name', models.CharField(max_length=55, verbose_name='Categery Name')),
                ('active_bucket_flag', models.BooleanField(default=1)),
                ('lower_tech_interval_gap', models.DecimalField(decimal_places=0, default=None, max_digits=10, blank=True, null=True, verbose_name='Lower Limit in Semesters for Teaching History')),
                ('upper_tech_interval_gap', models.DecimalField(decimal_places=0, default=None, max_digits=10, blank=True, null=True, verbose_name='Upper Limit in Semesters for Teaching History')),
                ('inactive_faculty_flag', models.BooleanField(verbose_name='Inactive Flag')),
                ('current_faculty_flag', models.BooleanField(verbose_name='Current Flag')),
                ('lower_bound_year', models.IntegerField()),
                ('lower_bound_sem_nbr', models.IntegerField()),
                ('upper_bound_year', models.IntegerField()),
                ('upper_bound_sem_nbr', models.IntegerField()),
                ('created_on', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('created_by', models.IntegerField(null=True, blank=True)),
                ('updated_on', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('updated_by', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ('created_on',),
                'verbose_name': 'Guest Faculty Category Definitions',
                'db_table': 'faculty_bucket_master',
                'managed': False,
                'verbose_name_plural': 'Guest Faculty Category Definitions',
            },
        ),
        migrations.CreateModel(
            name='GuestFacultyAssessmentSummary',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('assessment_identifier', models.CharField(max_length=50, verbose_name='Assessment Identifier')),
                ('assessment_date', models.DateField(verbose_name='Assessment Date')),
                ('overall_score', models.DecimalField(verbose_name='Overall Score', max_digits=10, decimal_places=2)),
                ('normalized_score', models.DecimalField(null=True, verbose_name='Normalized Score', max_digits=10, decimal_places=2, blank=True)),
                ('gf_strength', models.CharField(max_length=225, null=True, verbose_name='Overall Strengths', blank=True)),
                ('gf_weaknesses', models.CharField(max_length=225, null=True, verbose_name='Overall Weaknesses', blank=True)),
                ('recommendations_comments', models.CharField(max_length=225, null=True, verbose_name='Recommendations', blank=True)),
                ('assessor1_name', models.CharField(max_length=100, null=True, verbose_name='1st Assessor Name', blank=True)),
                ('assessor2_name', models.CharField(max_length=100, null=True, verbose_name='2nd Assessor Name', blank=True)),
                ('assessor3_name', models.CharField(max_length=100, null=True, verbose_name='3rd Assessor Name', blank=True)),
                ('sme1_name', models.CharField(max_length=100, null=True, verbose_name='1st SME Name', blank=True)),
                ('sme2_name', models.CharField(max_length=100, null=True, verbose_name='2nd SME Name', blank=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('last_updated_on', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('last_updated_by', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'db_table': 'gf_assessment_summary',
                'verbose_name': 'Guest Faculty Assessment Scores',
                'verbose_name_plural': 'Guest Faculty Assessment Scores',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GuestFacultyBucket',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('bucket_assigned_on', models.DateField(verbose_name='Bucket Assigneddata types  date')),
            ],
            options={
                'verbose_name': 'Guest Faculty Bucket',
                'db_table': 'guest_faculty_bucket',
                'managed': False,
                'verbose_name_plural': 'Guest Faculty Bucket',
            },
        ),
        migrations.CreateModel(
            name='GuestFacultyDetailedAssessment',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('assessment_score', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('key_observations', models.CharField(max_length=225, null=True, blank=True)),
                ('recommendations', models.CharField(max_length=225, null=True, blank=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('last_updated_on', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('last_updated_by', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Guest Faculty Detailed Assessment',
                'db_table': 'gf_assessment_details',
                'managed': False,
                'verbose_name_plural': 'Guest Faculty Detailed Assessment',
            },
        ),
        migrations.CreateModel(
            name='GuestFacultyHonararium',
            fields=[
            ],
            options={
                'verbose_name': 'Guest Faculty Honorarium',
                'managed': False,
                'proxy': True,
                'verbose_name_plural': 'Guest Faculty Honorarium',
            },
            bases=('facultyapp.guestfacultycourseoffer',),
        ),
        migrations.CreateModel(
            name='GuestFacultyHonorarium',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('lecture_rate_used', models.DecimalField(null=True, verbose_name='Lecture Rate Used', max_digits=10, decimal_places=2, blank=True)),
                ('lecture_honorarium', models.DecimalField(null=True, verbose_name='Lecture Honorarium', max_digits=10, decimal_places=2, blank=True)),
                ('mid_sem_qp_rate_used', models.DecimalField(null=True, verbose_name='Mid Sem Qp Rate Used', max_digits=10, decimal_places=2, blank=True)),
                ('compre_qp_rate_used', models.DecimalField(null=True, verbose_name='Compre Qp Rate Used', max_digits=10, decimal_places=2, blank=True)),
                ('qp_honorarium', models.CharField(max_length=225, null=True, blank=True)),
                ('mid_sem_eval_rate_used', models.DecimalField(null=True, verbose_name='Mid Sem Eval Rate Used', max_digits=10, decimal_places=2, blank=True)),
                ('compre_eval_rate_used', models.DecimalField(null=True, verbose_name='Compre Eval Rate Used', max_digits=10, decimal_places=2, blank=True)),
                ('assignment_eval_rate_used', models.DecimalField(null=True, verbose_name='Assignment Eval Rate Used', max_digits=10, decimal_places=2, blank=True)),
                ('evaluation_honorarium', models.DecimalField(null=True, verbose_name='Evaluation Honorarium', max_digits=10, decimal_places=2, blank=True)),
                ('dissertation_rate_used', models.DecimalField(null=True, verbose_name='Dissertation Rate Used', max_digits=10, decimal_places=2, blank=True)),
                ('dissertation_honorarium', models.DecimalField(null=True, verbose_name='Dissertation Honorarium', max_digits=10, decimal_places=2, blank=True)),
                ('course_type_section_location_honorarium', models.DecimalField(null=True, verbose_name='Course Type Section Location', max_digits=10, decimal_places=2, blank=True)),
                ('manualy_calculated_flag', models.BooleanField(default=True, verbose_name='Manually Calculated Flag')),
                ('course_type_rate_used', models.DecimalField(null=True, verbose_name='Course Type Rate Used', max_digits=10, decimal_places=2, blank=True)),
                ('total_honorarium', models.DecimalField(null=True, verbose_name='Total Honorarium', max_digits=10, decimal_places=2, blank=True)),
                ('created_on_datetime', models.DateTimeField(default=datetime.datetime.now, verbose_name='Created Date Time', editable=False)),
                ('last_updated_datetime', models.DateTimeField(default=datetime.datetime.now, verbose_name='Last updated date time', editable=False)),
                ('last_updated_by', models.CharField(max_length=225, verbose_name='Last updated by')),
                ('additional_teaching_honorarium', models.DecimalField(null=True, verbose_name='Additional Teaching Honorarium', max_digits=10, decimal_places=2, blank=True)),
            ],
            options={
                'verbose_name': 'Guest Faculty Honorarium Amounts',
                'db_table': 'guest_faculty_honorarium',
                'managed': False,
                'verbose_name_plural': 'Guest Faculty Honorarium Amounts',
            },
        ),
        migrations.CreateModel(
            name='GuestFacultyScore',
            fields=[
            ],
            options={
                'verbose_name': 'Guest Faculty  Assessment Score',
                'managed': False,
                'proxy': True,
            },
            bases=('facultyapp.guestfacultycourseoffer',),
        ),
        migrations.CreateModel(
            name='HonorariumFieldKeyWords',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('field_name', models.CharField(max_length=225, choices=[('lecture_rate_used', 'Lecture_Rate_Used'), ('mid_sem_qp_rate_used', 'Mid_Sem_qp_rate_used'), ('compre_qp_rate_used', 'Compre_qp_rate_used'), ('mid_sem_eval_rate_used', 'Mid_sem_eval_rate_used'), ('compre_eval_rate_used', 'Compre_eval_rate_used'), ('assignment_eval_rate_used', 'Assignment_eval_rate_used'), ('dissertation_rate_used', 'Dissertation_rate_used'), ('course_type_rate_used', 'Course_type_rate_used'), ('course_type_section_location_honorarium', 'Course_type_section_location_honorarium')])),
            ],
            options={
                'verbose_name': 'Honorarium Field Key Words',
                'db_table': 'honorarium_field_key_words',
                'managed': False,
                'verbose_name_plural': 'Honorarium Field Key Words',
            },
        ),
        migrations.CreateModel(
            name='HonorariumRateMaster',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('active_flag', models.BooleanField(default=True, verbose_name='Active Flag')),
                ('honorarium_rate', models.DecimalField(null=True, verbose_name='Honorariun Rate', max_digits=10, decimal_places=2, blank=True)),
                ('honorarium_amount', models.DecimalField(null=True, verbose_name='Honorariun Amount', max_digits=10, decimal_places=2, blank=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('last_updated_on', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('last_updated_by', models.CharField(max_length=225, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Honorarium Rate Master',
                'db_table': 'honorarium_rate_master',
                'managed': False,
                'verbose_name_plural': 'Honorarium Rate Master',
            },
        ),
        migrations.CreateModel(
            name='Natureofcurrentjob',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'db_table': 'nature_of_current_job',
                'managed': False,
                'verbose_name_plural': 'Nature Of Current Job',
            },
        ),
        migrations.AlterModelOptions(
            name='candidateevaluation',
            options={'managed': False, 'verbose_name': 'Guest Faculty Candidate Evaluation', 'verbose_name_plural': 'Guest Faculty Candidate Evaluation'},
        ),
        migrations.AlterModelOptions(
            name='coordinator',
            options={'managed': False, 'verbose_name': 'Coordinator Master', 'verbose_name_plural': 'Coordinator Master'},
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ('course_name',), 'verbose_name': 'Course Master', 'managed': False, 'verbose_name_plural': 'Course Master'},
        ),
        migrations.AlterModelOptions(
            name='courselocationsemesterdetail',
            options={'managed': False, 'verbose_name': 'Course Location Semester Details', 'verbose_name_plural': 'Course Location Semester Details. Assign Course to Faculty'},
        ),
        migrations.AlterModelOptions(
            name='degree',
            options={'ordering': ('degree_full_name',), 'managed': False, 'verbose_name_plural': 'Degree Master'},
        ),
        migrations.AlterModelOptions(
            name='discipline',
            options={'ordering': ('discipline_long_name',), 'managed': False, 'verbose_name': 'Academic Discipline Master', 'verbose_name_plural': 'Academic Discipline Master'},
        ),
        migrations.AlterModelOptions(
            name='facultyclassattendance',
            options={'managed': False, 'verbose_name': 'Guest Faculty Class Attendance', 'verbose_name_plural': 'Guest Faculty Class Attendance'},
        ),
        migrations.AlterModelOptions(
            name='feedbacksurvey',
            options={'managed': False, 'verbose_name': 'Faculty Feedback', 'verbose_name_plural': 'Faculty Feedback'},
        ),
        migrations.AlterModelOptions(
            name='guestfaculty',
            options={'ordering': ('name',), 'managed': False, 'verbose_name': 'Guest Faculty', 'verbose_name_plural': 'Guest Faculty'},
        ),
        migrations.AlterModelOptions(
            name='guestfacultycandidate',
            options={'ordering': ('name',), 'managed': False, 'verbose_name': 'Guest Faculty Candidate'},
        ),
        migrations.AlterModelOptions(
            name='guestfacultycourseoffer',
            options={'managed': False, 'verbose_name': 'Guest Faculty Course Assignments', 'verbose_name_plural': 'Guest Faculty Course Assignments'},
        ),
        migrations.AlterModelOptions(
            name='guestfacultyfeedbackresults',
            options={'managed': False, 'verbose_name': 'Guest Faculty Feedback', 'verbose_name_plural': 'Guest Faculty Feedback'},
        ),
        migrations.AlterModelOptions(
            name='guestfacultyqualification',
            options={'managed': False, 'verbose_name': 'Guest Faculty Qualification', 'verbose_name_plural': 'Guest Faculty Qualification'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ('location_name',), 'managed': False, 'verbose_name': 'Location Master', 'verbose_name_plural': 'Location Master'},
        ),
        migrations.AlterModelOptions(
            name='program',
            options={'ordering': ('program_name',), 'verbose_name': 'Program Master', 'managed': False, 'verbose_name_plural': 'Program Master'},
        ),
        migrations.AlterModelOptions(
            name='qualification',
            options={'managed': False, 'verbose_name': 'Qualification Master', 'verbose_name_plural': 'Qualification Master'},
        ),
        migrations.AlterModelOptions(
            name='semester',
            options={'ordering': ('semester_name',), 'managed': False, 'verbose_name': 'Semester Master', 'verbose_name_plural': 'Semester Master'},
        ),
    ]
