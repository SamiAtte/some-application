from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import db 
from app1 import app


@app.route("/sign_in", methods=["POST"])
def sign_in():
  session["sign_in"] = True
  return redirect(session["history"][-1])

@app.route("/cancel_sign_in", methods=["POST"])
def cancel_sign_in():
  del session["sign_in"] 
  if "sign_in_attempt" in session:
    del session["sign_in_attempt"]
  if "no_match" in session:
    del session["no_match"]
  if "name_not_available" in session:
    del session["name_not_available"]
  return redirect(session["history"][-1])



@app.route("/log_in", methods=["POST"])
def log_in():
  username = request.form["username"]
  password = request.form["password"]

  sql = "SELECT id, password_hash FROM Users WHERE username = ?"
  query = db.query(sql, [username])
  if not query:
    session["log_in_error"] = True
    return redirect(session["history"][-1])
  query = query[0]
  password_hash = query[1]

  if check_password_hash(password_hash, password):
    session["username"] = username
    session["user_id"] = query[0]
    if "log_in_error" in session:
      del session["log_in_error"] 
    return redirect(session["history"][-1])
  else:
    session["log_in_error"] = True
    return redirect(session["history"][-1])

@app.route("/log_out")
def log_out():
    del session["username"]
    del session["user_id"]
    return redirect(session["history"][-1])



@app.route("/register", methods=["POST"])
def register():
  print("täällä")
  username = request.form["username"]
  password1 = request.form["password1"]
  password2 = request.form["password2"]
  
  if password1 != password2:
    session["sign_in_attempt"] = username
    session["no_match"] = True
    #session["retry"] = True
    return redirect(session["history"][-1])

  if "no_match" in session:
    del session["no_match"];
  sql = "SELECT 1 FROM Users WHERE username = ?"
  taken = db.query(sql, [username])
  if taken:
    session["sign_in_attempt"] = username
    session["name_not_available"] = True
    #session["retry"] = True
    return redirect(session["history"][-1])

  password_hash = generate_password_hash(password1)
  try:
    sql = "INSERT INTO Users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])
  except sqlite3.IntegrityError:
    return "Error while trying to sign in"
  
  if "retry" in session:
    del session["retry"];
  if "no_match" in session:
    del session["no_match"];
  if "name_not_available" in session:
    del session["name_not_available"];
  if "sign_in_attempt" in session:
    del session["sign_in_attempt"];

  return redirect(session["history"][-1])


