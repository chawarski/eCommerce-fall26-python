-- 1. Create the database (with UTF-8 support) and select it
CREATE DATABASE IF NOT EXISTS inventory_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE inventory_db;

-- 2. Create a parent lookup table
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create a child table with a foreign key relationship
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    category_id INT,
    unit_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    in_stock BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id) REFERENCES categories(id)
        ON DELETE SET NULL
);

-- 4. Insert initial seed data
INSERT INTO categories (name) VALUES
    ('Area Scan Cameras'),
    ('Lenses'),
    ('Lighting');

INSERT INTO products (sku, name, category_id, unit_price, in_stock) VALUES
    ('CAM-1001', 'Mono 5MP GigE Camera', 1, 649.00, TRUE),
    ('CAM-1002', 'Color 12MP USB3 Camera', 1, 899.50, TRUE),
    ('LNS-2001', '16mm C-Mount Fixed Lens', 2, 185.00, FALSE);

-- 5. Verify the setup with a JOIN query
SELECT
    p.sku,
    p.name AS product_name,
    c.name AS category,
    p.unit_price,
    p.in_stock
FROM products p
LEFT JOIN categories c ON p.category_id = c.id;