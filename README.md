Last login: Sat Dec 28 14:32:22 on ttys000
You have new mail.

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
(base) MacBookPro-2:instance donfox1$ pwd
/Users/donfox1/Work/website_proj/instance
(base) MacBookPro-2:instance donfox1$ cd ..
(base) MacBookPro-2:website_proj donfox1$ ls
README.md		__pycache__/		config.py		logs/			requirements.txt	static/			tests/
__init__.py		app.py			instance/		models.py		routes.py		templates/		utils.py
(base) MacBookPro-2:website_proj donfox1$ subl .
(base) MacBookPro-2:website_proj donfox1$ conda deactivate
MacBookPro-2:website_proj donfox1$ conda activate flask_env
(flask_env) MacBookPro-2:website_proj donfox1$ ls
README.md		__pycache__/		config.py		logs/			requirements.txt	static/			tests/
__init__.py		app.py			instance/		models.py		routes.py		templates/		utils.py
(flask_env) MacBookPro-2:website_proj donfox1$ ls instance/
app.db
(flask_env) MacBookPro-2:website_proj donfox1$ ls -l instance/
total 24
-rw-r--r--  1 donfox1  staff  12288 Dec 28 14:40 app.db
(flask_env) MacBookPro-2:website_proj donfox1$ chmod +x *.db
chmod: *.db: No such file or directory
(flask_env) MacBookPro-2:website_proj donfox1$ chmod instance/app.db 
usage:	chmod [-fhv] [-R [-H | -L | -P]] [-a | +a | =a  [i][# [ n]]] mode|entry file ...
	chmod [-fhv] [-R [-H | -L | -P]] [-E | -C | -N | -i | -I] file ...
(flask_env) MacBookPro-2:website_proj donfox1$ chmod +xinstance/app.db 
usage:	chmod [-fhv] [-R [-H | -L | -P]] [-a | +a | =a  [i][# [ n]]] mode|entry file ...
	chmod [-fhv] [-R [-H | -L | -P]] [-E | -C | -N | -i | -I] file ...
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
