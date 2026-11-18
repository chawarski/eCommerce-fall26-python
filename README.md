# eCommerce-fall26-python
Simple eCommerce project to demonstrate python usage for DSCI 6602 fall 2026

Create a eCommerce platform that simulates the sales of ELECTRONICS: phones, accessories, computers, etc

Need to use SQL server for product warehouse simulating the product stock

Need a flask server with a local webpage to interact with SQL server for DB


## Requirements 
(**bold** for prof stated requirements)
- LANDING PAGE: links to other pages [@app.route("/")]
- **PRODUCT CATALOG PAGE**: 'customer' page with grid layout for viewing all products w/ **IMAGES, SPECS, ADD TO CART BUTTONS** [@app.route("/catalog")]
  
- **PRODUCT CRUD PAGE**: 'admin' page for **search, create, read, update, delete** products from DB, enforcing DB design. **SUPPLY SIDE WAREHOUSE COUNTS** [@app.route("/products")]
  
- **SHOPPING CART**: 'customer' page for viewing, editing shopping cart. **"BUY WITH SHOPPING CART, COUNT GOES UP/DOWN. UPDATE ON CART SHOULD UPDATE QUANTITY, NOT JUST ADD NEW LINES"** [@app.route("/cart")]
  
- **OOP IMPLEMENTATIONS: CLASSES FOR PRODUCT, CART, ETC. USE DECORATORS**
  
- (optional) CUSTOMIZE FRAMEWORK FOR OTHER PRODUCT TYPES. *Note: this should be inherent with our Product Crud page. You could remove all products and repopulate with anything.*


## DB Design
| id | category | name | part_number | description | image | price | quantity |
| -- | -- | -- | --| -- | -- | -- | -- |
| 0 | GPU | nVidia RTX 5090 | G-RTX-5090 | GeForce RTX 5090 32GB GDDR7 PCI Express 5.0 ATX Graphics Card 32GD | img | $6500 | 10 |
| 1 | phone | Apple iPhone Duo | IP-DUO-256 | iPhone Duo 256GB Night Sky | img | $1999 | 10 |
