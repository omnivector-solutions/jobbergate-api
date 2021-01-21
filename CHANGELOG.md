## 0.10.0

- Fix: "templates" folder structure is retained after an update-application operation (#176044390)
- Added: You can now restrict legal domains for email registration, using JOBBERGATE_VALID_EMAIL_DOMAINS (#176081242)

## 0.9.1

- Fix: Allow CORS for apex URL, https://jobbergate.io

## 0.9.0

- First officially-labeled release of Jobbergate-API.
- Supersedes current prod (no labeled version)
- Recent changes include:
    - SES for emails to improve email deliverability
    - Improved build automation and deployment automation
    - Fixed password resets
    - Password character restrictions
    - Improved logging in AWS
