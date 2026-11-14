from flask import Flask, render_template

app = Flask (__name__)

@app.route("/")
def homepage():
    return "Hello World!!"

@app.route("/hello/<personName>")
def hello(personName):
    return f"<h1> HELLO {personName} </h1> <p> <h2> cool </h2>"

@app.route("/helloPage/<personName>")
def helloPage(personName):
    return render_template("hello.html", personNameInTemplate = personName)

app.run (debug=True)