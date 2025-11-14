import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API key from environment (make sure .env has GEMINI_API_KEY=your_key)
genai.configure(api_key=os.getenv("AIzaSyDvrkArLX2MJQPkoofYfGOVKmOsCNfZUjk"))

def load_prompt (file_path):
    with open(file_path,'r') as f:
        return f.read().strip()

job_template = load_prompt("job_prompt.txt")
strength_template = load_prompt("strength_prompt.txt")
improved_template = load_prompt("improve_prompt.txt")


def analyzer(resume_text, job_description=None):
    if not resume_text:
        return {"error": "Resume text is required for analysis."}

    model = genai.GenerativeModel("gemini-2.5-flash")

    base_prompt = f"""

    {job_template} 
    --------------------------------------------
    {strength_template}
    --------------------------------------------
    {improved_template}

    Resume:
    {resume_text}

    In conclusion: (Summarize the whole analysis in 3 sentences and give a motivation in 2 sentences as well)
    """

    if job_description:
        base_prompt += f"""
        Compare the resume to this job description:
        {job_description}
        """

    response = model.generate_content(base_prompt)
    return response.text.strip()

def QnA_analyzer (token, resume_text=None):
    if not token:
        return {"error": "Token is required for Ai Chat."}
    
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are an assistant that MUST base all answers ONLY on the resume and optional job description below.
    Do NOT invent experience or skills that are not present in the resume.
    If information is missing, say so briefly.

    Resume:
    {resume_text}

    """
        
    prompt += f"""
    User question:
    {token}

    Instructions:
    - Use only the resume (and job description if provided) to answer.
    - Be concise, factual, and cite the exact resume line or phrase you used as evidence when applicable.
    - If the resume lacks the information needed to answer, respond: "Information not present in resume."
    Now generate the answer.
    """
    answer = model.generate_content(prompt)
    return answer.text.strip()
    
