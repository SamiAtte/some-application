from flask import Flask, render_template, request, redirect, session
import sqlite3
import db
import config
from utilities import multi_list

import models.editing 
import models.users
import models.pages
from app1 import app



@app.route("/")
def index():
  return redirect("/pools")



