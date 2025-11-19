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

    """
    Smart chatbot for resume Q&A.
    
    user_question: The user's question (string)
    resume_text: Optional - The user's resume (string)
    previous_summary: Optional - The AI summary from analyze_resume()
    """

    # Build prompt
    prompt = f"""
    You are a career assistant AI specialized in resume improvement, job matching,
    skill development, interview preparation, and career guidance.

    The user may ask questions about:
    - Resume improvements
    - Skills to learn
    - Job fit and recommendations
    - Interview questions
    - Career growth
    - ATS optimization

    Provide clear, direct, helpful answers.

    User Resume (if available):
    {resume_text}

    User question:
    {token}

    Provide the best possible answer.
    """

    # Generate AI response
    response = model.generate_content(prompt)
    return response.text.strip()
