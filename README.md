# 📝 EpicalExam

EpicalExam is a web-based online examination portal built with Python Flask.

The system allows candidates to log in, read exam instructions, take a timed MCQ exam, submit their answers, and receive an automatically calculated result.

Instead of using a traditional database such as MySQL or PostgreSQL, EpicalExam uses Google Sheets to store users, questions, exam settings, and results.

---

## 🚀 Features

### 👤 Authentication
- Candidate and Admin login
- Flask session-based authentication
- Role-based access
- Logout functionality
- Prevent multiple active candidate sessions

### 🧑‍🎓 Candidate
- Login securely
- View exam instructions
- View exam duration and question count
- Take timed MCQ exams
- Navigate between questions
- Submit answers
- Automatic server-side evaluation
- View exam results

### 👨‍💼 Admin
- Admin dashboard
- View candidate results
- View leaderboard
- Manage exam instructions
- Manage exam duration
- Reset candidate sessions
- Export results to Excel

### 📊 Google Sheets
Google Sheets is used as the application's database.

The system can store:

- Users
- Instructions
- Exam settings
- Questions
- Results
- Leaderboard

### 🔐 Security
- Server-side score calculation
- Session-based authentication
- Role-based authorization
- Environment variables for secrets
- Google API error handling
- Retry mechanism for API quota errors

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| HTML | Page structure |
| CSS | Styling |
| JavaScript | Frontend functionality |
| Bootstrap 5 | Responsive UI |
| Google Sheets | Database |
| gspread | Google Sheets API |
| Google Service Account | API authentication |
| pandas | Data processing |
| XlsxWriter | Excel export |
| Gunicorn | Production server |
| Docker | Containerization |
| Google Cloud Run | Deployment |

---

## 🏗️ Project Architecture

```text
                    ┌──────────────────┐
                    │     Browser      │
                    │ HTML/CSS/JS      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      Flask       │
                    │     Backend      │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
          Sessions       Google Sheets    Templates
              │              │              │
              │              ▼              │
              │       ┌──────────────┐      │
              │       │    gspread   │      │
              │       └──────┬───────┘      │
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                     Google Spreadsheet
