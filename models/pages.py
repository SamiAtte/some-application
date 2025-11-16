from flask import Flask, render_template, request, redirect, session
import db 
from utilities import multi_list
from app1 import app

@app.route("/user/<int:user_id>")
def user_page(user_id):
  user_sql = "SELECT username FROM Users WHERE id = ?"
  user_query = db.query(user_sql, [user_id])[0]

  post_sql= "SELECT post_pool_title,id FROM PostPools WHERE owner = ?"
  post_query = db.query(post_sql, [user_id])

  post_pools = multi_list(post_query,[0,1])

  return render_template("user-page.html", user_id=user_id, username=user_query[0], post_pools=post_pools)


@app.route("/post_pool/<int:post_pool_id>")
def post_pool(post_pool_id):
  title_sql = "SELECT post_pool_title,owner FROM PostPools WHERE id = ?"
  title_query = db.query(title_sql, [post_pool_id])
  title = title_query[0][0]
  owner_id =  title_query[0][1]

  user_sql = "SELECT username FROM Users WHERE id = ?"
  user_query = db.query(user_sql, [owner_id])
  owner_name = user_query[0][0]

  posts_sql = "SELECT post_headline,id FROM Posts WHERE post_pool = ?"
  posts_query = db.query(posts_sql, [post_pool_id])
  posts = multi_list(posts_query,[0,1])

  return render_template(
      "post-pool.html", 
      owner_id=owner_id, 
      owner_name=owner_name,
      post_pool_id=post_pool_id, 
      title=title, 
      posts=posts)

@app.route("/post/<int:post_id>")
def post(post_id):
  post_sql = '''
    SELECT A.post_headline, A.poster, B.content, C.post_pool_title
    FROM Posts A
    LEFT JOIN PostContents B ON A.id = B.post
    LEFT JOIN PostPools C on C.id = A.post_pool
    WHERE A.id = ?
  '''
  post_query = db.query(post_sql, [post_id])
  post_query = post_query[0]

  return render_template("post.html", 
    headline=post_query[0], 
    poster_id=post_query[1], 
    post_id=post_id,
    title=post_query[3], 
    content=post_query[2])


