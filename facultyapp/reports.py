from .models import GuestFacultyCandidate
from model_report.report import reports, ReportAdmin

class GFCandidateReport(ReportAdmin):
    title = _('Guest Faculty Candidate Report')
    model = GuestFacultyCandidate
    fields = ['application_number','name','application_status','application_submission_date','current_location_id']
    list_order_by = ('name',)
    type = 'report'

reports.register('GuestFacultyCandidate-report', GFCandidateReport)