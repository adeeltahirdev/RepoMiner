from flask import Flask, render_template, request, redirect, send_file
import requests
import zipfile
import io


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/repo-view')
def repo_view():
    
    if request.method == 'POST':
        repo_url = request.form.get('repo_url')
        
        parts = repo_url.strip('/').split('/')
        owner = parts[-2]
        repo = parts[-1]
        
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/"
        response = requests.get(url)
        contents = response.json()
        
        return render_template('repo.html', contents=contents, owner=owner, repo=repo)
    
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)