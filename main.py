import textwrap
from Data_Structure import clean_resume
from API_Analyzer import analyzer, QnA_analyzer
from File_handler import extract_text_from_pdf

# -------------------------
# Pretty printing for structured data
# -------------------------
def pretty_print(data, indent=0, width=80):
    """
    Recursively prints nested dictionaries and lists with proper indentation:
    - Lists of dicts: single '-' per item, sub-keys indented under it
    - Strings and numbers wrapped neatly
    """
    space = " " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{space}{key.capitalize()}:")
            pretty_print(value, indent + 2, width)

    elif isinstance(data, list):
        if all(isinstance(item, dict) for item in data):
            # List of dictionaries
            for item in data:
                print(f"{space}-")
                for k, v in item.items():
                    # Convert numbers to string
                    if not isinstance(v, str):
                        v = str(v)
                    wrapped = textwrap.fill(v, width=width, subsequent_indent=space + "  ")
                    print(f"{space}  {k}: {wrapped.strip()}")
                print()  # blank line between items
        else:
            # List of strings or numbers
            for item in data:
                if not isinstance(item, str):
                    item = str(item)
                wrapped = textwrap.fill(item, width=width, subsequent_indent=space + "  - ")
                print(f"{space}- {wrapped.strip()}")

    else:
        if not isinstance(data, str):
            data = str(data)
        wrapped = textwrap.fill(data, width=width, subsequent_indent=space)
        print(f"{space}{wrapped}")

# -------------------------
# Format AI-generated text (Markdown → bullets)
# -------------------------
import re
def format_ai_output(text, width=80, indent=0):
    cleaned = text.replace("**", "")
    cleaned = re.sub(r'^\s*\*\s+', '- ', cleaned, flags=re.MULTILINE)

    lines = cleaned.split("\n")
    formatted = []
    space = " " * indent

    for line in lines:
        if line.strip() == "":
            formatted.append("")
        else:
            wrapped = textwrap.fill(line, width=width, subsequent_indent=space)
            formatted.append(space + wrapped)

    return "\n".join(formatted)

# -------------------------
# Print numbered AI items (strengths / improvements)
# -------------------------
def print_numbered_items(items, width=80):
    """
    Prints numbered sections (AI Strengths or Improvements) neatly.
    - Numbered: 1., 2., 3.
    - Sub-items: '-' with proper indentation
    - Wraps long text
    """
    for i, item in enumerate(items, 1):
        main_key = next(iter(item))
        main_value = item[main_key]
        print(f"{i}. {main_key}: {main_value}")

        # Sub-items (Evidence / Specific suggestion etc.)
        for key, value in item.items():
            if key == main_key:
                continue
            if isinstance(value, str):
                wrapped = textwrap.fill(value, width=width, subsequent_indent="   - ")
                print(f"   - {key}: {wrapped.strip()}")
            elif isinstance(value, list):
                for sub in value:
                    wrapped = textwrap.fill(str(sub), width=width, subsequent_indent="   - ")
                    print(f"   - {key}: {wrapped.strip()}")
        print()  # blank line between items

# -------------------------
# Process resume function
# -------------------------
def process_resume(resume_path, job_description):
    try:
        print("\nLoading file...")
        raw_text = extract_text_from_pdf(resume_path)

        print("Cleaning and extracting text...")
        clean = clean_resume(raw_text)

        print("AI analysis...")
        ai_response = analyzer(raw_text, job_description)

        result = {
            "structured_data": clean,
            "ai_analysis": ai_response
        }

        print("\n========== RESULTS ==========\n")

        # Structured data
        print("📌 Extracted Structured Resume:")
        pretty_print(result["structured_data"])
        print()

        # AI analysis
        print("🤖 AI Analysis:")
        print(format_ai_output(result["ai_analysis"]))
        print("\nDone ✅\n")

        return result

    except Exception as e:
        print("❌ Error:", e)
        return None

# -------------------------
# Main interactive workflow
# -------------------------
def main():
    print("-------------------------------------------")
    print(".        AI Analyzer Application")
    print("-------------------------------------------")
    
    job_description = input("Input Job description: ")
    print("-------------------------------------------")
    resume_path = input("Input your employee resume here (must be .pdf): ")

    result = process_resume(resume_path, job_description)
    if not result:
        return

    # Optional QnA
    while True:
        print("-------------------------------------------")
        ask = input('Do you want to ask any question? (Y/N): ')
        if ask.lower() == 'y':
            question = input('Enter your question: ')
            try:
                print("\n========== QnA RESULT ==========\n")
                answer = QnA_analyzer(question, result["structured_data"])
                print(format_ai_output(answer))
                print("\nDone ✅\n")
            except Exception as e:
                print("❌ Error:", e)
        elif ask.lower() == 'n':
            print("Thanks!! Have a nice day XD")
            break
        else:
            print("Sorry, I didn't understand that. Try again.")

# -------------------------
# Entry point
# -------------------------
if __name__ == "__main__":
    main()

