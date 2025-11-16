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
  post_pool_sql = "SELECT post_pool_title,id FROM PostPools"
  post_pool_query = db.query(post_pool_sql, [])

  post_pools = multi_list(post_pool_query,[0,1])

  return render_template("index.html", post_pools=post_pools)



