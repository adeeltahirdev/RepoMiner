# 📦 RepoMiner

RepoMiner is a Flask-based web application that allows users to explore GitHub repositories in a tree-like structure and download files or entire folders as ZIP archives.

---

## 🚀 Features

- 🔍 Enter any public GitHub repository URL  
- 🌳 View repository files and folders in a hierarchical structure  
- 📂 Expand/collapse folders dynamically (no page reload)  
- 📥 Download individual files  
- 📦 Download entire folders as ZIP  
- ⚡ GitHub API integration  
- 🔐 Secure token handling via environment variables  
- 🌙 Dark mode support  
- ⏱ Auto-dismiss flash messages  

---

## 🛠 Tech Stack

- Backend: Flask (Python)  
- Frontend: HTML, CSS, JavaScript, Jinja2  
- API: GitHub REST API  
- Styling: Bootstrap 5  
- Libraries: requests, zipfile, python-dotenv  

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/adeeltahirdev/RepoMiner
cd repominer
```
---

### 2. Create virtual environment using uv
```bash
uv venv
```
Activate:

Linux / macOS:
```bash
source .venv/bin/activate
```
Windows:
```bash
.venv\Scripts\activate
```
---

### 3. Install dependencies
```bash
uv pip install flask requests python-dotenv
```
OR

```bash
pip install -r requirements.txt
```
---

## 🔐 Environment Variables

Create a `.env` file:

GITHUB_TOKEN=your_github_token_here

---

## 🔑 GitHub Token Setup

- Go to GitHub Settings → Developer Settings  
- Generate Personal Access Token  
- Select `public_repo` scope  
- Copy and add to `.env`

---

## ▶️ Run the Application
```bash
python app.py
```
Open:
http://127.0.0.1:5000/

---

## 📥 Usage

- Paste GitHub repo URL  
- Click submit  
- Browse files/folders  
- Download files or folders  

---

## ⚠️ Notes

- Works best for public repositories  
- Large repos may take time  
- API rate limits apply without token  

---

## 👨‍💻 Author

Developed by Adeel Tahir
