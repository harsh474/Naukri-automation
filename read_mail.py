import imaplib
import email
from email.header import decode_header
import time,re
from database.insert_operation import update_connection_status
# Gmail credentials (use app password, not your normal Gmail password)
EMAIL = "harshrajput1101@gmail.com"
PASSWORD = "azrl vgyj urvp pgal"


# Regex to capture LinkedIn profile URL
PROFILE_URL_RE = re.compile(r"https://(?:www|in)\.linkedin\.com/comm/in/[a-zA-Z0-9\-]+")

def extract_name(from_header):
    """Extract employee name from From header."""
    if " via LinkedIn" in from_header:
        return from_header.split(" via LinkedIn")[0].strip()
    return from_header

def decode_body(part):
    """Decode email body part to text."""
    charset = part.get_content_charset() or "utf-8"
    data = part.get_payload(decode=True)
    if data is None:
        payload = part.get_payload()
        if isinstance(payload, str):
            data = quopri.decodestring(payload)
        else:
            return ""
    try:
        text = data.decode(charset, errors="ignore")
    except:
        text = data.decode("utf-8", errors="ignore")
    return text.replace("=3D", "=").replace("&amp;", "&")

def extract_linkedin_url(msg):
    """Extract clean LinkedIn profile URL from email HTML body."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/html":
                body = decode_body(part)
                break
    else:
        body = decode_body(msg)

    # Find all matching URLs
    urls = PROFILE_URL_RE.findall(body) 
    for url in urls: 
        print(url,"\n")
    if urls:
        # Return the first clean URL (without query params)
        return urls[1].replace("/comm","")
    return None


def check_unseen_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    # Search only unseen LinkedIn invitations
    status, messages = mail.search(
        None,
        '(UNSEEN FROM "invitations@linkedin.com" SUBJECT "start a conversation with your new connection")'
    )
    email_ids = messages[0].split()
    if not email_ids:
        print("No new LinkedIn emails.")
        return
    employees=[]
    for e_id in email_ids[:2]:
        status, msg_data = mail.fetch(e_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # Name from From header
        name = extract_name(msg.get("From", ""))

        # LinkedIn URL from HTML body
        linkedin_link = extract_linkedin_url(msg)
        employees.append({name,linkedin_link})
        print("\n👤 Name:", name if name else "Not Found")
        print("🔗 LinkedIn URL:", linkedin_link if linkedin_link else "Not Found")
    
    update_connection_status(employees)
    time.sleep(12) 

    mail.logout()

# if __name__ == "__main__":
#     check_unseen_emails()