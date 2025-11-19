from Data_Structure import clean_resume
from API_Analyzer import analyzer, QnA_analyzer
from File_handler import extract_text_from_pdf

def process_resume(path, job_description=None):
    print("\nLoading file...")
    raw_text = extract_text_from_pdf(path)

    print("Cleaning and Extracting text...")
    clean = clean_resume(raw_text)

    print("AI analysis...")
    ai_response = analyzer(clean, job_description)

    # parsed_ai = extract_json(ai_response)

    return {
        "structured_data": clean,
        "ai_analysis": ai_response
    }


def main():
    print("-------------------------------------------")
    print(".        AI Analyzer Application")
    print("-------------------------------------------")
    Job_description = input(str("Input Job description: "))
    print("-------------------------------------------")
    Inputted_resume = input(str("Input your employee resume here (must be .pdf): "))

    try:
        print("\n========== PROCESS ==========\n")
        result = process_resume(Inputted_resume, Job_description )

        print("\n========== RESULTS ==========\n")

        print("📌 Extracted Structure:")
        print(result["structured_data"], "\n")

        print("🤖 AI Analysis:")
        print(result["ai_analysis"], "\n")

        print("Done ✅")

    except Exception as e:
        print("❌ Error:", e)
    

    #QnA with the recruiter 
    while True: 
        print("-------------------------------------------")
        agree = input(str('Do u want have any question? (Y/N): '))

        if agree.lower() == 'y':
            token = input(str('Enter your question: '))
            try:
                print("\n========== RESULTS ==========\n")
                print(QnA_analyzer(token, Inputted_resume))
                print("Done ✅")
            except Exception as e: 
                print("❌ Error:", e)
        elif agree.lower()== 'n':
            print("Thanks!! Have a nice day XD")
            break
        else:
            print("Sorry, I didn't understand that. Try again.")

if __name__ == "__main__":
    main()
