from datetime import datetime
from dao.database_manager import DatabaseManager
from entity.applicant import Applicant
from entity.company import Company
from entity.job_listing import JobListing
from exception.application_deadline_exception import ApplicationDeadlineException
from exception.database_connection_exception import DatabaseConnectionException
from exception.file_upload_exception import FileUploadException
from exception.invalid_email_format_exception import InvalidEmailFormatException
from exception.salary_calculation_exception import SalaryCalculationException


def main():
    db_manager = DatabaseManager()
    db_manager.initialize_database()

    while True:
        print("-------------------------------------------------------------------------")
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
        print("\n")
        print('--------------------------------------------------------------------------')
        if choice == "1":
            print("\nJob Listings")
            job_listings = db_manager.get_job_listings()
            for job in job_listings:
                print(
                    f"Job ID: {job[0]}, Title: {job[2]}, Company: {job[1]}, Salary: {job[5]}")

        elif choice == "2":
            print("\nPost a Job")
            company_id = int(input("Enter company ID: "))
            job_title = input("Enter job title: ")
            job_description = input("Enter job description: ")
            job_location = input("Enter job location: ")
            salary = float(input("Enter salary: "))
            job_type = input("Enter job type: ")
            job_listing = JobListing(None, company_id, job_title, job_description,
                                     job_location, salary, job_type, datetime.now().strftime("%Y-%m-%d"))
            db_manager.insert_job_listing(job_listing)
            print("Job posted successfully.")

        elif choice == "3":
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
                        f"Application ID: {app[0]}, Applicant: {app[5]} {app[6]}, Date: {app[3]}, Cover Letter: {app[4]}")
            else:
                print("No applications found for the provided job ID.")

        elif choice == "4":
            print("\nJob Applications")
            applications = db_manager.get_all_job_applications()
            if applications:
                for app in applications:
                    print(
                        f"Application ID: {app[0]}, Job ID: {app[1]}, Applicant ID: {app[2]}, Application Date: {app[3]}, Cover Letter: {app[4]}")
            else:
                print("No job applications found.")

        elif choice == "5":
            print("\nCompanies")
            companies = db_manager.get_companies()
            for company in companies:
                print(
                    f"Company ID: {company[0]}, Name: {company[1]}, Location: {company[2]}")

        elif choice == "6":
            print("\nAdd Company")
            company_name = input("Enter company name: ")
            location = input("Enter company location: ")
            company = Company(None, company_name, location)
            db_manager.insert_company(company)
            print("Company added successfully.")

        elif choice == "7":
            print("\nApplicants")
            applicants = db_manager.get_applicants()
            for applicant in applicants:
                print(
                    f"Applicant ID: {applicant[0]}, Name: {applicant[1]} {applicant[2]}, Email: {applicant[3]}")

        elif choice == "8":
            print("\nCreate Applicant Profile")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            phone = input("Enter phone: ")
            applicant = Applicant(None, first_name, last_name, email, phone, None)
            try:
                db_manager.insert_applicant(applicant)
                print("Applicant profile created successfully.")
            except InvalidEmailFormatException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == "9":
            print("\nApply for a Job")
            job_id = int(input("Enter job ID: "))
            applicant_id = int(input("Enter applicant ID: "))
            cover_letter = input("Enter cover letter: ")

            applicant = db_manager.get_applicant_by_id(applicant_id)
            job_listing = db_manager.get_job_listing_by_id(job_id)
            if applicant and job_listing:
                applicant = Applicant(applicant[0], applicant[1], applicant[2], applicant[3], applicant[4], applicant[5])
                try:
                    applicant.apply_for_job(job_id, cover_letter)
                    print("Job application submitted successfully.")
                except ApplicationDeadlineException as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                print("Invalid applicant ID or job ID.")

        elif choice == "10":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()