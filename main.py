from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.secret_key = 'Flash_seceret_key'
HEADERS = { "Authorization": f"token {os.getenv('GITHUB_TOKEN')}" }
print("TOKEN:", os.getenv('GITHUB_TOKEN'))

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

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)