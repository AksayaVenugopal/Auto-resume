from transformers import pipeline
def just_summarize(text):
# Load the summarization pipeline
    summarizer = pipeline("summarization", model="t5-small")

# Summarize the content
    summary = summarizer(text, max_length=50, min_length=20, do_sample=False)

# Output the result
    return (summary[0]['summary_text'])
# Input content
text = """
Used variety of learning modalities and support materials to facilitate learning process and accentuate presentations,
including visual, aural and social learning modalities.
Helped struggling students by providing support outside of classrooms and consistently checking in on progress.
Evaluated and supervised student activities and performance levels to provide reports on academic progress.
Performed research to serve as basis for academic writing for publication.
Collaborated with faculty members on Funded projects.
Collaborated with colleagues on curriculum revision, evaluation of course syllabi and lesson plans for Computer
Science and Artificial intelligence curriculum.
Mentored students and communicated internship and employment opportunities.
Facilitated academic and community collaborations to increase the number of community engaged research proposal
submissions to extramural funders.
"""

def project_summary(pd):
    

    # Using a summarization pipeline from Hugging Face
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize_project(description):
        # Generate the summarized text
        summary = summarizer(description, max_length=60, min_length=30, do_sample=False)[0]['summary_text']
        # Break the summary into 3 points
        points = summary.split('. ')[:3]  # Split and take first 3 sentences
        return [point.strip() + '.' for point in points if point.strip()]  # Ensure each point ends with a period

    

        # Generate summaries for each project
    summarized_projects = [summarize_project(description) for description in pd]

    # Output the summarized projects
    for i, summary in enumerate(summarized_projects, start=1):
        print(f"Project {i}:")
        for point in summary:
            print(f"- {point}")
    print()

summasummary=just_summarize(text)
print(summasummary)
project_summaries = [
    "AI-Powered Resume Generator: A cutting-edge platform utilizing NLP models (Hugging Face Transformers, BERT) to achieve 92% accuracy in tailoring resumes to job descriptions. Features include Skill Gap Analysis, which identifies missing competencies with 90% precision and recommends relevant courses via Coursera and edX APIs. Sentiment analysis of job descriptions (using NLTK and spaCy) ensures alignment with inferred company culture, achieving 85% tone accuracy. The Resume Strength Evaluation module leverages scikit-learn and TensorFlow for scoring alignment with job roles, with an accuracy of 88%. Data integration with LinkedIn and GitHub is implemented via REST APIs, ensuring a 97% success rate in dynamic updates.",
    "IoT Smart Home Automation System: A comprehensive IoT-based solution built on platforms like Raspberry Pi and Arduino, achieving 93% accuracy in predicting user preferences for home automation. The system reduces energy consumption by 25% using ML models (scikit-learn) for optimization of HVAC and lighting systems. Device communication is handled through MQTT protocols, and the system integrates with voice assistants like Alexa and Google Assistant using their respective SDKs, achieving a 96% success rate. Security features include real-time motion detection (OpenCV) and alerts, operating with 98% precision. Backend services are powered by AWS IoT Core, with a mobile app built on React Native for remote control and monitoring.",
    "E-Learning Platform with Gamification: A feature-rich e-learning solution designed to boost engagement by 35% through gamification techniques. The platform, built using React.js and Django, offers interactive quizzes and progress tracking, with a recommendation engine powered by collaborative filtering (Python, TensorFlow) achieving 92% accuracy in course suggestions. Analytics dashboards for instructors, developed using Tableau, provide actionable insights with 90% accuracy in identifying struggling students. The system supports real-time collaboration through WebRTC and has improved course completion rates by 40% in testing. Integration with video platforms like Zoom and YouTube enhances the learning experience.",
    "Blockchain-Based Voting System: A decentralized voting platform leveraging Ethereum blockchain for 100% immutability of recorded votes. The system uses biometric authentication (OpenCV, PyTorch) with a 98% accuracy rate, ensuring voter identity verification. Votes are anonymized through cryptographic hashing (SHA-256) and stored in smart contracts. Real-time result tracking has a latency of less than 2 seconds per transaction, powered by web3.js and Solidity for blockchain interactions. A secure, user-friendly frontend is built using Angular, with backend services hosted on AWS. Beta testing with 10,000 voters showed a system uptime of 99.9%, ensuring scalability for large-scale elections.",
    "Image Recognition for Wildlife Conservation: A machine learning project using convolutional neural networks (TensorFlow, Keras) to achieve 94% accuracy in identifying animal species from camera trap images. The system integrates GIS tools (ArcGIS) to map migration patterns with 92% spatial accuracy and generates automated population reports with 87% reliability. The platform reduces manual analysis time by 70%, enabling faster conservation decisions. Backend processing is managed using Python and AWS Lambda for scalability, while a React-based frontend provides researchers with interactive data visualization. Tested across 5 national parks, the system identified over 15,000 animals with a 95% success rate.",
    "Online Shopping System: A robust e-commerce platform featuring a recommendation engine powered by collaborative filtering algorithms (TensorFlow, scikit-learn) with 90% accuracy in product suggestions. The platform processes payments securely using Stripe and PayPal APIs, achieving a 98% success rate. Built with a React frontend and Node.js backend, the system supports up to 10,000 concurrent users with a response time under 1 second. Admin tools for inventory management, built using Django, operate with 95% reliability. Additional features include a chatbot for customer support (Dialogflow) and real-time order tracking integrated with Google Maps API. The platform guarantees a 99.5% uptime."
]
project_summary(project_summaries)
