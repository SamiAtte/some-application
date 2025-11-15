from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
  return "hello world"



@app.route("/page/<int:page_id>")
def page(page_id : int):
  return "page " + str(page_id)
  
