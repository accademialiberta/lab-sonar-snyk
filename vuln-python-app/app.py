from flask import Flask, request
import subprocess
import sqlite3
import os

app = Flask(__name__)

# Segreto hardcoded: pessima pratica
ADMIN_PASSWORD = "admin123"

@app.route("/")
def home():
    return "Demo DevSecOps: SonarQube + Snyk"

@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    # Query SQL costruita con concatenazione: vulnerabile a SQL injection
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users VALUES ('admin', 'admin123')")

    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    cursor.execute(query)

    result = cursor.fetchone()
    if result:
        return "Login riuscito"
    return "Login fallito"

@app.route("/ping")
def ping():
    host = request.args.get("host")

    # Comando shell costruito con input utente: vulnerabile a command injection
    output = subprocess.check_output("ping -c 1 " + host, shell=True)
    return output

@app.route("/debug")
def debug():
    # Informazione sensibile esposta
    return str(os.environ)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
