# Cold Email Pipeline

Automated job outreach using Gmail API, personalization, and rate-limiting. Works for any industry, role, or job search.

## Features

- ✅ Personalized emails with `{name}` template
- ✅ Gmail API integration with OAuth 2.0
- ✅ 20 emails/hour (configurable rate-limiting)
- ✅ Resume/CV attachment to all emails
- ✅ Error handling & logging
- ✅ Batch processing from CSV
- ✅ Works for any job role or industry

## Prerequisites

- Python 3.8+
- Gmail account
- Google Cloud Project with Gmail API enabled
- CSV file with contacts (name, email, company)
- Resume/CV file (PDF format)

## Setup

### 1. Clone Repository
```bash
git clone https://github.com/sharmamimanshi24/cold-email-pipeline.git
cd cold-email-pipeline
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Gmail API**
4. Create OAuth 2.0 credentials (Desktop application)
5. Download credentials as `client_secret_*.json`
6. Place in project folder

### 4. Configure

Create `config.json`:
```json
{
    "resume_file": "your_resume.pdf",
    "gmail_credentials": "client_secret_YOUR_PROJECT_ID.json"
}
```

### 5. Prepare Contacts

Create `all_hr_contacts_SIMPLE.csv`:
```
name,email,company
John Doe,john@example.com,TechCorp
Jane Smith,jane@startup.io,StartupXYZ
Alice Johnson,alice@bigcorp.com,BigCorp Inc
```

## Usage

```bash
python send_emails_final.py
```

**First run:** Browser will pop up to authenticate Gmail  
**After:** Emails send at 20/hour with resume attached

## Configuration

Edit `send_emails_final.py` to adjust:
- `send_rate_per_hour`: 20 (default, safe for Gmail)
- `test_mode`: False (set to True for preview)
- `limit`: None (set to number for testing)

## Customize Email Template

Edit `EMAIL_TEMPLATE` in `send_emails_final.py`:

```python
EMAIL_TEMPLATE = {
    "subject": "Your Job Role | Your Name",
    "body": """<html>
<body>
<p>Hi {name},</p>
<p>I'm interested in opportunities at {company}...</p>
</body>
</html>
"""
}
```

**Available placeholders:**
- `{name}` - Contact name
- `{company}` - Company name

## Output

Script generates `email_campaign_log_TIMESTAMP.txt`:
```
Campaign Date: 2026-07-06 10:30:45
Total Contacts: 1842
Sent: 1650
Failed: 192
```

## Error Handling

Common errors and what they mean:
- **DNS Error**: Company server offline (expected ~10% bounce rate)
- **Connection Timeout**: Gmail rate limit or network issue
- **Address Not Found**: Invalid email address in CSV
- **Mailbox Full**: Recipient's inbox is full

Script logs all errors and continues to next email automatically.

## Performance

- **Rate:** 20 emails/hour (safe for Gmail free accounts)
- **Total Time:** ~92 hours for 1800 emails (~4 days)
- **Resume Size:** Recommended <2MB
- **Throttling:** 3 minutes between emails (prevents spam filter)

## Best Practices

1. **Test with 1-5 emails first** (set `limit=5`)
2. **Keep laptop plugged in** during sending
3. **Monitor bounces** in your inbox
4. **Clean CSV** - verify all emails are valid
5. **Personalize email** - add company-specific details
6. **Use realistic sending rate** - 20/hour looks natural
7. **Update email template** - generic templates get lower response

## Use Cases

- 🎯 Fresh graduate job search
- 🎯 Career change outreach
- 🎯 Freelancer/Contractor pitches
- 🎯 Startup hiring campaigns
- 🎯 Networking at scale
- 🎯 Industry-specific job search

## CSV Format

Required columns in `all_hr_contacts_SIMPLE.csv`:
```
name,email,company
```

**Example:**
```
name,email,company
HR Manager,hr@company1.com,Company 1
Recruiter,recruiter@company2.com,Company 2
Hiring Lead,hiring@company3.com,Company 3
```

## Tech Stack

- **Backend:** Python
- **Email API:** Gmail API (OAuth 2.0)
- **Data Format:** CSV
- **Hosting:** Local machine or Cloud

## Troubleshooting

### "ModuleNotFoundError: No module named 'google'"
```bash
pip install -r requirements.txt
```

### "KeyError: 'email'"
CSV format is wrong. Check columns are: `name,email,company`

### "Gmail authentication failed"
Delete `token.json` and run again. Browser will pop up for fresh auth.

### "Emails not being sent"
Check that:
- Gmail API is enabled in Google Cloud Console
- OAuth credentials are downloaded correctly
- `config.json` has correct file names
- CSV contacts are valid

## Performance Tips

1. **Speed up:** Change `send_rate_per_hour` to 30 (faster but riskier)
2. **Slow down:** Change to 10 (more reliable, takes longer)
3. **Resume:** Keep under 1MB for faster sending
4. **Email:** Keep subject under 50 characters

## License

AGPL-3.0 - See LICENSE file

## Author

Mimanshi Sharma  
GitHub: [@sharmamimanshi24](https://github.com/sharmamimanshi24)  
Email: sharma.mimanshi24@gmail.com

## Contributing

Contributions welcome! Feel free to fork and submit PRs for:
- Better templates
- Additional features
- Bug fixes
- Documentation improvements

## Disclaimer

Use responsibly. This tool is for legitimate job outreach. Do not use for spam or unsolicited mass emails that violate Gmail's terms of service.
