# PLAN C: HYBRID WORKFLOW
## Manual Research on Top 50 Companies + Automated Sending

---

## Overview

**Step 1:** Extract all 1835 HR contacts (1 CSV)
**Step 2:** Research top 50 companies (defense, space, AI startups) 
**Step 3:** Add role info to those 50 manually
**Step 4:** Send role-specific emails to 50, generic to remaining 1785

**Timeline:**
- Step 1: 2 minutes
- Step 2: 1 hour (research)
- Step 3: 30 minutes (manual entry)
- Step 4: 18 hours (automated, overnight)

---

## STEP 1: EXTRACT ALL CONTACTS

### Run extraction
```bash
cd C:\Users\sharm\cold_email
python extract_all_contacts.py
```

**Output:**
```
[INFO] Extracting contacts from PDF...
[INFO] Extracted 1835 contacts from PDF
[SUCCESS] Saved 1835 contacts to all_hr_contacts.csv
[SUCCESS] Saved 650 companies to company_list_for_research.csv

NEXT STEPS:
1. Open company_list_for_research.csv
2. Research top 50 companies (defense, space, AI startups)
3. Add role_title and role_id for those 50
4. Save and run send_emails_hybrid.py
```

**Creates 2 files:**
- `all_hr_contacts.csv` — all 1835 HR contacts (role_title & role_id empty)
- `company_list_for_research.csv` — 650 unique companies for research

---

## STEP 2: RESEARCH TOP 50 COMPANIES

### Open `company_list_for_research.csv` in Excel

**You'll see:**
```
company,domain,num_contacts,role_title,role_id
Microsoft,microsoft.com,5,,
Google,google.com,3,,
TCS,tcs.com,8,,
...
```

### Research Process

For **top 50 companies** (your targets: defense, space, AI startups), fill in:

**Defense/Space Tech:**
- GalaxEye
- Tonbo Imaging
- Satsure
- ideaForge
- Pixxel
- Skyroot
- Agnikul
- Kalpnik Geosystems

**AI/LLM Startups:**
- Sarvam AI
- Abstrabit
- Deloitte (Agentic AI team)
- Accenture

**Big Tech:**
- Google
- Microsoft
- Amazon
- Adobe

### How to Research

1. **Company careers page:** Check `/careers` or `/jobs`
   - Look for "ML Intern", "AI Fresher", "Data Science Graduate"
   
2. **LinkedIn job search:**
   - Search: `[Company] fresher` or `[Company] intern ML`
   - Copy exact job title

3. **Adzuna/Indeed/Naukri:**
   - Search: `[Company] fresher ml`

### Example Entry

```
company: Google
domain: google.com
num_contacts: 5
role_title: Associate Machine Learning Engineer (Fresher)
role_id: job-12345
```

### What to Fill In

- **role_title:** Exact job title from posting
- **role_id:** Usually in URL or job listing
  - Examples: `job-12345`, `GOOG-ML-001`, `req-789`, or even the job URL slug

**If no role found:** Leave empty (will use generic template)

---

## STEP 3: TRANSFER ROLE INFO TO MAIN CSV

### Option A: Manual (Safest)

1. Open `all_hr_contacts.csv`
2. For companies with roles found, manually add:
   ```
   name,email,company,domain,role_title,role_id
   John,john@google.com,Google,google.com,Associate ML Engineer,job-12345
   ```
3. Save

### Option B: Excel VLOOKUP (Faster)

1. Create column in `all_hr_contacts.csv`
2. Use VLOOKUP to pull from `company_list_for_research.csv`:
   ```
   =VLOOKUP(D2, [company_list_for_research.csv]Sheet1!A:E, 4, FALSE)
   ```
3. This auto-fills role_title and role_id from your research

---

## STEP 4: SEND EMAILS

### Step 4a: Test Send

```bash
python send_emails_hybrid.py
```

**Output (test mode):**
```
============================================================
HYBRID EMAIL SENDER - TEST MODE
============================================================
[INFO] Gmail authentication successful

[INFO] Loaded 1835 contacts from all_hr_contacts.csv
[INFO] With roles: 50 | Without roles: 1785
[INFO] Test mode: True

[SENDING] Emails with specific roles (50)

[1/50] john@google.com (Google)
  Subject: Application for Associate ML Engineer at Google
  Body preview: Hi John, I hope you are doing well...

[SENDING] Generic emails (1785)

[1/1785] alice@acme.com (Acme Tech)
  Subject: AI/ML Role Opportunities | Acme Tech
  Body preview: Hi Alice, I hope you are doing well...

============================================================
NEXT STEPS:
1. Review test emails above
2. Edit main() - set test_mode=False
3. Run again to send all emails
============================================================
```

**Check:**
- Role-specific emails look good? ✓
- Generic emails look good? ✓
- Recipients are correct? ✓

### Step 4b: Go Live

**Edit `send_emails_hybrid.py`:**

Change:
```python
def main():
    # ... code ...
    sender.send_from_csv(
        'all_hr_contacts.csv',
        send_rate_per_hour=100,
        test_mode=True,  # ← CHANGE TO False
        limit=None
    )
```

To:
```python
def main():
    # ... code ...
    sender.send_from_csv(
        'all_hr_contacts.csv',
        send_rate_per_hour=100,
        test_mode=False,  # ← CHANGED
        limit=None
    )
```

Then run:
```bash
python send_emails_hybrid.py
```

**What happens:**
- Sends 50 role-specific emails (to companies you researched) → ~30 mins
- Sends 1785 generic emails (to remaining companies) → ~18 hours
- **Total: ~18.5 hours** (run overnight)

---

## EMAIL TEMPLATES

### Template A: With Role (for 50 researched companies)
```
Subject: Application for {role_title} at {company}

Hi {name},
I hope you are doing well. I am Mimanshi, a final-year B.Tech AI/ML student...
I came across the {role_title} position (ID: {role_id})...
[rest of email]
```

**Higher response rate.** Specific, targeted.

### Template B: Generic (for remaining 1785)
```
Subject: AI/ML Role Opportunities | {company}

Hi {name},
I hope you are doing well. I am Mimanshi, a final-year B.Tech AI/ML student...
I am highly interested in AI/ML engineering opportunities at {company}...
[rest of email]
```

**Still effective.** Generic but professional.

---

## FILES CHECKLIST

### Before extracting:
- [ ] `extract_all_contacts.py` in cold_email folder
- [ ] `Company_Wise_HR_Contacts_-_HR_Contacts.pdf` in cold_email folder

### Before research:
- [ ] `company_list_for_research.csv` created

### Before sending:
- [ ] `all_hr_contacts.csv` created
- [ ] Role info added for top 50 companies
- [ ] `send_emails_hybrid.py` in cold_email folder
- [ ] `Mimanshi_Sharma_AI_Developer_2026.pdf` (resume) in cold_email folder
- [ ] Gmail OAuth credentials (`client_secret_*.json`, `token.json`)

---

## TIMELINE

| Step | Time | Action |
|------|------|--------|
| 1 | 2 min | Extract contacts |
| 2 | 1 hour | Research 50 companies |
| 3 | 30 min | Enter role info |
| 4a | 5 min | Test emails |
| 4b | 18+ hours | Send all (overnight) |
| **Total** | **~20 hours** | **Complete** |

---

## TIPS

**Research efficiency:**
- Use your existing 50-company tracker (defense, space, AI startups)
- For each, Google search: `[company] careers freshers ml`
- Copy exact role title from posting
- Save role ID if visible, else use job URL slug

**Common role titles to look for:**
- ML Engineer Fresher
- ML Intern
- AI Intern
- Data Science Fresher
- Graduate Engineer (ML/AI)

**If you can't find a role:**
- Leave empty
- Generic email will be sent instead
- Still a qualified outreach

---

## WHAT HAPPENS AFTER

**Day 1:** Emails sent
**Day 2-3:** HR responses start coming in
**Day 4+:** Interviews scheduled

**Pro tips:**
- Check Gmail/phone calls regularly
- Prepare for quick interviews (have demo ready)
- Update resume based on feedback
- Follow up on non-responses after 1 week

---

## READY?

### Step 1: Run extraction
```bash
python extract_all_contacts.py
```

Paste output here so I can confirm it worked. Then move to research.