from .webapp import app
import pymysql
from . import database

# Main Application entry point
# to run this app, execute cd src and python -m eCom


def main() -> None:
    print("Hello from eCom")

    if False: # you only need to run this one time on your system to create DB
        if database.createDB():
            print("Sucessfully created SQL database")

    if False: # you only need to run this one time to create table, or when we expand the inventory csv
        if database.createInventory():
            print("Successfully populated database with products")

    df = database.getDFfromSQL()
    print(df.head())

    # do something with the DataFrame object

    app.run(debug=False)


if __name__ == "__main__":
    main()