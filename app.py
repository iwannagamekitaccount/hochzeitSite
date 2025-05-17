from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask-Backend läuft!"

@app.route("/speichern", methods=["POST"])
def speichern():
    vorname = request.form.get("vorname")
    nachname = request.form.get("nachname")
    print(f"Empfangen: {vorname} {nachname}")
    return f"Danke {vorname} {nachname}, deine Daten wurden gespeichert!"
