from database.mogodb_database_connection import client  
from datetime import datetime
db = client["naukri_db"] 




def insert_job_profile(company_name,job_profile,career_page_link,career_page_link_status):  
    
     # step1 create company 
     company_id = create_company(company_name)
     # step2 create job_profile 
     job_profile_id,is_new = create_job_profile(job_profile,career_page_link,career_page_link_status,company_id) 
     # step3 job_application_status_history 
     if is_new:  
          job_application_status_history(job_profile_id,"Schedule")
         
# step1
def create_company(company): 
     companies = db["companies"]
     company_doc = companies.find_one({"name":company})
     if not company_doc:
          company_result = companies.insert_one({
               "name": company
          })
          company_id = company_result.inserted_id
          print("✅ Company inserted:", company_id)
     else:
          company_id = company_doc["_id"]
    
     return company_id 

# step2 
def  create_job_profile(job_profile,career_page_link,career_page_link_status,company_id): 
     # ---- 2. Job Profile Insert ----
     job_profiles = db["job_profiles"]
     job_doc = job_profiles.find_one({"job_profile": job_profile, "company_id": company_id})
     if not job_doc:
          job_result = job_profiles.insert_one({
               "company_id": company_id,
               "job_profile": job_profile,
               "career_page_link": career_page_link,
               "career_page_link_status": career_page_link_status
          })
          job_id = job_result.inserted_id
          print("✅ Job Profile inserted:", job_id) 
          return job_id, True
     else:
      job_id = job_doc["_id"]
      return job_id, False

# step3 
def job_application_status_history(job_profile_id,status): 
     applications = db["job_application_status_history"]
     app_result = applications.insert_one({
     "job_profile_id": job_profile_id,
     "status": status,
     "changed_at": datetime.now()
     })
     print("✅ Job Application inserted:", app_result.inserted_id)


# insert employee in database 
def insert_employee(employees,company): 
      company_id =  create_company(company);  
#step1     insert employee and check duplicate 
      insert_employee_indatabase(employees,company_id) ; 
    
# step1 
def insert_employee_indatabase(employees,company_id):  
     employee_collection = db["company_employees"]
     for employee in employees:  
          try:
               if not employee_collection.find_one({'linkedin_link':employee['url'],'company_id':company_id}): 
                    result =  employee_collection.insert_one({  
                              'name' : employee['name'],
                              'linkedin_link':employee['url'], 
                              'company_id':company_id ,
                              "connection_status":"Connected",
                              "Date":datetime.now()
                         }) 
                    print("Employee is inserted in database with id",result.inserted_id) 
               else : 
                    print("Employee is already present in database")

          except Exception as e: 
            print("Error while inserting into database",e)
