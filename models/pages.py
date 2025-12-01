from flask import Flask, render_template, request, redirect, session
import db 
from utilities import multi_list
from app1 import app

import re





@app.route("/pools")
def pools():
  post_pool_sql = '''
      SELECT A.post_pool_title, A.id, B.username, C.count
      FROM PostPools A
      LEFT JOIN Users B ON B.id = A.owner
      LEFT JOIN (SELECT post_pool, COUNT(*) AS count FROM Posts GROUP BY post_pool) C ON C.post_pool = A.id
    '''
  post_pool_query = db.query(post_pool_sql, [])

  post_pools = multi_list(post_pool_query, list(range(0,4)))

  history_update("/pools")

  return render_template("frontpage/index-pools.html", post_pools=post_pools)

@app.route("/posts")
def posts():
  posts_sql = ''' 
      SELECT A.id, A.post_headline, A.poster, B.username, D.count, E.content, F.post_pool_title
      FROM Posts A
      LEFT JOIN PostContents E ON A.id = E.post
      LEFT JOIN Users B ON A.poster = B.id
      LEFT JOIN CommentsSections C ON A.id = C.post
      LEFT JOIN (SELECT comments_section, COUNT(*) AS count FROM Messages GROUP BY comments_section) D
        ON D.comments_section = C.id
      LEFT JOIN PostPools F ON A.post_pool = F.id
    '''
  posts_query = db.query(posts_sql, [])
  posts = multi_list(posts_query, list(range(0,7)))
  history_update("/posts")
  return render_template("frontpage/index-posts.html", posts=posts)

@app.route("/users")
def users():
  users_sql = ''' 
      SELECT A.id, A.username, B.count, C.count, 0
      FROM Users A
      LEFT JOIN (SELECT owner, COUNT(*) AS count FROM PostPools GROUP BY owner) B ON B.owner = A.id
      LEFT JOIN (SELECT poster, COUNT(*) AS count FROM Posts GROUP BY poster) C ON C.poster = A.id
    '''
#     LEFT JOIN (SELECT commenter, COUNT(*) AS count FROM Messages GROUP BY commenter) D ON C.commenter = A.id
  users_query = db.query(users_sql, [])
  users = multi_list(users_query, list(range(0,5)))
  history_update("/users")
  return render_template("frontpage/index-users.html", users=users)

@app.route("/statistics")
def statistics():
# userss_sql = ''' 
#   '''
# users_query = db.query(posts_sql, [])
# users = multi_list(posts_query, list(range(0,0)))
  statistics = []
  history_update("/statistics")
  return render_template("frontpage/index-stats.html", statistics=statistics)





@app.route("/user/<int:user_id>/pools")
def user_pools(user_id):
  user_sql = "SELECT username FROM Users WHERE id = ?"
  user_query = db.query(user_sql, [user_id])[0]

  pools_sql= '''
      SELECT A.post_pool_title, A.id, B.username, C.count
      FROM PostPools A
      LEFT JOIN Users B ON B.id = A.owner
      LEFT JOIN (SELECT post_pool, COUNT(*) AS count FROM Posts GROUP BY post_pool) C ON C.post_pool = A.id
      WHERE owner = ?
    '''
  pools_query = db.query(pools_sql, [user_id])
  pools = multi_list(pools_query, list(range(0,4)))
  history_update("/user/" + str(user_id) + "/pools")
  return render_template("user/user-pools.html", user_id=user_id, username=user_query[0], post_pools=pools)

@app.route("/user/<int:user_id>/posts")
def user_posts(user_id):
  user_sql = "SELECT username FROM Users WHERE id = ?"
  user_query = db.query(user_sql, [user_id])[0]

  posts_sql= '''
      SELECT A.id, A.post_headline, A.poster, B.username, D.count, E.content, F.post_pool_title
      FROM Posts A
      LEFT JOIN PostContents E ON A.id = E.post
      LEFT JOIN Users B ON A.poster = B.id
      LEFT JOIN CommentsSections C ON A.id = C.post
      LEFT JOIN (SELECT comments_section, COUNT(*) AS count FROM Messages GROUP BY comments_section) D
        ON D.comments_section = C.id
      LEFT JOIN PostPools F ON A.post_pool = F.id
      WHERE owner = ?
    '''
  posts_query = db.query(posts_sql, [user_id])
  posts = multi_list(posts_query, list(range(0,4)))
  history_update("/user/" + str(user_id) + "/posts")
  return render_template("user/user-posts.html", user_id=user_id, username=user_query[0], posts=posts)

@app.route("/user/<int:user_id>/statistics")
def user_stats(user_id):
  user_sql = "SELECT username FROM Users WHERE id = ?"
  user_query = db.query(user_sql, [user_id])[0]

# pools_sql= '''
#     SELECT A.post_pool_title, A.id, B.username, C.count
#     FROM PostPools A
#     LEFT JOIN Users B ON B.id = A.owner
#     LEFT JOIN (SELECT post_pool, COUNT(*) AS count FROM Posts GROUP BY post_pool) C ON C.post_pool = A.id
#     WHERE owner = ?
#   '''
# pools_query = db.query(pools_sql, [user_id])
# pools = multi_list(pools_query, list(range(0,4)))
  history_update("/user/" + str(user_id) + "/statistics")
  return render_template("user/user-stats.html", user_id=user_id, username=user_query[0])





@app.route("/post_pool/<int:post_pool_id>")
def post_pool(post_pool_id):
  pool_sql = '''
      SELECT A.post_pool_title, B.id, B.username
      FROM PostPools A
      LEFT JOIN Users B ON A.owner = B.id
      WHERE A.id = ?
    '''
  pool_query = db.query(pool_sql, [post_pool_id])
  pool_info = multi_list(pool_query, list(range(0,3)))

  posts_sql = ''' 
      SELECT A.id, A.post_headline, A.poster, B.username, D.count, E.content
      FROM Posts A
      LEFT JOIN PostContents E ON A.id = E.post
      LEFT JOIN Users B ON A.poster = B.id
      LEFT JOIN CommentsSections C ON A.id = C.post
      LEFT JOIN (SELECT comments_section, COUNT(*) AS count FROM Messages GROUP BY comments_section) D
        ON D.comments_section = C.id
      WHERE A.post_pool = ?
    '''
  posts_query = db.query(posts_sql, [post_pool_id])
  posts = multi_list(posts_query, list(range(0,6)))

  history_update("/post_pool/" + str(post_pool_id))

  return render_template("pool.html", post_pool_info=pool_info[0], posts=posts)

@app.route("/post/<int:post_id>")
def post(post_id):
  post_sql = '''
    SELECT A.post_headline, A.poster, B.content, C.post_pool_title, D.username, F.count
    FROM Posts A
    LEFT JOIN PostContents B ON A.id = B.post
    LEFT JOIN PostPools C on C.id = A.post_pool
    LEFT JOIN Users D on D.id = A.poster
    LEFT JOIN CommentsSections E ON A.id = E.post
    LEFT JOIN (SELECT comments_section, COUNT(*) AS count FROM Messages GROUP BY comments_section) F
      ON F.comments_section = E.id
    WHERE A.id = ?
  '''
  post_query = db.query(post_sql, [post_id])
  post = multi_list(post_query,list(range(0,6)))

  history_update("/post/" + str(post_id))

  return render_template("post.html", post=post[0])


def history_update(new_entry):
  m = session["history"] if "history" in session else []
  l = ["/pools", "/posts", "/statistics", "/users"]

  print(m)
  if m and m[-1] == new_entry:
    pass
  elif m and re.search(r"/user/[0-9]+/", m[-1]) and re.search(r"/user/[0-9]+/", new_entry):
     m[-1] = new_entry
  elif new_entry in l:
     m = [new_entry]
  else:
     m.append(new_entry)
  session["history"] = m


@app.route("/previous", methods=["POST"])
def previous():
  p = session["history"][-2]
  session["history"] = session["history"][0:-2]
  return redirect(p)





















