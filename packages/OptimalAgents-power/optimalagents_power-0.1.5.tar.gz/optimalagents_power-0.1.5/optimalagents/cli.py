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
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>OptimalAgents.ai</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
  <style>
    :root {
      --OptimalPink: #c30399;
      --AgentsIndigo: #687efe;
    }

    body {
      background: radial-gradient(circle at top right, #fdf0ff, #f2f7ff);
      font-family: 'Segoe UI', sans-serif;
    }

    .brandOptimal {
      color: var(--OptimalPink);
    }

    .brandAgents {
      color: var(--AgentsIndigo);
    }

    .circleColor {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      line-height: 60px;
      text-align: center;
      color: #fff;
      font-weight: 600;
      margin: auto;
    }

    .bgSection {
      background: rgba(255, 255, 255, 0.6);
      backdrop-filter: blur(6px);
      border-radius: 16px;
      padding: 40px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
    }
  </style>
</head>

<body>
  <nav class="navbar navbar-expand-lg bg-white shadow-sm sticky-top">
    <div class="container">
      <a class="navbar-brand d-flex align-items-center" href="#">
        <img src="https://optimalagents.ai/images/logo-nobg-only.png" alt="Logo" width="40" class="me-2">
        <span class="fw-bold">
          <span class="brandOptimal">Optimal</span><span class="brandAgents">Agents</span>
        </span>
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link" href="https://optimalagents.ai/dashboard">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="https://docs.optimalagents.ai/agent/development" target="_blank">Docs</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <section class="py-5 text-center">
    <div class="container">
      <img src="https://optimalagents.ai/images/logo-nobg-only.png" alt="Optimal Agents Logo" class="mb-3" style="width: 100px;" />
      <h1 class="fw-bold">
        <span class="brandOptimal">Optimal</span><span class="brandAgents">Agents.ai</span>
      </h1>
      <p class="lead mt-2">Build intelligent AI agents effortlessly with our platform.</p>
      <a href="https://docs.optimalagents.ai/agent/development" class="btn btn-primary px-4 py-2 mt-3" style="background-color: var(--AgentsIndigo); border: none;">Explore Documentation</a>
    </div>
  </section>

  <section class="py-5">
    <div class="container text-center bgSection">
      <h3 class="mb-4">Brand Colors</h3>
      <div class="row justify-content-center">
        <div class="col-6 col-md-3">
          <div class="circleColor" style="background-color: var(--OptimalPink);">#c30399</div>
          <p class="mt-2">Optimal Pink</p>
        </div>
        <div class="col-6 col-md-3">
          <div class="circleColor" style="background-color: var(--AgentsIndigo);">#687efe</div>
          <p class="mt-2">Agents Indigo</p>
        </div>
      </div>
    </div>
  </section>

  <section class="py-5">
    <div class="container bgSection">
      <h3 class="text-center mb-5">Features</h3>
      <div class="row g-4">
        <div class="col-md-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <h5 class="card-title">Component Driven</h5>
              <p class="card-text">Design reusable agent parts that scale across use cases.</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <h5 class="card-title">Instant API Exposure</h5>
              <p class="card-text">Deploy your agents as APIs with a single command.</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body">
              <h5 class="card-title">Secure Infrastructure</h5>
              <p class="card-text">Built-in support for auth, scaling and observability.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="py-5">
    <div class="container bgSection">
      <h3 class="text-center mb-4">Get Started Easily</h3>
      <ul class="list-group list-group-flush mx-auto" style="max-width: 600px;">
        <li class="list-group-item">Create your agent using YAML or Python</li>
        <li class="list-group-item">Test locally with built-in tools</li>
        <li class="list-group-item">Deploy with a single CLI command</li>
        <li class="list-group-item">Monitor and update using the dashboard</li>
      </ul>
    </div>
  </section>

  <footer class="bg-white text-center py-4 mt-5 text-muted">
    <div class="container">

      Built with OptimalAgents.ai - The Ultimate Agent Development Platform | Designed and Deployed by {author_name} &copy; {year} | Powered by OptimalAgents Infrastructure
    </div>  </footer>  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>

</html>
"""

REQUIREMENTS_FASTAPI = "fastapi\nuvicorn\nrequests"
REQUIREMENTS_FLASK = "flask\nrequests"
REQUIREMENTS_REST = "requests"

from datetime import datetime
def create_project():
    year = datetime.now().year
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
        f.write(f"""FROM python:3.11-slim-bullseye AS builder
            WORKDIR /app

            # Install build dependencies and create virtual environment
            RUN python -m venv /opt/venv
            ENV PATH="/opt/venv/bin:$PATH"

            COPY requirements.txt .
            RUN pip install --no-cache-dir -r requirements.txt

            FROM python:3.11-slim-bullseye
            WORKDIR /app

            # Copy virtual environment from builder
            COPY --from=builder /opt/venv /opt/venv
            ENV PATH="/opt/venv/bin:$PATH"

            # Copy application code
            COPY . .

            # Create non-root user
            RUN useradd -m appuser && \
                chown -R appuser:appuser /app
            USER appuser

            # Set environment variables
            ENV PYTHONUNBUFFERED=1
            ENV PYTHONDONTWRITEBYTECODE=1

            # Run the application
            CMD [{run_command.split()[0]!r}, *{run_command.split()[1:]}]""")

    with open(Path(project_name) / "requirements.txt", "w") as f:
        f.write(requirements)

    with open(Path(project_name) / "templates" / "index.html", "w") as f:
        f.write(INDEX_HTML_TEMPLATE)

    print(f"\nProject '{project_name}' ({framework}) has been created successfully!")

if __name__ == "__main__":
    create_project()