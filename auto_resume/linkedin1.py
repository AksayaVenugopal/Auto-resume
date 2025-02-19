import os
import json
import requests
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
import re

import calendar
#Load environment variables
load_dotenv()

# Constants
LOCAL = os.getenv("LOCAL")
LINKEDIN_API_URL = "https://linkedin-data-api.p.rapidapi.com/get-profile-data-by-url"
LINKEDIN_API_KEY = os.getenv("LINKEDIN_API_KEY")
LINKEDIN_PROFILE_URL = os.getenv("LINKEDIN_PROFILE_URL")
LINKEDIN_PROFILE_URL="https://in.linkedin.com/in/subburaj-s-b22641100"
print(LINKEDIN_PROFILE_URL)
LINKEDIN_DATA_FILE = "linkedin_data.json"

# Models
from pydantic import BaseModel
from typing import List, Optional

class LinkedinDateInfo(BaseModel):
    year: int
    month: int
    day: int

class LinkedinGeo(BaseModel):
    country: str
    city: str
    full: str

class LinkedinEducation(BaseModel):
    start: LinkedinDateInfo
    end: LinkedinDateInfo
    fieldOfStudy: str
    degree: str
    grade: str
    schoolName: str
    description: str
    activities: str
    url: str
    schoolId: str

class LinkedinPosition(BaseModel):
    companyName: str
    companyUsername: str
    companyURL: str
    companyLogo: str
    companyIndustry: str
    companyStaffCountRange: str
    title: str
    location: str
    description: str
    employmentType: str
    start: LinkedinDateInfo
    end: Optional[LinkedinDateInfo] = None

class LinkedinLocaleSupport(BaseModel):
    country: str
    language: str

class Language(BaseModel):
    name: str
    proficiency: str

class Skill(BaseModel):
    name: str
    proficiency: Optional[str] = None
    hasSkillAssessment: Optional[bool] = None

class Position(BaseModel):
    title: str
    companyName: str
    location: str
    description: str
    employmentType: Optional[str] = "Full-time"
    start: LinkedinDateInfo
    end: Optional[LinkedinDateInfo] = None

class Certification(BaseModel):
    name: str

class Project(BaseModel):
    title: str
    description: str
    start: LinkedinDateInfo
    end: Optional[LinkedinDateInfo] = None

class LinkedinProject(BaseModel):
    total: int
    items: Optional[List[Project]] = None


class LinkedinProfile(BaseModel):
    id: int
    urn: str
    firstName: str
    lastName: str
    username: str
    summary: str
    headline: str
    isOpenToWork: Optional[bool] = None
    isHiring: Optional[bool] = None
    languages: List[Language]
    skills: List[Skill]
    position: List[Position]
    certifications: List[Certification]
    projects: LinkedinProject

    @classmethod
    def parse_obj(cls, obj: dict):
        # Ensure languages, skills, positions, certifications, and projects are parsed correctly
        obj['languages'] = [Language(**lang) for lang in obj.get('languages', [])]
        obj['skills'] = [Skill(**skill) for skill in obj.get('skills', [])]
        obj['position'] = [Position(**pos) for pos in obj.get('position', [])]
        obj['certifications'] = [Certification(**cert) for cert in obj.get('certifications', [])]
        obj['projects'] = LinkedinProject(**obj.get('projects', {}))
        return super().parse_obj(obj)
def fetch_readme(repo_name: str):
    """Fetch the README.md content of the given repository."""
    url = f"https://api.github.com/repos/AksayaVenugopal/{repo_name}/readme"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.raw"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"README not found for {repo_name}, skipping repository.")
        return None

# Fetch LinkedIn Data
def fetch_linkedin_data() -> LinkedinProfile:
    if LOCAL and os.path.exists(LINKEDIN_DATA_FILE):
        # Load data from local file
        with open(LINKEDIN_DATA_FILE, "r") as file:
            data = json.load(file)
    else:
        # Fetch data from API
        url = LINKEDIN_API_URL
        querystring = {"url": LINKEDIN_PROFILE_URL}
        headers = {
            "x-rapidapi-key": LINKEDIN_API_KEY,
            "x-rapidapi-host": "linkedin-data-api.p.rapidapi.com",
        }
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            data = response.json()
            # Save data locally
            with open(LINKEDIN_DATA_FILE, "w") as file:
                json.dump(data, file)
        else:
            raise Exception(f"LinkedIn fetch failed: {response.status_code}: {response.text}")
    
    # Parse data into LinkedinProfile model
    return LinkedinProfile.parse_obj(data)


# Load environment variables from the .env file
load_dotenv()

GITHUB_API_URL = "https://api.github.com/graphql"
GITHUB_TOKEN = os.getenv("GITHUB_PAT")

# File paths
ORIGINAL_RESUME_FILE = r"C:\Users\aksay\auto_resume\misc\template.tex"
UPDATED_RESUME_FILE = "updated_resume.tex"

def fetch_github_data(query: str):
    """Fetch GitHub data using GraphQL."""
    if not GITHUB_TOKEN:
        raise ValueError("GitHub Personal Access Token (GITHUB_PAT) is missing. Please check your .env file.")
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(GITHUB_API_URL, json={"query": query}, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("data")
    else:
        print("Failed to fetch GitHub data.")
        print("Headers:", headers)
        print("Response:", response.text)
        raise Exception(f"GitHub query failed: {response.status_code}: {response.text}")
def cleanData(data: str) -> str:
    data = re.sub(r'[^\x00-\x7F]+', '', data)
    data = data.replace('\u0000', '')
    return data
def update_resume(data, linkedin_data):
    if not os.path.exists(ORIGINAL_RESUME_FILE):
        raise FileNotFoundError(f"Original resume file not found: {ORIGINAL_RESUME_FILE}")

    with open(ORIGINAL_RESUME_FILE, "r") as resume_file:
        resume_content = resume_file.read()

    # Validate mandatory fields
    if not linkedin_data.summary:
        print("horayyy!!")
        raise ValueError("LinkedIn summary is missing. This field is mandatory.")
    if not linkedin_data.skills:
        raise ValueError("LinkedIn skills are missing. This field is mandatory.")

    # Get repositories sorted by createdAt
    repositories = data["viewer"]["repositories"]["nodes"]

    # Select the top 3 most recent repositories with valid README
    valid_repositories = []
    for repo in repositories:
        readme = fetch_readme(repo["name"])
        if readme:
            valid_repositories.append((repo, readme))
        if len(valid_repositories) == 3:
            break

    # Prepare the repository entries for the resume
    repo_entries = "".join([
        f"\\item \\textbf{{\\href{{{repo['url']}}}{{{repo['name']}}}}}\\\\\n"
        f"Stars: {repo['stargazerCount']}\\\\\n"
        f"Description: {readme}\\\\\n"
        for repo, readme in valid_repositories
    ])

    # Replace <REPOSITORIES> placeholder with the updated repository entries
    updated_content = resume_content.replace("<REPOSITORIES>", repo_entries)

    # Process LinkedIn sections
    experiences = linkedin_data.position
    certifications = linkedin_data.certifications
    speaks = linkedin_data.languages
    skills = linkedin_data.skills
    summary = linkedin_data.summary

    def month_number_to_abbr(month_number: int) -> str:
        return calendar.month_abbr[month_number]

    experience_entries = "".join([
        f"\\textbf{{{cleanData(exp.title)}}} \\hfill {month_number_to_abbr(exp.start.month)} {exp.start.year} - "
        f"{f'{month_number_to_abbr(exp.end.month)} {exp.end.year}' if exp.end and exp.end.year != 0 else 'Present'}\\\\\n"
        f"{cleanData(exp.companyName)} \\hfill \\textit{{{cleanData(exp.location)}}}\n"
        + (f"\n{cleanData(exp.description.split('- ')[0])}\n"
           f"\\begin{{itemize}}\n"
           + "".join([f"\\item {cleanData(point.strip())}\n" for point in exp.description.replace('%', '\\%').split('- ')[1:]]) +
           f"\\end{{itemize}}\n"
           if "- " in exp.description else f"\n{cleanData(exp.description)}\n\n")
        for exp in experiences
    ]) if experiences else ""

    certification_entries = ", ".join([cleanData(cert.name) for cert in certifications]) if certifications else ""
    speaks_entries = ", ".join([
        f"{cleanData(speak.name)} ({cleanData(speak.proficiency.replace('PROFESSIONAL_WORKING', 'Professional').replace('ELEMENTARY', 'Elementary').replace('NATIVE_OR_BILINGUAL', 'Native'))})"
        for speak in speaks
    ]) if speaks else ""

    # Update placeholders
    updated_content = updated_content.replace("<EXPERIENCES>", experience_entries)
    updated_content = updated_content.replace("<CERTIFICATIONS>", certification_entries)
    updated_content = updated_content.replace("<SPEAKS>", speaks_entries)
    updated_content = updated_content.replace("<NAME>", linkedin_data.firstName + " " + linkedin_data.lastName)
    updated_content = updated_content.replace("<LINKEDIN>", f"linkedin.com/in/{linkedin_data.username}" if linkedin_data.username else "")
    updated_content = updated_content.replace("<SUMMARY>", cleanData(summary))

    # Add skills
    skill_entries = ", ".join([cleanData(skill.name) for skill in skills])
    updated_content = updated_content.replace("<SKILLS>", skill_entries)

    # Write the updated content to a new file
    OUTPUT_FILE = r"C:\Users\aksay\auto_resume\updated_resume.tex"
    with open(OUTPUT_FILE, "w") as output_file:
        output_file.write(cleanData(updated_content))

    print(f"LaTeX file updated: {OUTPUT_FILE}")
query = """
{
  viewer {
    login
    name
    location
    websiteUrl
    email
    repositories(first: 10, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        name
        url
        createdAt
        stargazerCount
      }
    }
  }
}
"""    
# Main Execution
if __name__ == "__main__":
    try:
        linkedin_data = fetch_linkedin_data()
        print(linkedin_data)
        github_data=fetch_github_data(query)
        print("Github done")
        update_resume(github_data,linkedin_data)
    except Exception as e:
        print("Error:", e)
