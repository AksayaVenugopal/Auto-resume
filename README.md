# 🚀 Auto Resume Updater & ATS Score Calculator  

A powerful automation tool that fetches GitHub and LinkedIn data to keep your resume updated while also evaluating its ATS (Applicant Tracking System) score for job applications.  

## 🔥 Features  

### 📌 Auto Resume Updater  
- **GitHub API Integration**: Fetches repository details including name, URL, languages, stars, and descriptions using the GitHub REST API.  
- **LinkedIn Scraper (via RapidAPI)**: Extracts job positions, certifications, languages, and projects from a LinkedIn profile.  
- **LaTeX Resume Automation**: Updates an Overleaf LaTeX template dynamically with the fetched data using Jinja2 templating.  
- **JSON Data Caching**: Stores API responses locally to prevent excessive API calls during testing and debugging.  

### 📌 ATS Score Calculator  
- **Resume Parsing**: Uses NLP techniques to extract and analyze resume content.  
- **Job Description Matching**: Implements keyword extraction and cosine similarity for alignment analysis.  
- **Section Validation**: Checks for missing critical sections like Education, Experience, and Skills.  
- **ATS Score Breakdown**: Provides individual scores for Content, Formatting, Skills, and Style using weighted calculations.  

## 🛠️ Tech Stack  

- **Python** (3.8+)  
- **Flask** (for API handling and UI integration)  
- **GitHub API** (REST API v3)  
- **RapidAPI** (for LinkedIn scraping)  
- **Jinja2** (for LaTeX template updates)  
- **NLTK / spaCy** (for NLP-based resume analysis)  
- **Requests & JSON** (for API handling and data storage)  

## ⚙️ Setup  

1. **Clone the repository:**  
   ```sh
   git clone https://github.com/AksayaVenugopal/Auto-resume.git
   cd Auto-resume

## 🙌 Credits  

This project was inspired by rahuletto. Their initial idea and insights helped shape the development of this tool.  

