import pymysql
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path


# Setup mysql(or other) server on your system using the USER and PASSWORD.
# You can edit your own user and password, but it will be easiest to share login.
# Assume no one has important DB data on their system, but we working local anyway.

DB_NAME = "eCom_inventory"
USER = "root"
PASSWORD = "chargerhorse"

# Function to build local DB using python
def createDB() -> bool:
    try:
        connection = pymysql.connect(host='localhost', user=USER, password=PASSWORD, cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            # Wipe database before building. Method is only safe for local, small projects like ours
            cursor.execute(f"DROP DATABASE IF EXISTS `{DB_NAME}`;")

            # Create the database (IF NOT EXISTS prevents errors if it already exists)
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            
            # Switch the active connection to the newly created database
            cursor.execute(f"USE `{DB_NAME}`;")
            
            # Create table using SQL
            sql = """
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(50) UNIQUE,
                    category VARCHAR(50) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                    quantity INT NOT NULL DEFAULT 0,
                    sku VARCHAR(100) UNIQUE,
                    description TEXT,
                    image MEDIUMBLOB 
                );
            """
            cursor.execute(sql)
        connection.commit()

    except Exception as e:
        print(f"SQL Connection Error: {e}")
        connection.close()
        return False

    connection.close()
    return True

# Function to populate DB Table with date from a csv
# We are using a csv becasue we can create synthetic data in this format
def createInventory() -> bool:
    connection = pymysql.connect(host='localhost', user=USER, password=PASSWORD, cursorclass=pymysql.cursors.DictCursor)
    inventory_file = (Path(__file__).resolve().parent.parent/ "inventory"/ "electronics_shop_inventory.csv")
    with inventory_file.open(encoding="utf-8") as file: 
        product_list = file.read().split("\n")
 
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"USE `{DB_NAME}`;")
            # Optional: Load raw image bytes if using MEDIUMBLOB (or pass a string path/URL if using VARCHAR)
            # with open("product_image.jpg", "rb") as img_file:
            #     image_data = img_file.read()

            sql = """
                INSERT INTO products (category, name, sku, description, price, quantity, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            row_data = [tuple(product.split(',')) for index, product in enumerate(product_list) if index > 0]
            for row in row_data:
                cursor.execute(sql, row)
                print(f"Product inserted with ID: {cursor.lastrowid}")

                # Commit the transaction so the row is saved to the database
                connection.commit()

    except pymysql.IntegrityError as e:
        # Triggers if part_number already exists (due to the UNIQUE constraint)
        print(f"Duplicate entry error: {e}")
        connection.close()
        return False
    
    connection.close()
    return True

# Block to create a pandas object from the SQL DB
def getDFfromSQL() -> pd.DataFrame:
    # Create a SQLAlchemy engine using the mysql+pymysql dialect
    # Format: mysql+pymysql://username:password@host:port/database_name
    engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@localhost:3306/{DB_NAME}")

    # Read table or run a custom SQL query
    query = "SELECT id, category, name, sku, description, price, quantity FROM products"
    df = pd.read_sql(query, con=engine)

    # print(df.head())
    return df

createDB()
createInventory()