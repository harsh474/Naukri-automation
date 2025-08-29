from fastapi import FastAPI
import requests

app = FastAPI()

# 🔹 Your Unipile Token (paste here)
UNIPILE_TOKEN = " oawPTaLs.EZ220hlBGYHCHMrYyFAFQIY+1g8cLSuZMPigdiQ+IYs="

# 🔹 Static Template Message
TEMPLATE_MESSAGE = """Hi {name},

I saw your profile and noticed you are working at {company}.
I am really interested in opportunities at your company. 
Would you be open to referring me for relevant roles?

Thanks 🙏
"""

# Function to extract LinkedIn profile ID from URL
def get_linkedin_profile_id(profile_url: str):
    url = "https://api.unipile.com/v1/linkedin/profile"
    headers = {
        "Authorization": f"Bearer {UNIPILE_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"url": profile_url}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching profile ID: {response.text}")
    
    data = response.json()
    return data.get("profile_id")

# Function to send LinkedIn message
def send_linkedin_message(profile_id: str, message: str):
    url = "https://api.unipile.com/v1/linkedin/messages"
    headers = {
        "Authorization": f"Bearer {UNIPILE_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "recipient_id": profile_id,
        "message": message
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error sending message: {response.text}")
    
    return response.json()

# FastAPI Endpoint
@app.get("/send-referral/")
def send_referral(): 
    profile_url= "https://www.linkedin.com/in/dhakad22klx/" 
    name="Deepak Dhakad"
    company ="Bitwise"
    try:
        profile_id = get_linkedin_profile_id(profile_url)
        if not profile_id:
            return {"error": "Profile not found"}

        # Personalize static message
        message = TEMPLATE_MESSAGE.format(name=name, company=company)

        # Send message
        result = send_linkedin_message(profile_id, message)
        return {"status": "success", "details": result}

    except Exception as e:
        return {"error": str(e)}



    
import { UnipileClient } from "unipile-node-sdk";

const client = new UnipileClient('https://{YOUR_DSN}', '{YOUR_ACCESS_TOKEN}');

await client.account.connectLinkedIn({ '****' });

const messages = await client.messaging.getAllMessages();
