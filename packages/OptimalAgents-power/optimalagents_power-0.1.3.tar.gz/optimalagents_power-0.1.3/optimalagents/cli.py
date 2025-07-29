import os
import argparse
from pathlib import Path

README_TEMPLATE = """# {project_name}

**Author**: {author_name}  
**Email**: {author_email}  
**Description**: {description}

---

## Setup


pip install -r requirements.txt


## Run


{run_command}


## Docker


docker build -t {project_name} .
docker run -d -p 8000:8000 {project_name}
"""

FASTAPI_TEMPLATE = """import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_agent_run():
    url = \"https://optimalagents.ai/check-user-credits\"
    agent_id = os.getenv("AGENT_ID")
    api_key = os.getenv("CREATOR_API_KEY")
    user_id = os.getenv("USER_ID")
    data = {"api_key": api_key, "agent_id": agent_id, "user_id": user_id}
    response = requests.post(url, json=data)
    result = response.json()

    if result.get("status") == "allowed":
        print("Agent execution permitted.")
    else:
        print(f"Error: {result.get('message')}")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content=open("templates/index.html").read(), status_code=200)
"""

FLASK_TEMPLATE = """import os
import requests
from flask import Flask, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def check_agent_run():
    url = \"https://optimalagents.ai/check-user-credits\"
    agent_id = os.getenv("AGENT_ID")
    api_key = os.getenv("CREATOR_API_KEY")
    user_id = os.getenv("USER_ID")
    data = {"api_key": api_key, "agent_id": agent_id, "user_id": user_id}
    response = requests.post(url, json=data)
    result = response.json()

    if result.get("status") == "allowed":
        print("Agent execution permitted.")
    else:
        print(f"Error: {result.get('message')}")

@app.route("/")
def index():
    return send_file("templates/index.html")

if __name__ == "__main__":
    app.run(debug=True)
"""

REST_TEMPLATE = """import os
import requests
from http.server import SimpleHTTPRequestHandler, HTTPServer
import socketserver

PORT = 8000

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/templates/index.html"
        return SimpleHTTPRequestHandler.do_GET(self)

def check_agent_run():
    url = \"https://optimalagents.ai/check-user-credits\"
    agent_id = os.getenv("AGENT_ID")
    api_key = os.getenv("CREATOR_API_KEY")
    user_id = os.getenv("USER_ID")
    data = {"api_key": api_key, "agent_id": agent_id, "user_id": user_id}
    response = requests.post(url, json=data)
    result = response.json()

    if result.get("status") == "allowed":
        print("Agent execution permitted.")
    else:
        print(f"Error: {result.get('message')}")

if __name__ == "__main__":
    os.chdir('.')
    httpd = HTTPServer(("", PORT), Handler)
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
"""

INDEX_HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Optimal Agents</title>
    <script>
        async function callApi() {
            const res = await fetch("/", { method: "GET" });
            const text = await res.text();
            console.log(text);
        }
        window.onload = callApi;
    </script>
</head>
<body>
    <h1>Hello from Optimal Agents.ai agent template</h1>
</body>
</html>
"""

REQUIREMENTS_FASTAPI = "fastapi\nuvicorn\nrequests"
REQUIREMENTS_FLASK = "flask\nrequests"
REQUIREMENTS_REST = "requests"

def create_project():
    parser = argparse.ArgumentParser(description="Create a new web project scaffold.")
    parser.add_argument("project_name", help="The name of the project.")
    args = parser.parse_args()

    project_name = args.project_name
    author_name = input("Enter your name: ")
    author_email = input("Enter your email: ")
    description = input("Enter a short project description: ")
    framework = input("Choose framework (fastapi/flask/rest): ").strip().lower()

    os.makedirs(project_name, exist_ok=True)
    os.makedirs(Path(project_name) / "static")
    os.makedirs(Path(project_name) / "templates")

    if framework == "fastapi":
        app_code = FASTAPI_TEMPLATE
        requirements = REQUIREMENTS_FASTAPI
        run_command = "uvicorn app:app --reload"
    elif framework == "flask":
        app_code = FLASK_TEMPLATE
        requirements = REQUIREMENTS_FLASK
        run_command = "python app.py"
    elif framework == "rest":
        app_code = REST_TEMPLATE
        requirements = REQUIREMENTS_REST
        run_command = "python app.py"
    else:
        print("Invalid framework.")
        return

    with open(Path(project_name) / "README.md", "w") as f:
        f.write(README_TEMPLATE.format(
            project_name=project_name,
            author_name=author_name,
            author_email=author_email,
            description=description,
            run_command=run_command
        ))

    with open(Path(project_name) / "app.py", "w") as f:
        f.write(app_code)

    with open(Path(project_name) / "Dockerfile", "w") as f:
        f.write(f"""FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [{run_command.split()[0]!r}, *{run_command.split()[1:]}]
""")

    with open(Path(project_name) / "requirements.txt", "w") as f:
        f.write(requirements)

    with open(Path(project_name) / "templates" / "index.html", "w") as f:
        f.write(INDEX_HTML_TEMPLATE)

    print(f"\nProject '{project_name}' ({framework}) has been created successfully!")

if __name__ == "__main__":
    create_project()