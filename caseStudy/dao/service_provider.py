from abc import ABC, abstractmethod

class ServiceProvider(ABC):
    @abstractmethod
    def initialize_database(self):
        pass

    @abstractmethod
    def insert_job_listing(self, job):
        pass

    @abstractmethod
    def insert_company(self, company):
        pass

    @abstractmethod
    def get_all_job_applications(self):
        pass

    @abstractmethod
    def get_job_listings(self, company_id=None):
        pass

    @abstractmethod
    def get_companies(self):
        pass

    @abstractmethod
    def insert_applicant(self, applicant):
        pass

    @abstractmethod
    def get_applicants(self):
        pass

    @abstractmethod
    def insert_job_application(self, application):
        pass

    @abstractmethod
    def get_applications_for_job(self, job_id):
        pass

    @abstractmethod
    def get_job_listing_by_id(self, job_id):
        pass

    @abstractmethod
    def get_applicant_by_id(self, applicant_id):
        pass