
# Resume Request App

A Flask-based web application that allows users to request a resume via email. User details are stored in a database, and the resume is sent as an email attachment.

---

## Features

- Collect user details (name, email) via a web form.
- Store requests in a database (SQLite).
- Send resumes to user email addresses using Flask-Mail.
- Record request logs for debugging and auditing.

---

## Prerequisites

- Python 3.8 or higher
- `pip` for package management
- A configured email account for sending emails (e.g., SMTP server)

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/resume-request-app.git
   cd resume-request-app


2. Set Up a virtual env of your choice
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables
SECRET_KEY=your_secret_key
MAIL_SERVER=smtp.mail.me.com
MAIL_PORT=587
MAIL_USERNAME=your_email@domain.com
MAIL_PASSWORD=your_password
MAIL_USE_TLS=True
MAIL_USE_SSL=False

5. Set Up the Database
   •  Ensure the instance directory exists.
   •  The database will be created automatically on app startup.

6. Run the Application
flask run

Usage
   1. Open the application in your browser at http://127.0.0.1:5000.
   2. Navigate to the resume request page.
   3. Fill out the form with your name and email.
   4. Submit the form to request a copy of the resume.

   Project Structure

   resume-request-app/
├── app.py               # Main application logic
"README.md" [noeol] 82L, 2466B
