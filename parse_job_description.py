from ai import get_ai_response
def parse_job_description(job_des):
    sans = {
  "job": {
    "title": "string",
    "job_id": "string",
    "department": "string",
    "location": {
      "city": "string",
      "state": "string",
      "country": "string",
      "remote": "false"
    },
    "employment_type": "string",
    "posted_date": "YYYY-MM-DD",
    "closing_date": "YYYY-MM-DD",
    "description": "string",
    "responsibilities": [
    ],
    "qualifications": {
      "required": [
        "string",
        "string"
      ],
      "preferred": [
        "string",
        "string"
      ]
    },
    "experience_level": "string",
    "salary_range": {
      "minimum": 0,
      "maximum": 0,
      "currency": "string"
    },
    "benefits": [
      "string",
      "string"
    ],
    "company": {
      "name": "string",
      "website": "string",
      "industry": "string"
    },
    "application_instructions": "string",
    "contact_email": "string"
  }
}
    prompt=f'''I have a job description that I’d like you to format into a specific JSON structure. Here’s the job description:\
        {job_des}\
            Please format this job description into the following JSON structure:\
        {sans}

Strictly provide above json reponse only. if given info is not present mention N/A

'''
    res=get_ai_response(prompt)
    print(res)
    return get_ai_response(prompt)

# parse_job_description("Software Engineer position at TechCorp, a technology company. Job ID: SE123. Based in Seattle, Washington, USA, with remote work option. Full-time role, posted on 2025-02-01, closing on 2025-03-15. Description: Join our team to develop cutting-edge software solutions. Responsibilities: Write clean code, collaborate with teams, and troubleshoot issues. Required qualifications: Bachelor’s in Computer Science, 3+ years of coding experience. Preferred: Experience with Python, cloud computing knowledge. Mid-level role. Salary: $90,000 - $120,000 USD. Benefits: Health insurance, 401(k). Company website: www.techcorp.com. Industry: Technology. Apply by sending resume to jobs@techcorp.com with instructions to include a cover letter.]")