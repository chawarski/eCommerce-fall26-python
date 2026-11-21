import pymysql
import pandas as pd
from sqlalchemy import create_engine

# Code block to build local DB using python

# Setup mysql(or other) server on your system using the below info.
# You can edit your own login and password, but it will be easiest to share login.
# Assume no one has important DB data on their system, but we working local anyway.

connection = pymysql.connect(host='localhost', user='root', password='chargerhorse', cursorclass=pymysql.cursors.DictCursor)
db_name = "eCom_inventory"

if True: # DB creation, can turn on/off
    try:
        with connection.cursor() as cursor:
            # Wipe database before building. Method is only safe for local, small projects like ours
            cursor.execute(f"DROP DATABASE IF EXISTS `{db_name}`;")

            # Create the database (IF NOT EXISTS prevents errors if it already exists)
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            
            # Switch the active connection to the newly created database
            cursor.execute(f"USE `{db_name}`;")
            
            # Create table
            cursor.execute("""
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
            """)
        
        connection.commit()

    except Exception as e:
        print(f"SQL Connection Error: {e}")
        connection.close()
 
if True: # product insertion can turn on/off 
    file = open(r"eCommerce-fall26-python\src\inventory\electronics_shop_inventory.csv")
    product_list = file.read().split("\n")
 
    try:
        with connection.cursor() as cursor:
            # Optional: Load raw image bytes if using MEDIUMBLOB (or pass a string path/URL if using VARCHAR)
            # with open("product_image.jpg", "rb") as img_file:
            #     image_data = img_file.read()

            sql = """
                INSERT INTO products (category, name, sku, description, image, price, quantity)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            row_data = [product.split(',') for index, product in enumerate(product_list) if index > 0]
            for row in row_data:
                product_row = (
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    None,  # Use None if we don't have an image
                    row[5],
                    row[6]
                )

                cursor.execute(sql, product_row)
                print(f"Product inserted with ID: {cursor.lastrowid}")

                # Commit the transaction so the row is saved to the database
                connection.commit()

    except pymysql.IntegrityError as e:
        # Triggers if part_number already exists (due to the UNIQUE constraint)
        print(f"Duplicate entry error: {e}")
        connection.close()
        raise SystemExit(1) from e

if connection.open:
    connection.close()

# Block to create a pandas object from the SQL DB
if True:
    # Create a SQLAlchemy engine using the mysql+pymysql dialect
    # Format: mysql+pymysql://username:password@host:port/database_name
    engine = create_engine(f"mysql+pymysql://root:chargerhorse@localhost:3306/{db_name}")

    # Read table or run a custom SQL query
    query = "SELECT id, category, name, sku, description, price, quantity FROM products"
    df = pd.read_sql(query, con=engine)

    print(df.head())