import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Fallback default questions if Google Sheets is not configured or fails
DEFAULT_QUESTIONS = [
    {
        "id": 1,
        "question": "What is the capital of France?",
        "option_a": "Berlin",
        "option_b": "Madrid",
        "option_c": "Paris",
        "option_d": "Rome",
        "correct_option": "C"
    },
    {
        "id": 2,
        "question": "Which programming language is primarily used for web styling?",
        "option_a": "Python",
        "option_b": "CSS",
        "option_c": "C++",
        "option_d": "SQL",
        "correct_option": "B"
    },
    {
        "id": 3,
        "question": "What does HTTP stand for?",
        "option_a": "HyperText Transfer Protocol",
        "option_b": "High Transfer Text Protocol",
        "option_c": "Hyperlink Text Test Process",
        "option_d": "Heavy Traffic Tool Program",
        "correct_option": "A"
    },
    {
        "id": 4,
        "question": "In Python, which keyword is used to define a function?",
        "option_a": "func",
        "option_b": "def",
        "option_c": "function",
        "option_d": "define",
        "correct_option": "B"
    },
    {
        "id": 5,
        "question": "Which data structure operates on a First-In-First-Out (FIFO) basis?",
        "option_a": "Stack",
        "option_b": "Tree",
        "option_c": "Queue",
        "option_d": "Graph",
        "correct_option": "C"
    }
]

DEFAULT_CANDIDATES = [
    {"name": "Test Candidate", "email": "candidate@example.com", "password": "password123", "roll_number": "101"},
    {"name": "Alice Smith", "email": "alice@example.com", "password": "password123", "roll_number": "102"},
    {"name": "Bob Johnson", "email": "bob@example.com", "password": "password123", "roll_number": "103"}
]

# Local cache/in-memory results fallback
LOCAL_RESULTS_FILE = os.path.join(os.path.dirname(__file__), "local_results.json")

def load_local_results():
    if os.path.exists(LOCAL_RESULTS_FILE):
        try:
            with open(LOCAL_RESULTS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_local_result_record(record):
    results = load_local_results()
    results.append(record)
    with open(LOCAL_RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=4)

def get_gspread_client():
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    
    if not creds_path or not sheet_id or not os.path.exists(creds_path):
        return None, None
        
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = Credentials.from_service_account_file(creds_path, scopes=scopes)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(sheet_id)
        return client, sheet
    except Exception as e:
        print(f"[gspread warning] Could not connect to Google Sheets: {e}")
        return None, None


def verify_candidate(email, password):
    _, sheet = get_gspread_client()
    if sheet:
        try:
            worksheet = sheet.worksheet("Candidates")
            records = worksheet.get_all_records()
            for row in records:
                if str(row.get("Email", "")).strip().lower() == email.strip().lower() and str(row.get("Password", "")) == password:
                    return {
                        "name": str(row.get("Name", "Candidate")),
                        "email": str(row.get("Email", email)),
                        "roll_number": str(row.get("RollNumber", "N/A"))
                    }
            return None
        except Exception as e:
            print(f"[gspread candidate check error]: {e}")
    
    # Fallback to local candidate check (or any email with password123)
    for cand in DEFAULT_CANDIDATES:
        if cand["email"].lower() == email.strip().lower() and cand["password"] == password:
            return cand
    if password == "password123":
        name_part = email.split("@")[0].replace(".", " ").title()
        return {"name": name_part or "Candidate", "email": email, "roll_number": "100"}
    return None


def get_questions():
    _, sheet = get_gspread_client()
    if sheet:
        try:
            worksheet = sheet.worksheet("Questions")
            records = worksheet.get_all_records()
            questions = []
            for i, row in enumerate(records, start=1):
                q_text = str(row.get("Question", "")).strip()
                if not q_text:
                    continue
                questions.append({
                    "id": int(row.get("ID", i)),
                    "question": q_text,
                    "option_a": str(row.get("OptionA", "")),
                    "option_b": str(row.get("OptionB", "")),
                    "option_c": str(row.get("OptionC", "")),
                    "option_d": str(row.get("OptionD", "")),
                    "correct_option": str(row.get("CorrectOption", "A")).strip().upper()
                })
            if questions:
                return questions
        except Exception as e:
            print(f"[gspread questions fetch error]: {e}")
            
    return DEFAULT_QUESTIONS


def save_exam_result(candidate_name, email, roll_number, score, total, percentage, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {
        "Timestamp": timestamp,
        "RollNumber": roll_number,
        "Name": candidate_name,
        "Email": email,
        "Score": score,
        "Total": total,
        "Percentage": f"{percentage:.2f}%",
        "Status": status
    }
    
    # Save to Google Sheets if connected
    saved_to_sheets = False
    _, sheet = get_gspread_client()
    if sheet:
        try:
            try:
                worksheet = sheet.worksheet("Results")
            except Exception:
                worksheet = sheet.add_worksheet(title="Results", rows="100", cols="8")
                worksheet.append_row(["Timestamp", "RollNumber", "Name", "Email", "Score", "Total", "Percentage", "Status"])
            
            worksheet.append_row([
                timestamp,
                roll_number,
                candidate_name,
                email,
                score,
                total,
                f"{percentage:.2f}%",
                status
            ])
            saved_to_sheets = True
        except Exception as e:
            print(f"[gspread save result error]: {e}")
            
    # Always save to local backup as well
    save_local_result_record(record)
    return saved_to_sheets


def get_all_results():
    _, sheet = get_gspread_client()
    if sheet:
        try:
            worksheet = sheet.worksheet("Results")
            records = worksheet.get_all_records()
            if records:
                return records
        except Exception as e:
            print(f"[gspread fetch results error]: {e}")
            
    return load_local_results()
