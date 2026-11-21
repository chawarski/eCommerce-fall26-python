from flask import Flask, render_template, request
import pandas as pd
from sqlalchemy import create_engine

DB_NAME = "eCom_inventory"
USER = "root"
PASSWORD = "chargerhorse"

app = Flask (__name__)
# Create a SQLAlchemy engine using the mysql+pymysql dialect
# Format: mysql+pymysql://username:password@host:port/database_name
engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@localhost:3306/{DB_NAME}")

@app.route("/")
def index():
    category = request.args.get("category")
    if category:
        query = "SELECT id, category, name, sku, description, image, price, quantity FROM products WHERE category = %(cat)s"
        df = pd.read_sql(query, con=engine, params={"cat": category})
    else:
        query = "SELECT id, category, name, sku, description, image, price, quantity FROM products"
        df = pd.read_sql(query, con=engine)

    products = df.to_dict(orient="records")
    return render_template("index.html", products=products)



# @app.route("/")
# def homepage():
#     return "Hello World!!"

# @app.route("/hello/<personName>")
# def hello(personName):
#     return f"<h1> HELLO {personName} </h1> <p> <h2> cool </h2>"

# @app.route("/helloPage/<personName>")
# def helloPage(personName):
#     return render_template("hello.html", personNameInTemplate = personName)

# app.run (debug=True)