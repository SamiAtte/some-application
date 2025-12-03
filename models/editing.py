
from flask import Flask, render_template, request, redirect, session
import db 
from app1 import app

@app.route("/post/<int:post_id>/delete",methods=["POST"])
def delete_post(post_id):
  post_pool_id_sql = ''' SELECT post_pool FROM Posts WHERE id = ?'''
  post_pool_id = db.query(post_pool_id_sql, [post_id])[0][0]
 
  db.execute("DELETE FROM Posts WHERE id = ?",[post_id])
  db.execute("DELETE FROM PostContents WHERE post = ?",[post_id])
  db.execute("DELETE FROM CommentsSections WHERE post = ?",[post_id])

  return redirect("/post_pool/" + str(post_pool_id))


@app.route("/post_pool/<int:post_pool_id>/delete",methods=["POST"])
def delete_post_pool(post_pool_id):
  post_ids_sql = ''' SELECT id FROM Posts WHERE post_pool = ?'''
  post_ids = db.query(post_ids_sql, [post_pool_id])
  for x in post_ids:
    delete_post(x[0])
  db.execute("DELETE FROM PostPools WHERE id = ?",[post_pool_id])
  return redirect("/")


@app.route("/pool/<int:post_pool_id>/<int:user_id>/submit_post", methods=["POST"])
def submit_post(post_pool_id, user_id):
  headline = request.form["headline"]
  content = request.form["content"]
  try:
    sql = "INSERT INTO Posts (poster,post_pool,post_headline) VALUES (?,?,?)"
    db.execute(sql, [user_id, post_pool_id, headline])
  except sqlite3.IntegrityError:
    return "Error while trying to submit post"

  post_id = db.last_insert_id()

  try:
    sql = "INSERT INTO PostContents (post,content) VALUES (?,?)"
    db.execute(sql, [post_id, content])
  except sqlite3.IntegrityError:
    return "Error while trying to submit post content"

  try:
    sql = "INSERT INTO CommentsSections (post) VALUES (?)"
    db.execute(sql, [post_id])
  except sqlite3.IntegrityError:
    return "Error while trying to make comment section"

  return redirect(session["history"][-1])


@app.route("/user/<int:user_id>/create_post_pool", methods=["POST"])
def create_post_pool(user_id):
  title = request.form["title"]

  try:
    sql = "INSERT INTO PostPools (owner, post_pool_title) VALUES (?, ?)"
    db.execute(sql, [user_id, title])
  except sqlite3.IntegrityError:
    return "Error while trying to create new post pool"

  return redirect(session["history"][-1])


