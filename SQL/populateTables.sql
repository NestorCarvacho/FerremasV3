INSERT INTO Category (category_name, description, picture) VALUES
('Hand Tools', 'Tools used manually for various tasks', 'hand_tools.jpg'),
('Power Tools', 'Electric or battery-powered tools', 'power_tools.jpg'),
('Gardening Tools', 'Tools for gardening and landscaping', 'gardening_tools.jpg'),
('Construction Tools', 'Tools used in construction and building', 'construction_tools.jpg'),
('Measuring Tools', 'Tools for measuring dimensions and distances', 'measuring_tools.jpg'),
('Safety Equipment', 'Protective gear and safety tools', 'safety_equipment.jpg'),
('Workshop Supplies', 'General supplies for workshops', 'workshop_supplies.jpg'),
('Hardware', 'Nails, screws, and other hardware items', 'hardware.jpg');

INSERT INTO PersonalInfo (county, address, phone, email, city, postal_code) VALUES
('Los Angeles', '123 Main St', '555-1234', 'JohnDoe@api-integracion.com', 'Los Angeles', '90001'),
('San Francisco', '456 Market St', '555-5678', 'JaneSmith@api-integracion.com', 'San Francisco', '94105'),
('New York', '789 Broadway', '555-8765', 'AliceJohnson@api-integracion.com', 'New York', '10001'),
('Chicago', '101 State St', '555-4321', 'BobBrown@api-integracion.com', 'Chicago', '60601'),
('Houston', '202 Elm St', '555-6789', 'CharlieDavis@api-integracion.com', 'Houston', '77001'),
('Miami', '303 Ocean Dr', '555-9876', 'EmilyClark@api-integracion.com', 'Miami', '33101'),
('Seattle', '404 Pine St', '555-6543', 'MichaelScott@api-integracion.com', 'Seattle', '98101'),
('Boston', '505 Beacon St', '555-3210', 'PamBeesly@api-integracion.com', 'Boston', '02108'),
('Denver', '606 Colfax Ave', '555-7890', 'JimHalpert@api-integracion.com', 'Denver', '80202'),
('Atlanta', '707 Peachtree St', '555-4567', 'DwightSchrute@api-integracion.com', 'Atlanta', '30303'),
('Dallas', '808 Elm St', '555-2345', 'AngelaMartin@api-integracion.com', 'Dallas', '75201'),
('Phoenix', '909 Grand Ave', '555-6781', 'OscarMartinez@api-integracion.com', 'Phoenix', '85001'),
('San Diego', '1010 Harbor Dr', '555-8764', 'StanleyHudson@api-integracion.com', 'San Diego', '92101'),
('Portland', '1111 Burnside St', '555-5432', 'KellyKapoor@api-integracion.com', 'Portland', '97201'),
('Las Vegas', '1212 Fremont St', '555-9870', 'RyanHoward@api-integracion.com', 'Las Vegas', '89101');

insert into `User` (PersonalInfo) values
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8),
(9),
(10),
(11),
(12),
(13),
(14),
(15);

INSERT INTO Customer (user_id, last_name, contact_name) VALUES
(1, 'Doe', 'John Doe'),
(2, 'Smith', 'Jane Smith'),
(3, 'Johnson', 'Alice Johnson'),
(4, 'Brown', 'Bob Brown'),
(5, 'Davis', 'Charlie Davis');

INSERT INTO Supplier (user_id, contact_name, contact_title, address, phone) VALUES
(1, 'John Doe', 'Owner', '123 Main St', '555-1234'),
(2, 'Jane Smith', 'Manager', '456 Market St', '555-5678'),
(3, 'Alice Johnson', 'Sales Rep', '789 Broadway', '555-8765'),
(4, 'Bob Brown', 'Director', '101 State St', '555-4321'),
(5, 'Charlie Davis', 'Coordinator', '202 Elm St', '555-6789');

INSERT INTO Shipper (company_name, phone) VALUES
('Fast Shipping Co.', '555-1111'),
('Quick Delivery Inc.', '555-2222'),
('Express Transport LLC', '555-3333'),
('Speedy Logistics', '555-4444'),
('Rapid Freight Services', '555-5555');

INSERT INTO Product (product_name, supplier_id, category_id, quantity_per_unit, unit_price, units_in_order, units_in_stock, reorder_level, discount) VALUES
('Hammer', 1, 1, '1 unit', 10.99, 50, 100, 10, 0.05),
('Screwdriver', 2, 1, '1 unit', 5.49, 30, 200, 20, 0.10),
('Drill', 3, 2, '1 unit', 99.99, 15, 50, 5, 0.15),
('Lawn Mower', 4, 3, '1 unit', 299.99, 10, 20, 2, 0.20),
('Measuring Tape', 5, 5, '1 unit', 15.99, 25, 150, 15, 0.08);

INSERT INTO Cart (customer_id, product_id, num_of_products, total_price) VALUES
(1, 1, 2, 21.98),
(2, 2, 5, 27.45),
(3, 3, 1, 99.99),
(4, 4, 1, 299.99),
(5, 5, 3, 47.97);

INSERT INTO `Order` (customer_id, order_date, required_date, shipped_date, freight, shipper_id, ) VALUES
(1, '2023-10-01', '2023-10-05', NULL, 5.00, 1),
(2, '2023-10-02', '2023-10-06', NULL, 7.50, 2),
(3, '2023-10-03', '2023-10-07', NULL, 15.00, 3),
(4, '2023-10-04', '2023-10-08', NULL, 20.00, 4),
(5, '2023-10-05', '2023-10-09', NULL, 25.00, 5);

INSERT INTO OrderDetails (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 2, 10.99),
(2, 2, 5, 5.49),
(3, 3, 1, 99.99),
(4, 4, 1, 299.99),
(5, 5, 3, 15.99);

INSERT INTO Payment (order_id, payment_date, amount, payment_method) VALUES
(1, '2023-10-01', 21.98, 'Credit Card'),
(2, '2023-10-02', 27.45, 'PayPal'),
(3, '2023-10-03', 99.99, 'Bank Transfer'),
(4, '2023-10-04', 299.99, 'Credit Card'),
(5, '2023-10-05', 47.97, 'Debit Card');

INSERT INTO OrderShipper (order_id, shipper_id, tracking_number) VALUES
(1, 1, 'TRACK123'),
(2, 2, 'TRACK456'),
(3, 3, 'TRACK789'),
(4, 4, 'TRACK101'),
(5, 5, 'TRACK112');

INSERT INTO OrderStatus (order_id, status, status_date) VALUES
(1, 'Pending', '2023-10-01'),
(2, 'Shipped', '2023-10-02'),
(3, 'Delivered', '2023-10-03'),
(4, 'Cancelled', '2023-10-04'),
(5, 'Pending', '2023-10-05');

INSERT INTO `Admin` (admin_name, email, password) VALUES
('Admin1', 'admin1@api-integracion.com', 'password1'),
('Admin2', 'admin2@api-integracion.com', 'password2'),
('Admin3', 'admin3@api-integracion.com', 'password3'),
('Admin4', 'admin4api-integracion.com', 'password4'),
('Admin5', 'admin5@api-integracion.com', 'password5');