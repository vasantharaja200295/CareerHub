from datetime import datetime
from entity.job_application import JobApplication
from dao.database_manager import DatabaseManager


class Applicant:
    def __init__(self, applicant_id, first_name, last_name, email, phone, resume):
        self.applicant_id = applicant_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.resume = resume

    def apply_for_job(self, job_id, cover_letter):
        application_date = datetime.now().strftime("%Y-%m-%d")
        application = JobApplication(None, job_id, self.applicant_id, application_date, cover_letter)
        db_manager = DatabaseManager()
        db_manager.insert_job_application(application)