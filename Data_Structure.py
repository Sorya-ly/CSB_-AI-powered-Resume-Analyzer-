import re
import json
import spacy
from spacy.matcher import PhraseMatcher


# ---------- Load Models and Data ----------
nlp = spacy.load("en_core_web_sm")

# Load predefined skill-to-job mapping
with open("job_skill_map.json", "r") as f:
    JOB_SKILL_MAP = json.load(f)


# ---------- Utility Functions ----------
def extract_emails(text):
    return re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)


def extract_phone_numbers(text):
    return re.findall(r'\+?\d[\d\s-]{8,}\d', text)


def extract_dates(text):
    return re.findall(r'\b(?:19|20)\d{2}\b', text)  # matches years like 2020, 2019


# ---------- Skill Extraction ----------
def load_skill_list():
    """A sample hardcoded list — you can expand it from datasets later."""
    return [
        "Python", "Java", "C++", "JavaScript", "React", "Node.js", "HTML", "CSS",
        "SQL", "Django", "Flask", "TensorFlow", "Keras", "Docker", "Kubernetes",
        "AWS", "Git", "Linux", "Pandas", "NumPy", "Machine Learning", "Deep Learning"
    ]


def extract_skills(text):
    """Use spaCy PhraseMatcher for flexible skill detection."""
    skills = load_skill_list()
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in skills]
    matcher.add("SKILLS", patterns)
    
    doc = nlp(text)
    matches = matcher(doc)
    found = list({doc[start:end].text for _, start, end in matches})
    return found


# ---------- Education Extraction ----------
def extract_education(text):
    """Find degree names and institutions using regex + spaCy NER."""
    doc = nlp(text)
    education_entries = []

    # Find education-related orgs
    for ent in doc.ents:
        if ent.label_ == "ORG" and re.search(r"University|College|Institute|School", ent.text, re.I):
            education_entries.append({"institution": ent.text})

    # Find degrees
    degrees = re.findall(r'(Bachelor|Master|PhD|BSc|MSc|BA|MA)[^,\n]*', text, re.I)
    for deg in degrees:
        if not education_entries:
            education_entries.append({"degree": deg})
        else:
            education_entries[0]["degree"] = deg

    return education_entries


# ---------- Experience Extraction ----------
def extract_experience(text):
    """Basic experience extraction by finding company/org and job title patterns."""
    doc = nlp(text)
    experiences = []

    for sent in doc.sents:
        if re.search(r'\b(Engineer|Developer|Manager|Analyst|Designer)\b', sent.text, re.I):
            company = None
            for ent in sent.ents:
                if ent.label_ == "ORG":
                    company = ent.text
                    break
            experiences.append({
                "company": company or "Unknown",
                "role": sent.text.strip()
            })

    return experiences


# ---------- Skill-to-Job Matching ----------
def match_jobs(found_skills):
    """Compare extracted skills to job categories in JOB_SKILL_MAP."""
    scores = {}

    for job, job_skills in JOB_SKILL_MAP.items():
        overlap = set(found_skills) & set(job_skills)
        scores[job] = len(overlap)

    # Sort jobs by most matches
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_matches = [{"title": job, "score": score} for job, score in ranked if score > 0]
    return top_matches[:3]  # Return top 3 suggestions

# ---------- Main Function ----------
def clean_resume(text):
    """Main function: extract structured data and match job categories."""
    result = {
        "contact": {
            "email": extract_emails(text),
            "phone": extract_phone_numbers(text)
        },
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }

    # Match jobs
    result["job_matches"] = match_jobs(result["skills"])
    return result


# # ---------- Example Run ----------
# if __name__ == "__main__":
#     sample_text = """
#     John Doe
#     Email: johndoe@gmail.com | Phone: +1 234 567 8901
#     Education: Bachelor of Science in Computer Science, ABC University (2020)
#     Experience:
#     - Software Engineer at XYZ Company, built web apps with Python and Django
#     - Worked with Docker and AWS for deployment
#     Skills: Python, Django, Docker, AWS, HTML, CSS
#     """

#     structured = clean_resume(sample_text)
#     print(json.dumps(structured, indent=4))