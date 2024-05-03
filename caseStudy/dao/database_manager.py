import mysql.connector
from dao.service_provider import ServiceProvider


class DatabaseManager(ServiceProvider):
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="careerhubpython"
        )
        self.cursor = self.conn.cursor()

    def initialize_database(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Companies (
                CompanyID INT AUTO_INCREMENT PRIMARY KEY,
                CompanyName VARCHAR(255) NOT NULL,
                Location VARCHAR(255) NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Jobs (
                JobID INT AUTO_INCREMENT PRIMARY KEY,
                CompanyID INT NOT NULL,
                JobTitle VARCHAR(255) NOT NULL,
                JobDescription TEXT NOT NULL,
                JobLocation VARCHAR(255) NOT NULL,
                Salary DECIMAL(10,2) NOT NULL,
                JobType VARCHAR(255) NOT NULL,
                PostedDate DATE NOT NULL,
                FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Applicants (
                ApplicantID INT AUTO_INCREMENT PRIMARY KEY,
                FirstName VARCHAR(255) NOT NULL,
                LastName VARCHAR(255) NOT NULL,
                Email VARCHAR(255) NOT NULL,
                Phone VARCHAR(20) NOT NULL,
                Resume LONGBLOB
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Applications (
                ApplicationID INT AUTO_INCREMENT PRIMARY KEY,
                JobID INT NOT NULL,
                ApplicantID INT NOT NULL,
                ApplicationDate DATE NOT NULL,
                CoverLetter TEXT NOT NULL,
                FOREIGN KEY (JobID) REFERENCES Jobs(JobID),
                FOREIGN KEY (ApplicantID) REFERENCES Applicants(ApplicantID)
            )
        """)

        self.conn.commit()

    def insert_job_listing(self, job):
        query = "INSERT INTO Jobs (CompanyID, JobTitle, JobDescription, JobLocation, Salary, JobType, PostedDate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (job.company_id, job.job_title, job.job_description,
                  job.job_location, job.salary, job.job_type, job.posted_date)
        self.cursor.execute(query, values)
        self.conn.commit()

    def insert_company(self, company):
        query = "INSERT INTO Companies (CompanyName, Location) VALUES (%s, %s)"
        values = (company.company_name, company.location)
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_all_job_applications(self):
        query = "SELECT * FROM Applications"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_job_listings(self, company_id=None):
        query = "SELECT * FROM Jobs"
        if company_id:
            query += " WHERE CompanyID = %s"
            self.cursor.execute(query, (company_id,))
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_companies(self):
        query = "SELECT * FROM Companies"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_applicant(self, applicant):
        query = "INSERT INTO Applicants (FirstName, LastName, Email, Phone, Resume) VALUES (%s, %s, %s, %s, %s)"
        values = (applicant.first_name, applicant.last_name,
                  applicant.email, applicant.phone, applicant.resume)
        self.cursor.execute(query, values)
        applicant.applicant_id = self.cursor.lastrowid
        self.conn.commit()

    def get_applicants(self):
        query = "SELECT * FROM Applicants"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_job_application(self, application):
        query = "INSERT INTO Applications (JobID, ApplicantID, ApplicationDate, CoverLetter) VALUES (%s, %s, %s, %s)"
        values = (application.job_id, application.applicant_id,
                  application.application_date, application.cover_letter)
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_applications_for_job(self, job_id):
        query = "SELECT Applications.ApplicationID, Applications.JobID, Applications.ApplicantID, Applications.ApplicationDate, Applications.CoverLetter, Applicants.FirstName, Applicants.LastName FROM Applications JOIN Applicants ON Applications.ApplicantID = Applicants.ApplicantID WHERE Applications.JobID = %s"
        self.cursor.execute(query, (job_id,))
        return self.cursor.fetchall()

    def get_job_listing_by_id(self, job_id):
        query = "SELECT * FROM Jobs WHERE JobID = %s"
        self.cursor.execute(query, (job_id,))
        return self.cursor.fetchone()

    def get_applicant_by_id(self, applicant_id):
        query = "SELECT * FROM Applicants WHERE ApplicantID = %s"
        self.cursor.execute(query, (applicant_id,))
        return self.cursor.fetchone()

    def __del__(self):
        self.conn.close()