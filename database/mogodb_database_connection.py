
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
uri = "mongodb+srv://harshrajput1101:Ghg4UxdZb2f4MXBj@cluster0.cmwuz7o.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# def create_job():   

#      db = client["naukri_db"]

#      # ---- 1. Company Insert ----
#      companies = db["companies"]
#      company_doc = companies.find_one({"name": "Microsoft"})
#      if not company_doc:
#           company_result = companies.insert_one({
#                "name": "Microsoft"
#           })
#           company_id = company_result.inserted_id
#           print("✅ Company inserted:", company_id)
#      else:
#           company_id = company_doc["_id"]

#      # ---- 2. Job Profile Insert ----
#      job_profiles = db["job_profiles"]
#      job_doc = job_profiles.find_one({"job_profile": "React Developer", "company_id": company_id})
#      if not job_doc:
#           job_result = job_profiles.insert_one({
#                "company_id": company_id,
#                "job_profile": "React Developer",
#                "career_page_link": "https://microsoft.com/careers/react",
#                "career_page_link_status": "Active"
#           })
#           job_id = job_result.inserted_id
#           print("✅ Job Profile inserted:", job_id)
#      else:
#       job_id = job_doc["_id"]

#      # ---- 3. Company Employee Insert ----
#      employees = db["company_employees"]
#      emp_doc = employees.find_one({"linkedin_link": "https://linkedin.com/in/johndoe", "company_id": company_id})
#      if not emp_doc:
#           emp_result = employees.insert_one({
#                "linkedin_link": "https://linkedin.com/in/johndoe",
#                "connection_status": "Connected",
#                "company_id": company_id
#           })
#           employee_id = emp_result.inserted_id
#           print("✅ Employee inserted:", employee_id)
#      else:
#        employee_id = emp_doc["_id"]

#      # ---- 4. Referral Status History Insert ----
#      referrals = db["referral_status_history"]
#      ref_result = referrals.insert_one({
#      "employee_id": employee_id,
#      "status": "Referred",
#      "changed_at": datetime.now(),
     
#      "job_profile_id": job_id
#      })
#      print("✅ Referral inserted:", ref_result.inserted_id)

#      # ---- 5. Job Application Status History Insert ----
#      applications = db["job_application_status_history"]
#      app_result = applications.insert_one({
#      "job_profile_id": job_id,
#      "status": "Applied",
#      "changed_at": datetime.now()
#      })
#      print("✅ Job Application inserted:", app_result.inserted_id)


    
    

