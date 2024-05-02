import mysql.connector
from datetime import datetime

class JobListing:
    def __init__(self, job_id, company_id, job_title, job_description, job_location, salary, job_type, posted_date):
        self.job_id = job_id
        self.company_id = company_id
        self.job_title = job_title
        self.job_description = job_description
        self.job_location = job_location
        self.salary = salary
        self.job_type = job_type
        self.posted_date = posted_date


class Company:
    def __init__(self, company_id, company_name, location):
        self.company_id = company_id
        self.company_name = company_name
        self.location = location


class Applicant:
    def __init__(self, applicant_id, first_name, last_name, email, phone, resume):
        self.applicant_id = applicant_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.resume = resume


class JobApplication:
    def __init__(self, application_id, job_id, applicant_id, application_date, cover_letter):
        self.application_id = application_id
        self.job_id = job_id
        self.applicant_id = applicant_id
        self.application_date = application_date
        self.cover_letter = cover_letter



class DatabaseManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="job_board"
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
        # Get all companies from the database
        query = "SELECT * FROM Companies"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_applicant(self, applicant):
        # Insert a new applicant into the database
        query = "INSERT INTO Applicants (FirstName, LastName, Email, Phone, Resume) VALUES (%s, %s, %s, %s, %s)"
        values = (applicant.first_name, applicant.last_name,
                  applicant.email, applicant.phone, applicant.resume)
        self.cursor.execute(query, values)
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
        query = "SELECT * FROM Applications WHERE JobID = %s"
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

def main():
    # Initialize the database
    db_manager = DatabaseManager()
    db_manager.initialize_database()

    while True:
        print("\nJob Board Application")
        print("1. Job Listings")
        print("2. Post a Job")
        print("3. View Job Applications")
        print("4. Job Applications")
        print("5. Companies")
        print("6. Add Company")
        print("7. View Applicants")
        print("8. Create Applicant Profile")
        print("9. Apply for a Job")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Display job listings
            print("\nJob Listings")
            job_listings = db_manager.get_job_listings()
            for job in job_listings:
                print(
                    f"Job ID: {job[0]}, Title: {job[2]}, Company: {job[1]}, Salary: {job[5]}")

        elif choice == "2":
            # Post a job
            print("\nPost a Job")
            company_id = int(input("Enter company ID: "))
            job_title = input("Enter job title: ")
            job_description = input("Enter job description: ")
            job_location = input("Enter job location: ")
            salary = float(input("Enter salary: "))
            job_type = input("Enter job type: ")
            job_listing = JobListing(None, company_id, job_title, job_description,
                                     job_location, salary, job_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            db_manager.insert_job_listing(job_listing)
            print("Job posted successfully.")

        elif choice == "3":
            # View job applications
            print("\nView Job Applications")
            job_listings = db_manager.get_job_listings()
            for job in job_listings:
                print(
                    f"Job ID: {job[0]}, Title: {job[2]}, Company: {job[1]}, Salary: {job[5]}")

            job_id = int(input("Enter job ID: "))
            applications = db_manager.get_applications_for_job(job_id)
            if applications:
                print("Applications for the selected job:")
                for app in applications:
                    print(
                        f"Application ID: {app[0]}, Applicant ID: {app[2]}, Date: {app[3]}, Cover Letter: {app[4]}")
            else:
                print("No applications found for the provided job ID.")

        elif choice == "4":
            # Job applications
            # Implement this option according to your requirements
            print("\nJob Applications")
            applications = db_manager.get_all_job_applications()
            if applications:
                for app in applications:
                    print(
                        f"Application ID: {app[0]}, Job ID: {app[1]}, Applicant ID: {app[2]}, Application Date: {app[3]}, Cover Letter: {app[4]}")
            else:
                print("No job applications found.")

        elif choice == "5":
            # Display companies
            print("\nCompanies")
            companies = db_manager.get_companies()
            for company in companies:
                print(
                    f"Company ID: {company[0]}, Name: {company[1]}, Location: {company[2]}")

        elif choice == "6":
            # Add company
            print("\nAdd Company")
            company_name = input("Enter company name: ")
            location = input("Enter company location: ")
            company = Company(None, company_name, location)
            db_manager.insert_company(company)
            print("Company added successfully.")

        elif choice == "7":
            # View applicants
            print("\nApplicants")
            applicants = db_manager.get_applicants()
            for applicant in applicants:
                print(
                    f"Applicant ID: {applicant[0]}, Name: {applicant[1]} {applicant[2]}, Email: {applicant[3]}")

        elif choice == "8":
            # Create applicant profile
            print("\nCreate Applicant Profile")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            phone = input("Enter phone: ")
            applicant = Applicant(
                None, first_name, last_name, email, phone, None)
            db_manager.insert_applicant(applicant)
            print("Applicant profile created successfully.")

        elif choice == "9":
            # Apply for a job
            print("\nApply for a Job")
            job_id = int(input("Enter job ID: "))
            applicant_id = int(input("Enter applicant ID: "))
            cover_letter = input("Enter cover letter: ")

            applicant = db_manager.get_applicant_by_id(applicant_id)
            job_listing = db_manager.get_job_listing_by_id(job_id)
            if applicant and job_listing:
                applicant.apply_for_job(job_id, cover_letter)
                print("Job application submitted successfully.")
            else:
                print("Invalid applicant ID or job ID.")

        elif choice == "10":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

