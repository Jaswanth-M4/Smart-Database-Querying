import sqlite3

# Connect to SQLite
connection = sqlite3.connect("classicmodels.db")
cursor = connection.cursor()

# Create tables
cursor.executescript("""
DROP TABLE IF EXISTS productlines;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS offices;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS orderdetails;

CREATE TABLE productlines (
  productLine TEXT PRIMARY KEY,
  textDescription TEXT
);

CREATE TABLE products (
  productCode TEXT PRIMARY KEY,
  productName TEXT NOT NULL,
  productLine TEXT NOT NULL,
  productScale TEXT NOT NULL,
  productVendor TEXT NOT NULL,
  productDescription TEXT NOT NULL,
  quantityInStock INTEGER NOT NULL,
  buyPrice REAL NOT NULL,
  MSRP REAL NOT NULL,
  FOREIGN KEY (productLine) REFERENCES productlines(productLine)
);

CREATE TABLE offices (
  officeCode TEXT PRIMARY KEY,
  city TEXT NOT NULL,
  phone TEXT NOT NULL,
  addressLine1 TEXT NOT NULL,
  addressLine2 TEXT,
  state TEXT,
  country TEXT NOT NULL,
  postalCode TEXT NOT NULL
);

CREATE TABLE employees (
  employeeNumber INTEGER PRIMARY KEY,
  lastName TEXT NOT NULL,
  firstName TEXT NOT NULL,
  extension TEXT NOT NULL,
  email TEXT NOT NULL,
  officeCode TEXT NOT NULL,
  reportsTo INTEGER,
  jobTitle TEXT NOT NULL,
  FOREIGN KEY (officeCode) REFERENCES offices(officeCode)
);

CREATE TABLE customers (
  customerNumber INTEGER PRIMARY KEY,
  customerName TEXT NOT NULL,
  contactLastName TEXT NOT NULL,
  contactFirstName TEXT NOT NULL,
  phone TEXT NOT NULL,
  addressLine1 TEXT NOT NULL,
  addressLine2 TEXT,
  city TEXT NOT NULL,
  state TEXT,
  postalCode TEXT,
  country TEXT NOT NULL,
  salesRepEmployeeNumber INTEGER,
  creditLimit REAL,
  FOREIGN KEY (salesRepEmployeeNumber) REFERENCES employees(employeeNumber)
);

CREATE TABLE payments (
  customerNumber INTEGER,
  checkNumber TEXT,
  paymentDate TEXT,
  amount REAL NOT NULL,
  PRIMARY KEY (customerNumber, checkNumber),
  FOREIGN KEY (customerNumber) REFERENCES customers(customerNumber)
);

CREATE TABLE orders (
  orderNumber INTEGER PRIMARY KEY,
  orderDate TEXT NOT NULL,
  requiredDate TEXT NOT NULL,
  shippedDate TEXT,
  status TEXT NOT NULL,
  comments TEXT,
  customerNumber INTEGER NOT NULL,
  FOREIGN KEY (customerNumber) REFERENCES customers(customerNumber)
);

CREATE TABLE orderdetails (
  orderNumber INTEGER,
  productCode TEXT,
  quantityOrdered INTEGER NOT NULL,
  priceEach REAL NOT NULL,
  orderLineNumber INTEGER NOT NULL,
  PRIMARY KEY (orderNumber, productCode),
  FOREIGN KEY (orderNumber) REFERENCES orders(orderNumber),
  FOREIGN KEY (productCode) REFERENCES products(productCode)
);
""")

# Insert sample records into productlines
productlines_data = [
    ("Classic Cars", "Attention to detail and precision manufacturing define our classic car models."),
    ("Motorcycles", "Our motorcycles line features models from the 50s and 60s."),
    ("Planes", "All model planes are incredibly detailed and historically accurate."),
    ("Ships", "Ships include both sail and motor vessels from various time periods."),
    ("Trains", "Highly detailed trains and accessories from the golden age of rail."),
    ("Trucks and Buses", "Rugged and durable, our trucks and buses are popular with collectors."),
    ("Vintage Cars", "Vintage car models include some of the earliest vehicles ever made.")
]

cursor.executemany('''
    INSERT INTO productlines (productLine, textDescription)
    VALUES (?, ?)
''', productlines_data)


print("Inserted records into productlines successfully!")


# Insert data into OFFICES table
offices_data = [
    (1, "San Francisco", "100 Market Street", "Suite 300", "CA", "USA", "94080", "650-219-4782"),
    (2, "Boston", "1550 Court Place", "Suite 102", "MA", "USA", "02107", "215-837-0825"),
    (3, "NYC", "523 East 53rd Street", "apt. 5A", "NY", "USA", "10022", "212-555-3000"),
    (4, "Paris", "43 Rue Jouffroy D'abbans", "", "", "France", "75017", "33-1-14-47-61-3000"),
    (5, "Tokyo", "4-1 Kioicho", "", "Chiyoda-Ku", "Japan", "102-8578", "81-33-258-2943"),
    (6, "Sydney", "5-11 Wentworth Avenue", "Floor #2", "NSW", "Australia", "2010", "61-2-9264-2451"),
    (7, "London", "25 Old Broad Street", "Level 7", "", "UK", "EC2N 1HN", "44-20-7877-2041")
]

cursor.executemany("""
    INSERT INTO offices (officeCode, city, addressLine1, addressLine2, state, country, postalCode, phone)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", offices_data)

# Insert data into EMPLOYEES table
employees_data = [
    (1002, "Murphy", "Diane", "x5800", "dmurphy@classicmodelcars.com", 1, "President", None),
    (1056, "Patterson", "Mary", "x4611", "mpatterso@classicmodelcars.com", 1, "VP Sales", 1002),
    (1076, "Firrelli", "Jeff", "x9273", "jfirrelli@classicmodelcars.com", 1, "VP Marketing", 1002),
    (1088, "Patterson", "William", "x4871", "wpatterson@classicmodelcars.com", 6, "Sales Manager (APAC)", 1056),
    (1102, "Bondur", "Gerard", "x5408", "gbondur@classicmodelcars.com", 4, "Sale Manager (EMEA)", 1056),
    (1143, "Bow", "Anthony", "x5428", "abow@classicmodelcars.com", 1, "Sales Manager (NA)", 1056),
    (1165, "Jennings", "Leslie", "x3291", "ljennings@classicmodelcars.com", 1, "Sales Rep", 1143),
    (1166, "Thompson", "Leslie", "x4065", "lthompson@classicmodelcars.com", 1, "Sales Rep", 1143),
    (1188, "Firrelli", "Julie", "x2173", "jfirrelli@classicmodelcars.com", 2, "Sales Rep", 1143),
    (1216, "Patterson", "Steve", "x4334", "spatterson@classicmodelcars.com", 2, "Sales Rep", 1143),
    (1286, "Tseng", "Foon Yue", "x2248", "ftseng@classicmodelcars.com", 3, "Sales Rep", 1143),
    (1323, "Vanauf", "George", "x4102", "gvanauf@classicmodelcars.com", 3, "Sales Rep", 1143),
    (1337, "Bondur", "Loui", "x6493", "lbondur@classicmodelcars.com", 4, "Sales Rep", 1102),
    (1370, "Hernandez", "Gerard", "x2028", "ghernande@classicmodelcars.com", 4, "Sales Rep", 1102),
    (1401, "Castillo", "Pamela", "x2759", "pcastillo@classicmodelcars.com", 4, "Sales Rep", 1102),
    (1501, "Bott", "Larry", "x2311", "lbott@classicmodelcars.com", 7, "Sales Rep", 1102),
    (1504, "Jones", "Barry", "x102", "bjones@classicmodelcars.com", 7, "Sales Rep", 1102),
    (1611, "Fixter", "Andy", "x101", "afixter@classicmodelcars.com", 6, "Sales Rep", 1088),
    (1612, "Marsh", "Peter", "x102", "pmarsh@classicmodelcars.com", 6, "Sales Rep", 1088),
    (1619, "King", "Tom", "x103", "tking@classicmodelcars.com", 6, "Sales Rep", 1088),
    (1621, "Nishi", "Mami", "x101", "mnishi@classicmodelcars.com", 5, "Sales Rep", 1056),
    (1625, "Kato", "Yoshimi", "x102", "ykato@classicmodelcars.com", 5, "Sales Rep", 1056),
    (1702, "Gerard", "Martin", "x2312", "mgerard@classicmodelcars.com", 4, "Sales Rep", 1102)
]

cursor.executemany("""
    INSERT INTO employees (employeeNumber, lastName, firstName, extension, email, officeCode, jobTitle, reportsTo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", employees_data)

customers_data = [
    (103, "Atelier graphique", "Schmitt", "Carine", "40.32.2555", "54, rue Royale", None, "Nantes", None, "44000", "France", 1370, 21000.00),
    (112, "Signal Gift Stores", "King", "Jean", "7025551838", "8489 Strong St.", None, "Las Vegas", "NV", "83030", "USA", 1166, 71800.00),
    (114, "Australian Collectors, Co.", "Ferguson", "Peter", "03 9520 4555", "636 St Kilda Road", "Level 3", "Melbourne", "Victoria", "3004", "Australia", 1611, 117300.00),
    (119, "La Rochelle Gifts", "Labrune", "Janine", "40.67.8555", "67, rue des Cinquante Otages", None, "Nantes", None, "44000", "France", 1370, 118200.00),
    (121, "Baane Mini Imports", "Bergulfsen", "Jonas", "07-98 9555", "Erling Skakkes gate 78", None, "Stavern", None, "4110", "Norway", 1504, 81700.00),
    (124, "Mini Gifts Distributors Ltd.", "Nelson", "Susan", "4155551450", "5677 Strong St.", None, "San Rafael", "CA", "97562", "USA", 1165, 210500.00),
    (125, "Havel & Zbyszek Co", "Piestrzeniewicz", "Zbyszek", "(26) 642-7555", "ul. Filtrowa 68", None, "Warszawa", None, "01-012", "Poland", 1401, 0.00),
    (128, "Blauer See Auto, Co.", "Keitel", "Roland", "0695-34 6555", "Lyonerstr. 34", None, "Frankfurt", None, "60528", "Germany", 1501, 59700.00),
    (129, "Mini Wheels Co.", "Murphy", "Julie", "6505555787", "5557 North Pendale Street", None, "San Francisco", "CA", "94217", "USA", 1165, 64600.00),
    (131, "Land of Toys Inc.", "Lee", "Kwai", "2125557818", "897 Long Airport Avenue", None, "NYC", "NY", "10022", "USA", 1323, 114900.00)
]

cursor.executemany("""
    INSERT INTO customers (
        customerNumber, customerName, contactLastName, contactFirstName,
        phone, addressLine1, addressLine2, city, state, postalCode,
        country, salesRepEmployeeNumber, creditLimit
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", customers_data)

payments_data = [
    (103, "HQ336336", "2004-10-19", 6066.78),
    (103, "JM555205", "2003-06-05", 14571.44),
    (112, "BO864823", "2004-10-28", 5435.26),
    (112, "GG31455", "2004-11-17", 5745.88),
    (112, "GK294751", "2004-12-15", 9841.33),
    (112, "HQ336338", "2005-01-19", 19564.58),
    (114, "BO864824", "2003-06-20", 45864.03),
    (114, "GG31456", "2004-01-20", 12319.73),
    (119, "GG31457", "2003-04-25", 2680.35),
    (119, "GK294752", "2004-07-16", 2425.94),
    (121, "GK294753", "2004-10-01", 2222.22),
    (124, "BO864825", "2003-10-28", 14191.12),
    (124, "GG31458", "2004-11-01", 1565.58),
    (125, "GG31459", "2003-05-20", 6815.12),
    (128, "HQ336339", "2004-07-09", 5977.19),
    (129, "GK294754", "2004-06-10", 2314.28),
    (129, "JM555206", "2004-12-10", 8588.80),
    (131, "BO864826", "2004-10-10", 6400.00),
    (131, "GG31460", "2005-01-01", 3300.00)
]

cursor.executemany("""
    INSERT INTO payments (
        customerNumber, checkNumber, paymentDate, amount
    )
    VALUES (?, ?, ?, ?)
""", payments_data)

orders_data = [
    (10100, "2003-01-06", "2003-01-13", "2003-01-10", "Shipped", None, 363),
    (10101, "2003-01-09", "2003-01-18", "2003-01-11", "Shipped", None, 128),
    (10102, "2003-01-10", "2003-01-18", "2003-01-14", "Shipped", None, 181),
    (10103, "2003-01-29", "2003-02-07", "2003-02-02", "Shipped", None, 121),
    (10104, "2003-01-31", "2003-02-09", "2003-02-01", "Shipped", None, 141),
    (10105, "2003-02-11", "2003-02-18", "2003-02-14", "Shipped", None, 145),
    (10106, "2003-02-17", "2003-02-24", "2003-02-21", "Shipped", None, 278),
    (10107, "2003-02-24", "2003-03-03", "2003-02-26", "Shipped", None, 141),
    (10108, "2003-03-03", "2003-03-10", "2003-03-08", "Shipped", None, 385),
    (10109, "2003-03-10", "2003-03-19", "2003-03-11", "Shipped", None, 486),
    (10110, "2003-03-18", "2003-03-24", "2003-03-20", "Shipped", None, 181),
    (10111, "2003-03-25", "2003-03-31", "2003-03-28", "Shipped", None, 129),
    (10112, "2003-03-24", "2003-03-31", "2003-03-29", "Shipped", None, 369),
    (10113, "2003-03-26", "2003-04-02", "2003-03-30", "Shipped", None, 282),
    (10114, "2003-04-01", "2003-04-07", "2003-04-02", "Shipped", None, 350),
    (10115, "2003-04-04", "2003-04-11", "2003-04-06", "Shipped", None, 129),
    (10116, "2003-04-08", "2003-04-15", "2003-04-13", "Shipped", None, 205),
    (10117, "2003-04-10", "2003-04-17", "2003-04-14", "Shipped", None, 321),
    (10118, "2003-04-11", "2003-04-18", "2003-04-15", "Shipped", None, 363),
    (10119, "2003-04-14", "2003-04-21", "2003-04-20", "Shipped", None, 141)
]

cursor.executemany("""
    INSERT INTO orders (
        orderNumber, orderDate, requiredDate, shippedDate, 
        status, comments, customerNumber
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", orders_data)

orderdetails_data = [
    (10100, 'S18_1749', 30, 136.00, 3),
    (10100, 'S18_2248', 50, 55.09, 2),
    (10100, 'S18_4409', 22, 75.46, 4),
    (10100, 'S24_3969', 49, 35.29, 1),
    (10101, 'S18_2325', 25, 108.06, 4),
    (10101, 'S18_2795', 26, 167.06, 1),
    (10101, 'S24_1937', 45, 32.53, 3),
    (10101, 'S24_2022', 46, 44.35, 2),
    (10102, 'S18_1342', 39, 95.55, 2),
    (10102, 'S18_1367', 41, 58.33, 1),
    (10102, 'S24_2840', 45, 28.71, 3),
    (10102, 'S24_3420', 49, 50.10, 4),
    (10103, 'S18_2957', 36, 53.53, 1),
    (10103, 'S24_1785', 43, 103.64, 2),
    (10104, 'S18_3136', 26, 81.35, 2),
    (10104, 'S18_3320', 45, 86.13, 1),
    (10105, 'S24_1937', 38, 30.26, 1),
    (10105, 'S24_2022', 43, 44.35, 2),
    (10106, 'S18_3140', 46, 93.07, 3),
    (10106, 'S18_3259', 22, 65.77, 1),
    (10106, 'S18_4522', 49, 83.79, 2),
    (10107, 'S24_2840', 45, 28.71, 1),
    (10107, 'S24_3420', 49, 50.10, 2),
    (10108, 'S10_1678', 20, 100.00, 1),
    (10109, 'S10_1949', 30, 100.00, 1)
]

cursor.executemany("""
    INSERT INTO orderdetails (
        orderNumber, productCode, quantityOrdered, 
        priceEach, orderLineNumber
    )
    VALUES (?, ?, ?, ?, ?)
""", orderdetails_data)

products_data = [
    ("S10_1678", "1969 Harley Davidson Ultimate Chopper", "Motorcycles", "1:10", "Min Lin Diecast", "This replica features working kickstand, front suspension...", 7933, 48.81, 95.70),
    ("S10_1949", "1952 Alpine Renault 1300", "Classic Cars", "1:10", "Classic Metal Creations", "Turnable front wheels; steering function; detailed engine...", 7305, 98.58, 214.30),
    ("S10_2016", "1996 Moto Guzzi 1100i", "Motorcycles", "1:10", "Highway 66 Mini Classics", "Official Moto Guzzi logos and insignias...", 6625, 68.99, 118.94),
    ("S10_4698", "2003 Harley-Davidson Eagle Drag Bike", "Motorcycles", "1:10", "Red Start Diecast", "Model features official logos and realistic exhaust pipes...", 5582, 91.02, 193.66)
]

cursor.executemany('''
    INSERT INTO products (
        productCode, productName, productLine, productScale, productVendor,
        productDescription, quantityInStock, buyPrice, MSRP
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', products_data)

print("Inserted records into products successfully!")


# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in the database:")
for table in tables:
    print(" -", table[0])

# Display content of each table
for table in tables:
    print(f"\nContents of table: {table[0]}")
    cursor.execute(f"SELECT * FROM {table[0]}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# Commit and close
connection.commit()
connection.close()

print("Database structure for classicmodels created successfully.")
