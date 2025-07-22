from fastapi import FastAPI
from pydantic import BaseModel
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from database import create_db_and_tables 
from models import User 
from database import SessionDep 
import requests 
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from browser_automation import send_adobe_sign
app = FastAPI()  


@app.on_event('startup') 
def on_start(): 
     create_db_and_tables() 
     
@app.post("/user/")
def create_hero(user: User, session: SessionDep) : 
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user 
 
access_token  = "eyJhbGciOiJSUzI1NiIsIng1dSI6Imltc19uYTEta2V5LWF0LTEuY2VyIiwia2lkIjoiaW1zX25hMS1rZXktYXQtMSIsIml0dCI6ImF0In0.eyJpZCI6IjE3NDk2MjkyMTU5MzNfM2M2M2YxMTMtNzI5ZC00ZTQ5LWJjYTMtYzFmNTk0ODQxMTYxX3VlMSIsIm9yZyI6IkQ1MUMyMjVBNjg0OTJGNjYwQTQ5NUU1MkBBZG9iZU9yZyIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJjbGllbnRfaWQiOiJiZTVlY2M1MmQ0NDg0MjI5ODA4MmQyZDgzNGZkYzhhYyIsInVzZXJfaWQiOiJENTJBMjIyRjY4NDkzMDExMEE0OTVDNjBAdGVjaGFjY3QuYWRvYmUuY29tIiwiYXMiOiJpbXMtbmExIiwiYWFfaWQiOiJENTJBMjIyRjY4NDkzMDExMEE0OTVDNjBAdGVjaGFjY3QuYWRvYmUuY29tIiwiY3RwIjozLCJtb2kiOiJmMmUyNTZlIiwiZXhwaXJlc19pbiI6Ijg2NDAwMDAwIiwiY3JlYXRlZF9hdCI6IjE3NDk2MjkyMTU5MzMiLCJzY29wZSI6IkRDQVBJLG9wZW5pZCxBZG9iZUlEIn0.WpcGPL8j6-e8EurdMxZiZRNgXws7aQ6ln5gguyVL8Ew1EZjNIvpHwr-taZNEMQO1uWZa9zboy3Gw8zCFvew68P_AkoYHNd7HdCK_rhg2aYWcFKOQsyb2updf6VB7KwIowrNQwRL1lphPANpC1Taiie4ew4ywNOMx2xKqywdFbbxPNrojUW_4GzcMmVEy6JMLmu86BxF9v1sLKFdn89wsHhfMWY1NsulcJPpntaJ1HJFtF1Cs4vRNZo_PseiC4hvlIx_EcbFVrbQSALapnnQVqHCFC0DZB-akqkmdSBGxUp9ea4kLG8bBME3VPLxHyZXyBXVDOzVX2n4Lg5I8H2OV_Q"
url = "https://api.adobesign.com/api/rest/v6" 
backend_domain = ""


# adobe api 
@app.get("/alldocuments") 
def all_documents():  
     headers ={  
               "Authorization": f"Bearer {access_token}"
          }
     response = requests.get(url = f'{url}/libraryDocuments',headers=headers) 
     # Check and print response
     if response.status_code == 200:
          data = response.json()
          print("Template IDs and Names:")
          for doc in data.get("libraryDocumentList", []):
               print(f"Name: {doc['name']}, ID: {doc['id']}")
     else:
          print("Error:", response.status_code)
          print("Message:", response.text) 

def create_aggrement(user_data,template_id): 
     headers ={  
               "Authorization": f"Bearer {access_token}"
          } 
     payload = {
        "documentCreationInfo": {
            "fileInfos": [{"libraryDocumentId": template_id}],
            "name": f"{user_data['name']} - Agreement",
            "recipientSetInfos": [{
                "recipientSetMemberInfos": [{"email": user_data['email'], "name": user_data['name']}],
                "recipientSetRole": "SIGNER"
            }],
            "mergeFieldInfo": [
                {"fieldName": "name", "defaultValue": user_data["name"]},
                {"fieldName": "email", "defaultValue": user_data["email"]},
                {"fieldName": "state", "defaultValue": user_data["state"]}
            ],
            "signatureType": "ESIGN",
            "signatureFlow": "SENDER_SIGNATURE_NOT_REQUIRED",
            "callbackInfo": f'https://{backend_domain}/webhook/adobe-sign'
        }
     } 
     # get aggrement_id
     response = requests.post(f'{url}/agreements', json=payload, headers=headers)  
     
     if response.status_code == 200:
          data = response.json()
          print("Aggrement data",data)
          agreement_id = data['agreement_id']
     else:
          print("Error:", response.status_code)
          print("Message:", response.text) 
     
     # get signing URL 
     if agreement_id: 
          url_response = requests.get(f'{url}/agreements/{agreement_id}/signingUrls')
          url_response.raise_for_status()
          signing_url = url_response.json()["signingUrlSetInfos"][0]["signingUrls"][0]["esignUrl"]

     return agreement_id, signing_url


#  till now we get the sigin url  
#  registering the webhook url to listsin status of aggremenet if signed or submit  



class JoinRequest(BaseModel):
    template_name: str
    email: str
    
    
@app.post("/join")
def join_user(req: JoinRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_adobe_sign, req.template_name, req.email)
    return {"message": "Agreement will be sent shortly!"}

