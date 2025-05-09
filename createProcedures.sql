-- product
DROP PROCEDURE IF EXISTS sp_get_products;
DROP PROCEDURE IF EXISTS sp_get_product;
DROP PROCEDURE IF EXISTS sp_add_product;
DROP PROCEDURE IF EXISTS sp_update_product;
DROP PROCEDURE IF EXISTS sp_delete_product;
-- customer
DROP PROCEDURE IF EXISTS sp_get_customers;
DROP PROCEDURE IF EXISTS sp_get_customer;
DROP PROCEDURE IF EXISTS sp_add_customer;
DROP PROCEDURE IF EXISTS sp_update_customer;
DROP PROCEDURE IF EXISTS sp_delete_customer;
-- category
DROP PROCEDURE IF EXISTS sp_get_categories;
DROP PROCEDURE IF EXISTS sp_get_category;
DROP PROCEDURE IF EXISTS sp_add_category;
DROP PROCEDURE IF EXISTS sp_update_category;
DROP PROCEDURE IF EXISTS sp_delete_category;
-- Order
DROP PROCEDURE IF EXISTS sp_get_Orders;
DROP PROCEDURE IF EXISTS sp_get_Order;
DROP PROCEDURE IF EXISTS sp_add_Order;
DROP PROCEDURE IF EXISTS sp_update_Order;
DROP PROCEDURE IF EXISTS sp_delete_Order;
-- OrderDetails
DROP PROCEDURE IF EXISTS sp_get_OrderDetails;
DROP PROCEDURE IF EXISTS sp_get_OrderDetail;
DROP PROCEDURE IF EXISTS sp_add_OrderDetail;
DROP PROCEDURE IF EXISTS sp_update_OrderDetail;
DROP PROCEDURE IF EXISTS sp_delete_OrderDetail;
-- cart
DROP PROCEDURE IF EXISTS sp_get_carts;
DROP PROCEDURE IF EXISTS sp_get_cart;
DROP PROCEDURE IF EXISTS sp_add_cart;
DROP PROCEDURE IF EXISTS sp_update_cart;
DROP PROCEDURE IF EXISTS sp_delete_cart;
-- admin
DROP PROCEDURE IF EXISTS sp_get_admins;
DROP PROCEDURE IF EXISTS sp_get_admin;
DROP PROCEDURE IF EXISTS sp_add_admin;
DROP PROCEDURE IF EXISTS sp_update_admin;
DROP PROCEDURE IF EXISTS sp_delete_admin;
-- billinginfo
DROP PROCEDURE IF EXISTS sp_get_billinginfos;
DROP PROCEDURE IF EXISTS sp_get_billinginfo;
DROP PROCEDURE IF EXISTS sp_add_billinginfo;
DROP PROCEDURE IF EXISTS sp_update_billinginfo;
DROP PROCEDURE IF EXISTS sp_delete_billinginfo;
-- PersonalInfo
DROP PROCEDURE IF EXISTS sp_get_PersonalInfos;
DROP PROCEDURE IF EXISTS sp_get_PersonalInfo;
DROP PROCEDURE IF EXISTS sp_add_PersonalInfo;
DROP PROCEDURE IF EXISTS sp_update_PersonalInfo;
DROP PROCEDURE IF EXISTS sp_delete_PersonalInfo;
-- user
DROP PROCEDURE IF EXISTS sp_get_users;
DROP PROCEDURE IF EXISTS sp_get_user;
DROP PROCEDURE IF EXISTS sp_add_user;
DROP PROCEDURE IF EXISTS sp_update_user;
DROP PROCEDURE IF EXISTS sp_delete_user;
-- shipper
DROP PROCEDURE IF EXISTS sp_get_shippers;
DROP PROCEDURE IF EXISTS sp_get_shipper;
DROP PROCEDURE IF EXISTS sp_add_shipper;
DROP PROCEDURE IF EXISTS sp_update_shipper;
DROP PROCEDURE IF EXISTS sp_delete_shipper;
-- ==== PRODUCT ====
DELIMITER //
CREATE PROCEDURE sp_get_products()
BEGIN
    SELECT * FROM Product;
END //

CREATE PROCEDURE sp_get_product(IN pid INT)
BEGIN
    SELECT * FROM Product WHERE product_id = pid;
END //

CREATE PROCEDURE sp_add_product(
    IN pname VARCHAR(100),
    IN psupplier_id INT,
    IN pcategory_id INT,
    IN pquantity_per_unit VARCHAR(100),
    IN punit_price DECIMAL(10,2),
    IN punits_in_order INT,
    IN punits_in_stock INT,
    IN preorder_level INT,
    IN pdiscount DECIMAL(5,2)
)
BEGIN
    INSERT INTO Product (
        product_name, supplier_id, category_id, quantity_per_unit, unit_price,
        units_in_order, units_in_stock, reorder_level, discount
    ) VALUES (
        pname, psupplier_id, pcategory_id, pquantity_per_unit, punit_price,
        punits_in_order, punits_in_stock, preorder_level, pdiscount
    );
END //

CREATE PROCEDURE sp_update_product(
    IN pid INT,
    IN pname VARCHAR(100),
    IN psupplier_id INT,
    IN pcategory_id INT,
    IN pquantity_per_unit VARCHAR(100),
    IN punit_price DECIMAL(10,2),
    IN punits_in_order INT,
    IN punits_in_stock INT,
    IN preorder_level INT,
    IN pdiscount DECIMAL(5,2)
)
BEGIN
    UPDATE Product SET
        product_name = pname,
        supplier_id = psupplier_id,
        category_id = pcategory_id,
        quantity_per_unit = pquantity_per_unit,
        unit_price = punit_price,
        units_in_order = punits_in_order,
        units_in_stock = punits_in_stock,
        reorder_level = preorder_level,
        discount = pdiscount
    WHERE product_id = pid;
END //

CREATE PROCEDURE sp_delete_product(IN pid INT)
BEGIN
    DELETE FROM Product WHERE product_id = pid;
END //

-- ==== CUSTOMER ====
CREATE PROCEDURE sp_get_customers()
BEGIN
    SELECT * FROM Customer;
END //

CREATE PROCEDURE sp_get_customer(IN cid INT)
BEGIN
    SELECT * FROM Customer WHERE id = cid;
END //

CREATE PROCEDURE sp_add_customer(IN user_id INT, IN last_name VARCHAR(100), IN contact_name VARCHAR(100))
BEGIN
    INSERT INTO Customer(user_id, last_name, contact_name) VALUES (user_id, last_name, contact_name);
END //

CREATE PROCEDURE sp_update_customer(IN cid INT, IN last_name VARCHAR(100), IN contact_name VARCHAR(100))
BEGIN
    UPDATE Customer SET last_name = last_name, contact_name = contact_name WHERE id = cid;
END //

CREATE PROCEDURE sp_delete_customer(IN cid INT)
BEGIN
    DELETE FROM Customer WHERE id = cid;
END //

-- ==== CATEGORY ====
CREATE PROCEDURE sp_get_categories()
BEGIN
    SELECT * FROM Category;
END //

CREATE PROCEDURE sp_get_category(IN caid INT)
BEGIN
    SELECT * FROM Category WHERE category_id = caid;
END //

CREATE PROCEDURE sp_add_category(IN name VARCHAR(100), IN description TEXT)
BEGIN
    INSERT INTO Category(category_name, description) VALUES (name, description);
END //

CREATE PROCEDURE sp_update_category(
    IN categoryId INT,
    IN categoryName VARCHAR(100),
    IN descriptionCategory TEXT
)
BEGIN
    UPDATE category SET
        category_name = categoryName,
        category.description = descriptionCategory
    WHERE category_id = categoryId;
END //

CREATE PROCEDURE sp_delete_category(IN categoryId INT)
BEGIN
    DELETE FROM category WHERE category_id = categoryId;
END //
-- ==== ORDERS ====
CREATE PROCEDURE sp_get_Orders()
BEGIN
    SELECT * FROM integracionEcomerce.ORDER;
END //

CREATE PROCEDURE sp_get_Order(IN oid INT)
BEGIN
    SELECT * FROM integracionecomerce.order WHERE order_id = oid;
END //

CREATE PROCEDURE sp_add_order(
    IN customer_id INT,
    IN order_date DATETIME,
    IN required_date DATETIME,
    IN shipped_date DATETIME,
    IN freight DECIMAL(10,2),
    IN shipper_id INT
)
BEGIN
    INSERT INTO integracionecomerce.ORDER (
        customer_id, order_date, required_date, shipped_date, freight, shipper_id
    ) VALUES (
    customer_id, order_date, required_date, shipped_date, freight, shipper_id
    );
END //

CREATE PROCEDURE sp_update_order(
    IN oid INT,
    IN customerId INT,
    IN orderDate DATETIME,
    IN requiredDate DATETIME,
    IN shippedDate DATETIME,
    IN freightDec DECIMAL(10,2),
    IN shipperId INT
)
BEGIN
    UPDATE integracionecomerce.Order SET
        customer_id = customerId,
        order_date = orderDate,
        required_date = requiredDate,
        shipped_date = shippedDate,
        freight = freightDec,
        shipper_id = shipperId
    WHERE order_id = oid;
END //

CREATE PROCEDURE sp_delete_order(IN oid INT)
BEGIN
    DELETE FROM integracionecomerce.order WHERE order_id = oid;
END //

-- ==== OrderDetails ====
CREATE PROCEDURE sp_get_OrderDetails()
BEGIN
    SELECT * FROM OrderDetails;
END //

CREATE PROCEDURE sp_get_OrderDetail(IN odid INT)
BEGIN
    SELECT * FROM OrderDetails WHERE id = odid;
END //

CREATE PROCEDURE sp_add_OrderDetail(
    IN orderId INT,
    IN productId INT,
    IN unitPrice DECIMAL(10,2),
    IN qty INT,
    IN disc DECIMAL(5,2)
)
BEGIN
    INSERT INTO OrderDetail(
        order_id, product_id, unit_price, quantity, discount
    ) VALUES (
    orderId, productId, unitPrice, qty, disc
    );
END //

CREATE PROCEDURE sp_update_OrderDetail(
    IN odid INT,
    IN orderId INT,
    IN productId INT,
    IN unitPrice DECIMAL(10,2),
    IN qty INT,
    IN disc DECIMAL(5,2)
)
BEGIN
    UPDATE OrderDetails SET
        order_id = orderId,
        product_id = productId,
        unit_price = unitPrice,
        quantity = qty,
        discount = disc
    WHERE id = odid;
END //

CREATE PROCEDURE sp_delete_orderDetail(IN odid INT)
BEGIN
    DELETE FROM OrderDetails WHERE id = odid;
END //

-- ==== CART ====
CREATE PROCEDURE sp_get_Carts()
BEGIN
    SELECT * FROM cart;
END //

CREATE PROCEDURE sp_get_Cart(IN cid INT)
BEGIN
    SELECT * FROM cart WHERE id = cid;
END //

CREATE PROCEDURE sp_add_Cart(
    IN customerId INT,
    IN productId INT,
    IN numOfProducts DECIMAL(10,2),
    IN totalPrice INT
)
BEGIN
    INSERT INTO Cart (
        customer_id, product_id, num_of_products, total_price
    ) VALUES (
        customerId, productId, numOfProducts, totalPrice
    );
END //

CREATE PROCEDURE sp_update_cart(
    IN cid INT,
    IN customerId INT,
    IN productId INT,
    IN numOfProducts DECIMAL(10,2),
    IN totalPrice INT
)
BEGIN
    UPDATE OrderDetails SET
        customer_id = cid,
        product_id = customerId,
        num_of_products= productId,
        total_price = totalPrice
    WHERE id = cid;
END //

CREATE PROCEDURE sp_delete_cart(IN odid INT)
BEGIN
    DELETE FROM cart WHERE id = cid;
END //

-- ==== ADMIN ====
CREATE PROCEDURE sp_get_admins()
BEGIN
    SELECT * FROM integracionecomerce.admin;
END //

CREATE PROCEDURE sp_get_admin(IN aid INT)
BEGIN
    SELECT * FROM integracionecomerce.admin WHERE admin_id = aid;
END //

CREATE PROCEDURE sp_add_Admin(
    IN adminName varchar(100),
    IN adminPassword varchar(100)
)
BEGIN
    INSERT INTO integracionecomerce.admin (
        admin_name, admin_password
    ) VALUES (
        adminName, adminPassword
    );
END //

CREATE PROCEDURE sp_update_admin(
    IN aid INT,
    IN adminName varchar(100),
    IN adminPassword varchar(100)
)
BEGIN
    UPDATE integracionecomerce.admin SET
        admin_name = adminName,
        admin_password = adminPassword
    WHERE id = aid;
END //

CREATE PROCEDURE sp_delete_admin(IN aid INT)
BEGIN
    DELETE FROM integracionecomerce.admin WHERE id = aid;
END //

-- ==== BILLINGINFO ====
CREATE PROCEDURE sp_get_billinginfos()
BEGIN
    SELECT * FROM billinginfo;
END //

CREATE PROCEDURE sp_get_billinginfo(IN bid INT)
BEGIN
    SELECT * FROM billinginfo WHERE billing_id = bid;
END //

CREATE PROCEDURE sp_add_billinginfo(
    IN customerId INT,
    IN billingAddress varchar(255),
    IN creditCardNumber varchar(16),
    IN creditCardPin varchar(4),
    IN creditCardExpDate date,
    IN billDate date
)
BEGIN
    INSERT INTO billinginfo (
        customer_id, billing_address, credit_card_number, credit_card_pin, credit_card_exp_date, bill_date
    ) VALUES (
        customerId, billingAddress, creditCardNumber, creditCardPin, creditCardExpDate, billDate
    );
END //

CREATE PROCEDURE sp_update_billinginfo(
    IN bid INT,
    IN customerId INT,
    IN billingAddress varchar(255),
    IN creditCardNumber varchar(16),
    IN creditCardPin varchar(4),
    IN creditCardExpDate date,
    IN billDate date
)
BEGIN
    UPDATE billinginfo SET
        customer_id = customerId,
        billing_address =billingAddress,
        credit_card_number =creditCardNumber,
        credit_card_pin = creditCardPin,
        credit_card_exp_date = creditCardExpDate,
        bill_date = billDate
    WHERE billing_id = bid;
END //

CREATE PROCEDURE sp_delete_billinginfo(IN bid INT)
BEGIN
    DELETE FROM billinginfo WHERE billing_id = bid;
END //

-- ==== PERSONALINFO ====
CREATE PROCEDURE sp_get_PersonalInfos()
BEGIN
    SELECT * FROM PersonalInfo;
END //

CREATE PROCEDURE sp_get_PersonalInfo(IN pid INT)
BEGIN
    SELECT * FROM PersonalInfo WHERE personal_id = pid;
END //

CREATE PROCEDURE sp_add_PersonalInfo(
    IN PiCountry varchar(100),
    IN PiAdress varchar(255),
    IN PiPhone varchar(15),
    IN PiEmail varchar(254),
    IN PiCity varchar(100),
    IN PiPostalCode varchar(20)
)
BEGIN
    INSERT INTO PersonalInfo (
        country, address, phone, email, city, postal_code
    ) VALUES (
        PiCountry, PiAdress, PiPhone, PiEmail, PiCity, PiPostalCode
    );
END //

CREATE PROCEDURE sp_update_PersonalInfo(
    IN Pid INT,
    IN PiCountry INT,
    IN PiAdress varchar(255),
    IN PiPhone varchar(16),
    IN PiEmail varchar(4),
    IN PiCity date,
    IN PiPostalCode date
)
BEGIN
    UPDATE PersonalInfo SET
        country = PiCountry,
        address = PiAdress,
        phone = PiPhone,
        email = PiEmail,
        city = PiCity,
        postal_code = PiPostalCode
    WHERE personal_id = Pid;
END //

CREATE PROCEDURE sp_delete_PersonalInfo(IN pid INT)
BEGIN
    DELETE FROM PersonalInfo WHERE personal_id = Pid;
END //

-- ==== USER ====
CREATE PROCEDURE sp_get_users()
BEGIN
    SELECT * FROM integracionecomerce.user;
END //

CREATE PROCEDURE sp_get_user(IN uid INT)
BEGIN
    SELECT * FROM integracionecomerce.user WHERE id = uid;
END //

CREATE PROCEDURE sp_add_user(
    IN personalInfoId INT
)
BEGIN
    INSERT INTO integracionecomerce.user (
        personal_info_id
    ) VALUES (
        personalInfoId
    );
END //

CREATE PROCEDURE sp_update_user(
    IN uid INT,
    IN personalInfoId INT
)
BEGIN
    UPDATE integracionecomerce.user SET
        personal_info_id = personalInfoId
    WHERE id = uid;
END //

CREATE PROCEDURE sp_delete_user(IN uid INT)
BEGIN
    DELETE FROM integracionecomerce.user WHERE id = uid;
END //

-- ==== SHIPPER ====
CREATE PROCEDURE sp_get_shippers()
BEGIN
    SELECT * FROM shipper;
END //

CREATE PROCEDURE sp_get_shipper(IN sid INT)
BEGIN
    SELECT * FROM shipper WHERE shipper_id = sid;
END //

CREATE PROCEDURE sp_add_shipper(
    IN companyName varchar(100),
    IN phoneShip varchar(15)
)
BEGIN
    INSERT INTO shipper (
        company_name, phone
    ) VALUES (
        companyName, phoneShip
    );
END //

CREATE PROCEDURE sp_update_shipper(
    IN sid INT,
    IN companyName varchar(100),
    IN phoneShip varchar(15)
)
BEGIN
    UPDATE shipper SET
        company_name = companyName,
        phone = phoneShip
    WHERE shipper_id = sid;
END //

CREATE PROCEDURE sp_delete_shipper(IN sid INT)
BEGIN
    DELETE FROM shipper WHERE shipper_id = sid;
END //

DELIMITER ;