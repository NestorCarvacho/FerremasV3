USE integracionEcomerce;

CREATE TABLE PersonalInfo (
    personal_id INT AUTO_INCREMENT PRIMARY KEY,
    county VARCHAR(100),
    address VARCHAR(255),
    phone VARCHAR(15),
    email VARCHAR(254),
    city VARCHAR(100),
    postal_code VARCHAR(20)
);

CREATE TABLE `User` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    personal_info_id INT UNIQUE,
    FOREIGN KEY (personal_info_id) REFERENCES PersonalInfo(personal_id) ON DELETE CASCADE
);

CREATE TABLE Customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    last_name VARCHAR(100),
    contact_name VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES `User`(id) ON DELETE CASCADE
);

CREATE TABLE Supplier (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    contact_name VARCHAR(100),
    contact_title VARCHAR(100),
    address VARCHAR(255),
    phone VARCHAR(15),
    FOREIGN KEY (user_id) REFERENCES `User`(id) ON DELETE CASCADE
);

CREATE TABLE Category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100),
    description TEXT,
    picture VARCHAR(255)  -- Para almacenar rutas de imagen si no usas blobs
);

CREATE TABLE Product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    supplier_id INT,
    category_id INT,
    quantity_per_unit VARCHAR(100),
    unit_price DECIMAL(10,2),
    units_in_order INT,
    units_in_stock INT,
    reorder_level INT,
    discount DECIMAL(5,2),
    picture VARCHAR(255), -- Ruta de imagen opcional
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Category(category_id) ON DELETE CASCADE
);

CREATE TABLE Cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    num_of_products INT,
    total_price DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES Customer(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
);

CREATE TABLE Shipper (
    shipper_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100),
    phone VARCHAR(15)
);

CREATE TABLE `Order` (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    order_date DATETIME,
    required_date DATETIME,
    shipped_date DATETIME NULL,
    freight DECIMAL(10,2),
    shipper_id INT,
    FOREIGN KEY (customer_id) REFERENCES Customer(id) ON DELETE CASCADE,
    FOREIGN KEY (shipper_id) REFERENCES Shipper(shipper_id) ON DELETE CASCADE
);

CREATE TABLE OrderDetails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    unit_price DECIMAL(10,2),
    quantity INT,
    discount DECIMAL(5,2),
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
);

CREATE TABLE Admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    admin_name VARCHAR(100),
    admin_password VARCHAR(100)
);

CREATE TABLE BillingInfo (
    billing_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT UNIQUE,
    billing_address VARCHAR(255),
    credit_card_number VARCHAR(16),
    credit_card_pin VARCHAR(4),
    credit_card_exp_date DATE,
    bill_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customer(id) ON DELETE CASCADE
);

create table Payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    payment_date DATETIME,
    amount DECIMAL(10,2),
    payment_method VARCHAR(50),
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id) ON DELETE CASCADE
);

create table OrderShipper (
    order_id INT,
    shipper_id INT,
    tracking_number VARCHAR(50),
    PRIMARY KEY (order_id, shipper_id),
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id) ON DELETE CASCADE,
    FOREIGN KEY (shipper_id) REFERENCES Shipper(shipper_id) ON DELETE CASCADE
);

create table OrderStatus (
    order_id INT,
    status VARCHAR(50),
    status_date DATETIME,
    PRIMARY KEY (order_id, status),
    FOREIGN KEY (order_id) REFERENCES `Order`(order_id) ON DELETE CASCADE
);