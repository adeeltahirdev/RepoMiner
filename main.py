from flask import Flask, render_template, request, jsonify, send_file
import requests
import os
import io
import zipfile
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.secret_key = 'Flash_seceret_key'
HEADERS = { "Authorization": f"token {os.getenv('GITHUB_TOKEN')}" }

@app.route('/')
def home():
    return render_template('home.html')

def clean_github_content(content):
    
    
    if isinstance(content, dict) and content.get("type") == "file":
        return {
            'type': 'file',
            'download_url': content['download_url'],
            'name': content.get('name'),
            'path': content.get('path')
        }
    
    items = []
    
    for item in content:
        items.append({
            "name": item["name"],
            "type": item["type"],
            "path": item["path"],
            "download_url": item.get("download_url"),
            "is_dir": item["type"] == 'dir'
        })
    
    items.sort(key=lambda x: not x["is_dir"])
    
    return {
        'type': 'dir',
        'items': items
    } 
    
def fetch_all_files(owner: str, repo: str, path: str = ""):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    
    print("Fetch URL:", url )
    
    if response.status_code != 200:
        return None
    
    content = response.json()
    
    if isinstance(content, dict):
        if content.get("type") == "file":
            return [{
                "path": content["path"],
                "download_url": content["download_url"]
            }]
        return []
    
    files = []
    
    for item in content:
        if item["type"] == "file":
            files.append({
                "path": item["path"],
                "download_url": item["download_url"]
            })
        elif item["type"] == "dir":
            files.extend(fetch_all_files(owner, repo, item["path"]))
            
    return files

def create_zip(files):
    memory_file = io.BytesIO()
    
    with zipfile.ZipFile(memory_file, 'w') as zip_f:
        for file in files:
            file_response = requests.get(file["download_url"])
            
            if file_response.status_code == 200:
                zip_f.writestr(file["path"], file_response.content)
            
    memory_file.seek(0)
    return memory_file

@app.route('/api/repo-content', methods = ['POST'])
def api_repo_content():
    data = request.get_json()
    
    
    if not data or 'repo_url' not in data:
       return jsonify({"error": "Missing GitHub URL!"}), 400
        
    repo_url = data['repo_url']
    path = data.get('path', '')
    
    
    try:
        parts = repo_url.strip('/').split('/')
        owner = parts[-2]
        repo = parts[-1]
    except:
       return jsonify({"error": "Invalid GitHub URL!"}), 400
        
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
       return jsonify({"error": "Failed to fetch repository"}), 400
        
    content = response.json()
    data = clean_github_content(content)
    
    if data['type'] == 'file':
        return jsonify({
            "type": "file",
            "download_url": data["download_url"],
            "name": data["name"],
            "path": data["path"]
        })
    
    return jsonify({
        "owner": owner,
        "repo": repo,
        "type": "dir",
        "items": data.get("items", []),
        "path": path
    })
    
@app.route('/api/download-folder', methods=['POST'])
def download_folder():
    data = request.get_json()
    
    repo_url = data.get("repo_url")
    path = data.get("path", "")
    
    parts = repo_url.strip('/').split('/')
    owner = parts[-2]
    repo = parts[-1]
    
    files = fetch_all_files(owner, repo, path)
    zip_file = create_zip(files)
    
    folder_name = path.strip('/').split('/')[-1] if path else repo

    print("sending Zip:", folder_name + ".zip")
    
    return send_file(
        zip_file,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"{folder_name}.zip",
    )

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)