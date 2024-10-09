import sqlite3

# Function to create tables for the e-commerce platform
def create_tables():
    conn = sqlite3.connect('ecommerce_platform.db')
    cursor = conn.cursor()

    # Create Customer table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customer (
        CustomerID VARCHAR(5) PRIMARY KEY,
        CustomerName VARCHAR(100) NOT NULL,
        Email VARCHAR(100) NOT NULL UNIQUE,
        Password VARCHAR(100) NOT NULL,
        Role VARCHAR(20) NOT NULL CHECK (Role IN ('customer', 'admin'))
    );
    ''')

    # Create ProductCategories table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ProductCategories (
        CategoryID VARCHAR(5) PRIMARY KEY,
        CategoryName VARCHAR(100) NOT NULL
    );
    ''')

    # Create Products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        ProductID VARCHAR(5) PRIMARY KEY,
        ProductName VARCHAR(100) NOT NULL,
        Description TEXT,
        Price DECIMAL(10, 2) NOT NULL CHECK (Price >= 0),
        CategoryID VARCHAR(5),
        FOREIGN KEY (CategoryID) REFERENCES ProductCategories(CategoryID)
    );
    ''')

    # Create Orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        OrderID VARCHAR(5) PRIMARY KEY,
        CustomerID VARCHAR(5),
        OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
        TotalAmount DECIMAL(10, 2) NOT NULL CHECK (TotalAmount >= 0),
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
    );
    ''')

    # Create OrderDetails table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS OrderDetails (
        OrderID VARCHAR(5),
        ProductID VARCHAR(5),
        Quantity INT NOT NULL CHECK (Quantity > 0),
        UnitPrice DECIMAL(10, 2) NOT NULL CHECK (UnitPrice >= 0),
        PRIMARY KEY (OrderID, ProductID),
        FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
    );
    ''')

    conn.commit()
    conn.close()
    print("E-commerce tables created successfully!")

# Function to create indexes
def create_indexes():
    conn = sqlite3.connect('ecommerce_platform.db')
    cursor = conn.cursor()

    # Create an index on CustomerID in the Orders table
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_customer_orders ON Orders(CustomerID);')
    
    # Create an index on ProductID in the OrderDetails table
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_product_orderdetails ON OrderDetails(ProductID);')

    conn.commit()
    conn.close()
    print("Indexes created successfully!")

# Function to create views
def create_views():
    conn = sqlite3.connect('ecommerce_platform.db')
    cursor = conn.cursor()

    # Create a view for order summary with customer details
    cursor.execute('''
    CREATE VIEW IF NOT EXISTS v_OrderSummary AS
    SELECT 
        o.OrderID, 
        c.CustomerName, 
        o.OrderDate, 
        o.TotalAmount
    FROM 
        Orders o
    JOIN 
        Customer c ON o.CustomerID = c.CustomerID;
    ''')

    # Create a view for product sales summary
    cursor.execute('''
    CREATE VIEW IF NOT EXISTS v_ProductSalesSummary AS
    SELECT 
        p.ProductName, 
        SUM(od.Quantity) AS TotalQuantitySold, 
        SUM(od.Quantity * od.UnitPrice) AS TotalRevenue
    FROM 
        Products p
    JOIN 
        OrderDetails od ON p.ProductID = od.ProductID
    GROUP BY 
        p.ProductName;
    ''')

    conn.commit()
    conn.close()
    print("Views created successfully!")

# Function to insert a customer
def insert_customer(customer_id, customer_name, email, password, role):
    conn = sqlite3.connect('ecommerce_platform.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Customer (CustomerID, CustomerName, Email, Password, Role) VALUES (?, ?, ?, ?, ?);",
                   (customer_id, customer_name, email, password, role))
    conn.commit()
    conn.close()
    print(f"Customer {customer_name} inserted successfully.")

# Function to insert a product category
def insert_product_category(category_id, category_name):
    conn = sqlite3.connect('ecommerce_platform.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ProductCategories (CategoryID, CategoryName) VALUES (?, ?);", 
                   (category_id, category_name))
    conn.commit()
    conn.close()
    print(f"Product category {category_name} inserted successfully.")

# Function to insert a product
def insert_product(product_id, product_name, description, price, category_id):
    conn = sqlite3.connect('ecommerce_platform.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Products (ProductID, ProductName, Description, Price, CategoryID) VALUES (?, ?, ?, ?, ?);",
                   (product_id, product_name, description, price, category_id))
    conn.commit()
    conn.close()
    print(f"Product {product_name} inserted successfully.")

# Function to place an order
def place_order(order_id, customer_id, total_amount):
    conn = sqlite3.connect('ecommerce_platform.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Orders (OrderID, CustomerID, TotalAmount) VALUES (?, ?, ?);",
                   (order_id, customer_id, total_amount))
    conn.commit()
    conn.close()
    print(f"Order {order_id} placed successfully.")

# Function to add details to an order
def add_order_detail(order_id, product_id, quantity, unit_price):
    conn = sqlite3.connect('ecommerce_platform.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO OrderDetails (OrderID, ProductID, Quantity, UnitPrice) VALUES (?, ?, ?, ?);",
                   (order_id, product_id, quantity, unit_price))
    conn.commit()
    conn.close()
    print(f"Added product {product_id} to order {order_id}.")

# Function to display all customers
def display_all_customers():
    conn = sqlite3.connect('ecommerce_platform.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer;")
    results = cursor.fetchall()
    conn.close()
    print("\nCurrent Customers:")
    for customer in results:
        print(f"Customer ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Role: {customer[4]}")

# Function to display all products
def display_all_products():
    conn = sqlite3.connect('ecommerce_platform.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products;")
    results = cursor.fetchall()
    conn.close()
    print("\nCurrent Products:")
    for product in results:
        print(f"Product ID: {product[0]}, Name: {product[1]}, Price: {product[3]:.2f}, Category ID: {product[4]}")

# Function to display all orders
def display_all_orders():
    conn = sqlite3.connect('ecommerce_platform.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Orders;")
    results = cursor.fetchall()
    conn.close()
    print("\nCurrent Orders:")
    for order in results:
        print(f"Order ID: {order[0]}, Customer ID: {order[1]}, Order Date: {order[2]}, Total Amount: {order[3]:.2f}")

# Function to display total quantity sold
def display_total_quantity_sold():
    conn = sqlite3.connect('ecommerce_platform.db')
    cursor = conn.cursor()
    
    # Query the view to get the total quantity sold for all products
    cursor.execute("SELECT SUM(TotalQuantitySold) FROM v_ProductSalesSummary;")
    total_quantity_sold = cursor.fetchone()[0]
    
    if total_quantity_sold is None:
        total_quantity_sold = 0

    conn.close()
    
    print(f"\nTotal Quantity Sold for all products: {total_quantity_sold}")

# Function to display total revenue
def display_total_revenue():
    conn = sqlite3.connect('ecommerce_platform.db')
    cursor = conn.cursor()
    
    # Query the view to get the total revenue for all products
    cursor.execute("SELECT SUM(TotalRevenue) FROM v_ProductSalesSummary;")
    total_revenue = cursor.fetchone()[0]
    
    if total_revenue is None:
        total_revenue = 0.0

    conn.close()
    
    print(f"\nTotal Revenue from all product sales: ${total_revenue:.2f}")

# Function to display the menu
def display_menu():
    print("\nMenu:")
    print("1. View All Customers")
    print("2. View All Products")
    print("3. View All Orders")
    print("4. Insert Customer")
    print("5. Insert Product Category")
    print("6. Insert Product")
    print("7. Place Order")
    print("8. Add Order Detail")
    print("9. View Total Revenue")
    print("10. View Total Quantity Sold")  # Add this new option
    print("11. Exit")

# Main function to run the program
def main():
    create_tables()  # Create tables if they don't exist
    create_indexes()  # Create indexes for performance optimization
    create_views()  # Create views for simplified data access

    while True:
        display_menu()
        choice = input("Enter your choice (1-11): ")

        if choice == '1':
            display_all_customers()

        elif choice == '2':
            display_all_products()

        elif choice == '3':
            display_all_orders()

        elif choice == '4':
            customer_id = input("Enter Customer ID (e.g., C001): ")
            customer_name = input("Enter Customer Name: ")
            email = input("Enter Email: ")
            password = input("Enter Password: ")
            role = input("Enter Role (customer/admin): ")
            insert_customer(customer_id, customer_name, email, password, role)

        elif choice == '5':
            category_id = input("Enter Category ID (e.g., CAT01): ")
            category_name = input("Enter Category Name: ")
            insert_product_category(category_id, category_name)

        elif choice == '6':
            product_id = input("Enter Product ID (e.g., P001): ")
            product_name = input("Enter Product Name: ")
            description = input("Enter Product Description: ")
            price = float(input("Enter Price: "))
            category_id = input("Enter Category ID (e.g., CAT01): ")
            insert_product(product_id, product_name, description, price, category_id)

        elif choice == '7':
            order_id = input("Enter Order ID (e.g., O001): ")
            customer_id = input("Enter Customer ID (e.g., C001): ")
            total_amount = float(input("Enter Total Amount: "))
            place_order(order_id, customer_id, total_amount)

        elif choice == '8':
            order_id = input("Enter Order ID (e.g., O001): ")
            product_id = input("Enter Product ID (e.g., P001): ")
            quantity = int(input("Enter Quantity: "))
            unit_price = float(input("Enter Unit Price: "))
            add_order_detail(order_id, product_id, quantity, unit_price)

        elif choice == '9':
            display_total_revenue()  # Call the function to show total revenue

        elif choice == '10':
            display_total_quantity_sold()  # Call the new function to show total quantity sold

        elif choice == '11':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
