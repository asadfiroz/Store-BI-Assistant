-- Store BI Assistant — Database Setup

Create database if not exists Bi_demo;
use BI_demo;

Create Table customers (
	customer_id INT PRIMARY KEY AUTO_INCREMENT,
	name varchar(100),
	email varchar(100),
	region varchar(100),
	joined_date Date
);

CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    cost DECIMAL(10,2)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- ── Seed Data ───────────────────────────────

INSERT INTO customers (name, email, region, joined_date) VALUES
('Asad Firoz','afiroz@email.com','North','2023-01-15'),
('Nafisah Shaik','nafsaww@email.com','South','2023-02-20'),
('Daniel Charles','dcharles@email.com','East','2023-03-10'),
('David Brown','david@email.com','West','2023-04-05'),
('Eva Martinez','eva@email.com','North','2023-05-18'),
('Frank Lee','frank@email.com','South','2023-06-22'),
('Grace Kim','grace@email.com','East','2023-07-30'),
('Henry Davis','henry@email.com','West','2023-08-14'),
('Iris Wilson','iris@email.com','North','2023-09-09'),
('Jack Taylor','jack@email.com','South','2023-10-01'),
('Karen Moore','karen@email.com','East','2023-11-11'),
('Liam Jackson','liam@email.com','West','2023-12-25'),
('Mia Thomas','mia@email.com','North','2024-01-08'),
('Noah Harris','noah@email.com','South','2024-02-14'),
('Olivia Clark','olivia@email.com','East','2024-03-19'),
('Paul Lewis','paul@email.com','West','2024-04-23'),
('Quinn Walker','quinn@email.com','North','2024-05-05'),
('Rachel Hall','rachel@email.com','South','2024-06-17'),
('Sam Allen','sam@email.com','East','2024-07-29'),
('Tina Young','tina@email.com','West','2024-08-12');

INSERT INTO products (name, category, price, cost) VALUES
('Laptop Pro','Electronics',1200.00,700.00),
('Wireless Mouse','Electronics',35.00,12.00),
('Office Chair','Furniture',350.00,180.00),
('Standing Desk','Furniture',600.00,300.00),
('Python Book','Books',45.00,15.00),
('Data Science Book','Books',55.00,18.00),
('USB Hub','Electronics',28.00,9.00),
('Monitor 27in','Electronics',450.00,250.00),
('Keyboard Mechanical','Electronics',120.00,55.00),
('Webcam HD','Electronics',85.00,35.00),
('Notebook Set','Stationery',12.00,4.00),
('Pen Set','Stationery',8.00,2.00),
('Headphones','Electronics',200.00,90.00),
('Desk Lamp','Furniture',45.00,18.00),
('Cable Organizer','Stationery',15.00,5.00);

INSERT INTO orders (customer_id, order_date, status) VALUES
(1,'2024-01-10','completed'),(2,'2024-01-15','completed'),
(3,'2024-01-20','returned'),(4,'2024-02-01','completed'),
(5,'2024-02-10','completed'),(6,'2024-02-14','returned'),
(7,'2024-02-20','completed'),(8,'2024-03-05','completed'),
(9,'2024-03-12','returned'),(10,'2024-03-18','completed'),
(11,'2024-03-25','completed'),(12,'2024-04-02','completed'),
(13,'2024-04-10','returned'),(14,'2024-04-15','completed'),
(15,'2024-04-22','completed'),(16,'2024-05-01','completed'),
(17,'2024-05-08','returned'),(18,'2024-05-15','completed'),
(19,'2024-05-22','completed'),(20,'2024-06-01','completed'),
(1,'2024-06-10','completed'),(2,'2024-06-18','completed'),
(3,'2024-07-01','completed'),(4,'2024-07-09','returned'),
(5,'2024-07-15','completed'),(6,'2024-07-22','completed'),
(7,'2024-08-01','completed'),(8,'2024-08-10','completed'),
(9,'2024-08-18','returned'),(10,'2024-09-01','completed');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1,1,1,1200.00),(1,2,1,35.00),(2,8,1,450.00),
(3,3,1,350.00),(4,9,1,120.00),(4,7,2,28.00),
(5,13,1,200.00),(6,4,1,600.00),(7,5,2,45.00),
(8,10,1,85.00),(9,1,1,1200.00),(10,2,3,35.00),
(11,6,1,55.00),(12,8,1,450.00),(13,3,1,350.00),
(14,9,1,120.00),(15,13,1,200.00),(16,11,5,12.00),
(17,4,1,600.00),(18,1,1,1200.00),(19,7,2,28.00),
(20,5,1,45.00),(21,2,2,35.00),(22,10,1,85.00),
(23,6,2,55.00),(24,8,1,450.00),(25,1,1,1200.00),
(26,13,1,200.00),(27,9,1,120.00),(28,3,1,350.00),
(29,4,1,600.00),(30,2,4,35.00);
