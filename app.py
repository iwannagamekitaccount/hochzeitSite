import os
import json
import subprocess
from flask import Flask, request

app = Flask(__name__)

REPO_URL = "https://github.com/iwannagamekitaccount/hochzeitSite.git"
REPO_DIR = "/tmp/repo"
FILENAME = "gaesteliste.json"

@app.route("/")
def home():
    return "Flask-Backend läuft!"

@app.route("/speichern", methods=["POST"])
def speichern():
    vorname = request.form.get("vorname")
    nachname = request.form.get("nachname")
    neuer_eintrag = {"vorname": vorname, "nachname": nachname}

    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        return "GitHub Token fehlt!", 500

    auth_repo_url = REPO_URL.replace("https://", f"https://{github_token}@")

    # 1. Repo klonen
    subprocess.run(["rm", "-rf", REPO_DIR], check=True)
    subprocess.run(["git", "clone", auth_repo_url, REPO_DIR], check=True)

    # 2. Datei laden oder neu erstellen
    file_path = os.path.join(REPO_DIR, FILENAME)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            daten = json.load(f)
    else:
        daten = []

    daten.append(neuer_eintrag)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(daten, f, indent=2, ensure_ascii=False)

    # 3. Git Konfiguration setzen (vor dem Commit!)
    subprocess.run(["git", "-C", REPO_DIR, "config", "user.email", "gaesteliste@render.local"], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "config", "user.name", "Render Gaesteliste Bot"], check=True)

    # 4. Commit & Push
    subprocess.run(["git", "-C", REPO_DIR, "add", FILENAME], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "commit", "-m", f"Neuer Eintrag: {vorname} {nachname}"], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "push", "origin", "main"], check=True)  # ggf. "master"

    return f"Danke {vorname} {nachname}, deine Daten wurden gespeichert und gepusht!"
