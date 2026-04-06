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
    file_name = url.split('/')[-1]
    response = requests.get(url)
    
    return send_file(
        io.BytesIO(response.content),
        as_attachment=True,
        download_name=f"{file_name}"
    )
    
    
def get_all_files(owner, repo, path=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    items = response.json()
    files = []

    for item in items:
        if item["type"] == "file":
            files.append(item)
        elif item["type"] == "dir":
            files.extend(get_all_files(owner, repo, item["path"]))

    return files
    
@app.route('/download-folder')
def download_folder():
    owner = request.args.get('owner')
    repo = request.args.get('repo')
    path = request.args.get('path', '')

    files = get_all_files(owner, repo, path)

    if not files:
        return "Folder is empty or error occurred"

    memory_file = io.BytesIO()

    with zipfile.ZipFile(memory_file, 'w') as zf:
        for file in files:
            try:
                file_data = requests.get(file["download_url"]).content
                relative_path = file["path"].replace(path + "/", "") if path else file["path"]
                zf.writestr(relative_path, file_data)
            except:
                continue

    memory_file.seek(0)

    folder_name = path.split("/")[-1] if path else repo

    return send_file(
        memory_file,
        as_attachment=True,
        download_name=f"{folder_name}.zip"
    )

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)