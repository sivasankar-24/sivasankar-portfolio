from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import requests
import os

# Read API key from environment variable
OPENROUTER_API_KEY = os.getenv("SIVASANKAR_PORTFOLIO_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

portfolio = """
Siva Sankar S P
Aspiring Data Scientist skilled in machine learning, deep learning, NLP, and front-end development.
Experienced in building sentiment analysis models, creating dashboards, and performing software testing.
Strong in Python, SQL, and Power BI with internships across Data Science, Front-End Development, and Quality Analysis.
Technical Skills: Python, SQL, HTML, CSS, TensorFlow, Hugging Face Transformers, Scikit-learn,
OpenCV, Matplotlib, Power BI, NetworkX, Manual Testing, Postman, Black-Box Testing, Regression,
Agile, Team Collaboration, Documentation, Communication, Analytical Troubleshooting,
Team Collaboration, Leadership.
Professional Experience:
Quality Analyst Trainee Intern – Tristha Global Pvt Ltd (May 2025 – Aug 2025)
Front-End Developer Intern – Salesqueen Software Solutions (Nov 2024 – Feb 2025)
Data Science Intern – Aristocrat Research IT Solutions (Jul 2024 – Aug 2024)
Projects:
- Sentiment Analysis on IMDb Dataset: DistilBERT model (87.94% accuracy), Hugging Face, Python, customer review analysis
- Structural Equation Modeling on FinTech: SEM, Python, NetworkX, Matplotlib, banks/FinTech customer insights
- Management Systems: Responsive UIs, HTML, CSS, team workflow, leave/license tracking systems
- End-to-End Software Testing: Postman, Power BI, Sanity, Regression, Black-box testing, dashboards
Certifications: Data Science – SoftLogic, Python for Data Science – IBM, Machine Learning with Python – IBM,
Deep Learning with TensorFlow – IBM.
Education: B.E. EEE – Panimalar (2020-2024), 12th – Velammal (2018-2020), 10th – KV HVF (2008-2018)
Contact: [sivasankarsp.24@gmail.com](mailto:sivasankarsp.24@gmail.com), linkedin.com/in/siva-sankar-67154b294, github.com/sivasankar-24
"""

project_details = {
    "sentiment analysis": (
        "The Sentiment Analysis project involves building a DistilBERT NLP model on the IMDb movie reviews dataset. "
        "It classifies reviews as positive or negative, using Hugging Face Transformers and Python. Achieved 87.94% accuracy, "
        "showcasing skills in NLP and real-world application of sentiment classification."
    ),
    "structural equation modeling": (
        "Structural Equation Modeling on FinTech focused on analyzing customer satisfaction, loyalty, and service quality using SEM. "
        "This project used Python, NetworkX for graph modeling, and Matplotlib for visualizing trends. Delivered actionable insights "
        "improving fintech customer experiences."
    ),
    "management systems": (
        "The Management Systems project developed responsive front-end applications for internal tools like leave tracking. "
        "It highlights expertise in HTML, CSS, and user-centric design for efficiency."
    ),
    "end-to-end testing": (
        "The End-to-End Testing project covers API validation with Postman, dashboard creation with Power BI, "
        "and comprehensive quality assurance across software lifecycles."
    ),
}

skill_details = {
    "frontend": "Frontend skills include HTML, CSS, JavaScript, and responsive design.",
    "backend": "Backend skills include Python, SQL, REST APIs, and database management.",
    "ai": "AI skills encompass NLP, machine learning models, transformer architectures, and deep learning.",
    "testing": "Testing skills include automation frameworks, manual testing, and defect tracking."
}

class QueryRequest(BaseModel):
    message: str
    session_id: str

session_states: Dict[str, str] = {}

@app.post("/chat")
def chat(query: QueryRequest):
    prompt = query.message.lower().strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Empty message received")

    session_id = query.session_id
    if session_id not in session_states:
        session_states[session_id] = ""
    state = session_states[session_id]

    def reset_state(response_text):
        session_states[session_id] = ""
        return {"response": response_text}

    def set_state(response_text, new_state):
        session_states[session_id] = new_state
        return {"response": response_text}

    if "project" in prompt:
        if state == "awaiting_project_choice":
            for key in project_details:
                if key in prompt:
                    return reset_state(project_details[key])
            return set_state(
                "Sorry, I didn't recognize that project. Please choose from: sentiment analysis, structural equation modeling, management systems, end-to-end testing.",
                "awaiting_project_choice",
            )
        else:
            return set_state(
                "I have worked on these projects: sentiment analysis, structural equation modeling, management systems, end-to-end testing. Which one would you like to hear about?",
                "awaiting_project_choice",
            )

    if "skill" in prompt or "skills" in prompt:
        if state == "awaiting_skill_choice":
            for key in skill_details:
                if key in prompt:
                    return reset_state(skill_details[key])
            return set_state(
                "Please specify a skill area: frontend, backend, ai, or testing.",
                "awaiting_skill_choice",
            )
        else:
            return set_state(
                "My skills include frontend, backend, ai, and testing. Which skill area would you like to know more about?",
                "awaiting_skill_choice",
            )

    # For all other inputs, fallback to external AI model using portfolio data
    system_msg = {
        "role": "system",
        "content": f"You are Jarvis, a virtual assistant. Use ONLY the following portfolio data to answer user questions:\n{portfolio}"
    }
    user_msg = {"role": "user", "content": query.message}
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": "openrouter/sonoma-dusk-alpha",
        "messages": [system_msg, user_msg],
        "max_tokens": 500,
        "temperature": 0.7,
        "top_p": 1,
        "n": 1,
        "stream": False,
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
    if response.status_code != 200:
        error_text = response.text
        print(f"OpenRouter API error {response.status_code}: {error_text}")  # Debug log
        return reset_state("Sorry, I'm currently unable to respond. Please try again later.")
    data = response.json()
    answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    session_states[session_id] = ""
    return {"response": answer.strip()}
