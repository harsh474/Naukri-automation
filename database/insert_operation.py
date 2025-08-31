from database.mogodb_database_connection import client  
from datetime import date
db = client["naukri_db"] 




def insert_job_profile(company_name, job_role, job_link):  
    
     # step1 create company 
     company_id = create_company(company_name)
     # step2 create job_profile 
     job_profile_id,is_new = create_job_profile( job_role, job_link,company_id) 
   
         
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
def  create_job_profile(job_role,job_link,company_id): 
     # ---- 2. Job Profile Insert ----
     job_profiles = db["job_profiles"]
     job_doc = job_profiles.find_one({"job_link": job_link, "company_id": company_id})
     if not job_doc:
          job_result = job_profiles.insert_one({
               "company_id": company_id,
               "job_role":job_role ,
               "job_link":job_link, 
               "job_status":"scheduled", 
               "referral_status":"scheduled", 
               "date": date.today().isoformat()   # ✅ stores as "2025-08-31"
          })
          job_id = job_result.inserted_id
          print("✅ Job Profile inserted:", job_id) 
          return job_id, True
     else:
      job_id = job_doc["_id"]
      return job_id, False



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
                              "date": date.today().isoformat()   # ✅ stores as "2025-08-31"

                         }) 
                    print("Employee is inserted in database with id",result.inserted_id) 
               else : 
                    print("Employee is already present in database")

          except Exception as e: 
            print("Error while inserting into database",e)




def individual_data(job): 
    return { 
        "company": job["company"].get("name"), 
        "job_role":job.get("job_role"),
        "job_link": job.get("job_link"),
        "job_status":job.get("job_status"), 
        "referral_status":job.get("referral_status"),
        "date":job.get('date')
    }


def get_jobs():
    try:
        pipeline = [
            {
                "$lookup": {
                    "from": "companies",          # companies collection name
                    "localField": "company_id",   # field in job_profiles
                    "foreignField": "_id",        # field in companies
                    "as": "company"
                }
            },
            { "$unwind": "$company" }  # ensures one company object instead of list
        ]

        jobs = db['job_profiles'].aggregate(pipeline)
        return [individual_data(job) for job in jobs]

    except Exception as e:
        print("Error while finding jobs", e)
        return []

def individual_company(company): 
    return{ 
        
    }

def find_companie_employee(): 
     companies = db["companies"].find() 
     # companies = [individual_company(company) for comapny in companies] 
     for company in companies: 
         print("id",company['_id'])  
         if not db['company_employees'].find({'company_id':company['_id']}): 
             return {"status":True,'company':company['name']}
         
     return{"status":False,'company':None}      


def update_connection_status(employees):  
    
     for employee in employees: 
          try: 
            updated_document=   db['company_employees'].find_one_and_update({'linkedin_link':employee['linkedin_link']},{'$set',{'connection_status':'connected'}})
            print("updated_document",updated_document) 
          except Exception as e: 
              print("error while updating employee document ",e) 


def update_job_profile(job_link): 
          try: 
            updated_document=   db['job_profiles'].find_one_and_update({'job_link':job_link},{'$set',{'referral_status':'sent'}})
            print("updated_document",updated_document) 
          except Exception as e: 
              print("error while updating employee document ",e) 


def get_job_profile_employee(): 
          try: 
               job_profile = db["job_profiles"].find_one({'referral_status':'scheduled'}) 
               comapny = db['companies'].find_one({'_id':job_profile['company_id']}) 
               employees = db['company_employees'].find({'company_id':job_profile['company_id']}) 
               if comapny and employees : 
                    return{'status':True,'data': [comapny,job_profile['job_role'], job_profile['job_link'],  employees]}

          except Exception as e : 
               print("Error while get_job_profile_employee",e) 
               return  {'status':False}