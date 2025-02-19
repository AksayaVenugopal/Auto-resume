import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

GITHUB_API_URL = "https://api.github.com/graphql"
GITHUB_TOKEN = os.getenv("GITHUB_PAT")

# File paths
ORIGINAL_RESUME_FILE = "misc\\original_resume.tex"
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

def update_resume(data):
    """Update original resume with GitHub data."""
    if not os.path.exists(ORIGINAL_RESUME_FILE):
        raise FileNotFoundError(f"Original resume file not found: {ORIGINAL_RESUME_FILE}")
    
    with open(ORIGINAL_RESUME_FILE, "r") as resume_file:
        resume_content = resume_file.read()

    # Remove existing project section by identifying the placeholder
    resume_content = resume_content.replace("<EXISTING_PROJECTS>", "")

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

    # Write the updated content to a new file
    with open(UPDATED_RESUME_FILE, "w") as output_file:
        output_file.write(updated_content)

    print(f"Updated resume saved as: {UPDATED_RESUME_FILE}")

# GraphQL query to fetch viewer data and their repositories (ordered by creation date)
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

if __name__ == "__main__":
    try:
        print("Fetching GitHub data...")
        github_data = fetch_github_data(query)
        
        print("Updating resume...")
        update_resume(github_data)
        
        print("Process completed successfully.")
    except Exception as e:
        print("Error:", e)
