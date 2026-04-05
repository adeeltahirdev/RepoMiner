from flask import Flask, render_template, request, redirect, send_file
import requests
import zipfile
import io


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/repo-view', methods=['GET', 'POST'])
@app.route('/repo-view/<owner>/<repo>/', defaults={'path': ''})
@app.route('/repo-view/<owner>/<repo>/<path:path>')
def repo_view(owner=None, repo=None, path=""):

    # STEP 1: Handle form submit
    if request.method == 'POST':
        repo_url = request.form.get('repo_url')

        if not repo_url:
            return redirect('/')

        try:
            parts = repo_url.strip('/').split('/')
            owner = parts[-2]
            repo = parts[-1]
        except:
            return "Invalid GitHub URL"

        return redirect(f"/repo-view/{owner}/{repo}/")

    # STEP 2: Handle navigation (GET)
    if not owner or not repo:
        return redirect('/')

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url)

    if response.status_code != 200:
        return "Repository not found or API error"

    contents = response.json()

    return render_template(
        'repo.html',
        contents=contents,
        owner=owner,
        repo=repo,
        path=path
    )
    
@app.route('/get-contents')
def get_contents():
    owner = request.args.get('owner')
    repo = request.args.get('repo')
    path = request.args.get('path', '')

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url)

    return response.json()

@app.route('/download-file')
def download_file():
    url = request.args.get('url')
    response = requests.get(url)
    
    return send_file(
        io.BytesIO(response.content),
        as_attachment=True,
        download_name='file'
    )

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)