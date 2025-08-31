from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler 
from database.insert_operation import insert_job_profile , find_companie_employee
from fastapi.middleware.cors import CORSMiddleware

# from naukri import main as bot1
from linkdin_search import main as bot2
# from read_mail import check_unseen_emails as bot3
# from linkdin_message import main as bot4 

from database.insert_operation import get_jobs
app = FastAPI()
scheduler = BackgroundScheduler()

app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,  # Set to True if you need to send cookies or authorization headers
        allow_methods=["*"],     # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
        allow_headers=["*"],     # Allows all headers
    )


# def bot1_naukri(): 
#     bot1()
#     print("Running Bot 1 - Naukri Apply")

# def bot2_employee_search():  
#     result = find_companie_employee 
#     if result['status']:
#         bot2()
#         print("Running Bot 2 - Employee Search")

# def bot3_check_connection(): 
#     bot3()
#     print("Running Bot 3 - Connection Status")

# def bot4_referral(): 
#     bot4()
#     print("Running Bot 4 - Referral Message")


# # Scheduler jobs
# scheduler.add_job(bot1_naukri, "interval", hours=1)
# scheduler.add_job(bot2_employee_search, "interval", hours=1)
# scheduler.add_job(bot3_check_connection, "interval", hours=1)
# scheduler.add_job(bot4_referral, "interval", hours=1)

# scheduler.start()

@app.get("/")
def home():
    return {"status": "Scheduler running 🚀"}


@app.get("/jobs")
def jobs():
    return  get_jobs()
@app.post("/insert_job_profile") 
def insert_job(company_name, job_role, job_link): 
     try:
         insert_job_profile(company_name, job_role, job_link)
     except Exception as e :
        print("Error while insert job",e)




