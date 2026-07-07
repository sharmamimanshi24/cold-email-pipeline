import os
import csv
import base64
import time
import json
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery

# Email Template
EMAIL_TEMPLATE = {
    "subject": "AI/ML Fresher Role | Hands-on R&D Experience",
    "body": """<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">

<p>Hi,</p>

<p>I'm <strong>Mimanshi Sharma</strong>, a final-year AI/ML student at SRMIST and currently an <strong>AI Research Intern at DRDO's DYSL-AI Lab</strong>. 
<br>I am looking for roles like <strong>Generative AI Engineer</strong>, <strong>LLM Application Developer</strong>, <strong>AI Pipeline Engineer</strong>, or <strong>Backend Engineer</strong> and other roles focused on <strong>AI and ML systems</strong>, have attached the resume for the same.</p>

<p><u><b>MY WORK</b></u></p>

<ul style="line-height: 1.8;">
  <li><b>Audio-Language Models Evaluation:</b> Evaluated 3 production models (SALMONN-7B, Audio Flamingo, Qwen2-Audio) using Automated pipelines.</li>
  
  <li><b>Built Automated Data Pipelines:</b> Built in order to curate 600 original song-cover dataset. My automation cut the manual work by 92% and sped up the data processing by 48 times. Real efficient systems that saved manual work and time.</li>
  
  <li><b>Full-Stack Memory AI Project:</b> Built and deployed a production-grade RAG application on GCP using FastAPI, Firestore, Vector Embeddings, and React. Check it out: <a href="https://memory-ai-671546906215.us-central1.run.app/">https://memory-ai-671546906215.us-central1.run.app/</a></li>
  
  <li><b>Multi-Agent system for Bias Detection:</b> Built Multi-Agent Systems in order to detect Bias.</li>
  
  <li><b>Co-authored and presented an AI research paper at ICCBI 2026</b>, an international IEEE conference, and received a Certificate of Presentation.</li>
</ul>

<p><u><b>TECHNICAL STACK</b></u> - Python, FastAPI, GCP, Vertex AI, Firestore, Cloud Run, RAG, Vector Search, Multi-Agent Systems, Ollama, LLM Evaluation</p>

<p><b>Looking for opportunities to join immediately.</b></p>

<p><b>Portfolio:</b><br>
Memory AI: <a href="https://memory-ai-671546906215.us-central1.run.app/">memory-ai-671546906215.us-central1.run.app</a><br>
GitHub: <a href="https://github.com/sharmamimanshi24">github.com/sharmamimanshi24</a><br>
LinkedIn: <a href="https://linkedin.com/in/mimanshi-sharma">linkedin.com/in/mimanshi-sharma</a></p>

<p>I'd be happy to connect and hear back from you.</p>

<p>Best regards,<br>
<b>Mimanshi Sharma</b><br>
<a href="mailto:sharma.mimanshi24@gmail.com">sharma.mimanshi24@gmail.com</a><br>
<b>+91 93153-00494</b></p>

</body>
</html>
"""
}


class EmailSender:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.service = None
    
    def load_config(self, config_file):
        """Load configuration"""
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            return {
                'resume_file': 'Mimanshi_Sharma_AI_Developer_2026.pdf',
                'gmail_credentials': 'client_secret_902839548333-9buvc2sq3mbejc9ua2iueuvj6c5q77aa.apps.googleusercontent.com.json'
            }
    
    def authenticate_gmail(self):
        """Authenticate with Gmail API"""
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        creds = None
        
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.config['gmail_credentials'], SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        self.service = discovery.build('gmail', 'v1', credentials=creds)
        print("[INFO] Gmail authentication successful")
    
    def load_resume(self):
        """Load resume as base64"""
        try:
            with open(self.config['resume_file'], 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            print(f"[ERROR] Failed to load resume: {str(e)}")
            return None
    
    def create_email_message(self, to_email, subject, body, resume_b64):
        """Create MIME email with resume"""
        message = MIMEMultipart()
        message['To'] = to_email
        message['From'] = 'sharma.mimanshi24@gmail.com'
        message['Subject'] = subject
        
        message.attach(MIMEText(body, 'html'))
        
        if resume_b64:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(base64.b64decode(resume_b64))
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', 
                           filename=self.config['resume_file'])
            message.attach(part)
        
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    
    def send_email(self, to_email, subject, body, resume_b64):
        """Send email via Gmail API"""
        try:
            message = self.create_email_message(to_email, subject, body, resume_b64)
            self.service.users().messages().send(userId='me', body=message).execute()
            return True
        except Exception as e:
            print(f"    [ERROR] Failed to send: {str(e)}")
            return False
    
    def send_campaign(self, csv_path, send_rate_per_hour=100, test_mode=False, limit=None):
        """Send emails from CSV"""
        
        if not os.path.exists(csv_path):
            print(f"[ERROR] CSV not found: {csv_path}")
            return
        
        # Read CSV
        rows = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        if limit:
            rows = rows[:limit]
        
        print(f"\n[INFO] Loaded {len(rows)} contacts from {csv_path}")
        print(f"[INFO] Test mode: {test_mode}")
        
        if test_mode:
            print(f"[INFO] Showing first 2 sample emails only")
        
        resume_b64 = self.load_resume()
        if not resume_b64:
            print("[ERROR] Could not load resume, aborting")
            return
        
        delay = 3600 / send_rate_per_hour
        sent = 0
        failed = 0
        
        for idx, row in enumerate(rows):
            # Show only first 2 in test mode
            if test_mode and idx > 1:
                break
            
            email = row['email'].strip()
            name = row['name'].strip()
            company = row['company'].strip()
            
            print(f"\n[{idx+1}/{len(rows)}] {email}")
            
            # Format email
            subject = EMAIL_TEMPLATE['subject']
            body = EMAIL_TEMPLATE['body'].format(
                name=name,
                company=company
            )
            
            if test_mode:
                print(f"  Subject: {subject}")
                print(f"  To: {email}")
                print(f"  Body preview:\n{body[:200]}...\n")
            else:
                if self.send_email(email, subject, body, resume_b64):
                    print(f"  ✓ Sent")
                    sent += 1
                else:
                    print(f"  ✗ Failed")
                    failed += 1
            
            # Throttle
            if idx < len(rows) - 1 and not test_mode:
                time.sleep(delay)
        
        if not test_mode and (sent > 0 or failed > 0):
            print(f"\n[SUMMARY] Sent: {sent} | Failed: {failed}")
            
            # Log results
            log_file = f"email_campaign_log_{int(time.time())}.txt"
            with open(log_file, 'w') as f:
                f.write(f"Campaign Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Contacts: {len(rows)}\n")
                f.write(f"Sent: {sent}\n")
                f.write(f"Failed: {failed}\n")
            print(f"[INFO] Results logged to {log_file}")


def main():
    sender = EmailSender()
    
    if not os.path.exists('all_hr_contacts_SIMPLE.csv'):
        print("[ERROR] CSV not found. Make sure all_hr_contacts_SIMPLE.csv is in this folder!")
        return
    
    print("\n" + "="*60)
    print("AI/ML COLD EMAIL CAMPAIGN - SENDING TO ALL 1835")
    print("="*60)
    
    # Authenticate once
    sender.authenticate_gmail()
    
    # Send campaign to all contacts
    sender.send_campaign(
        'all_hr_contacts_SIMPLE.csv',
        send_rate_per_hour=20,      # 20 emails/hour = 1 email every 3 minutes
        test_mode=False,             
        limit=None           
    )
    
    print("\n[CAMPAIGN COMPLETE]")


if __name__ == "__main__":
    main()
