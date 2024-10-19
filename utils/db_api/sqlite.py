import sqlite3

from pydantic_core.core_schema import none_schema


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db
    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)
    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql,parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    # Create table
    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int ,
            fullname varchar(255),
            telegram_id varchar(20) UNIQUE,
            language varchar(3),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, fullname: str, telegram_id: str = None, language: str = 'uz'):

        sql = """
        INSERT INTO Users(id, fullname,telegram_id, language) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, fullname, telegram_id, language), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)
    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)
    def update_user_fullname(self, telegram_id):

        sql = f"""
        UPDATE Users SET fullname=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(telegram_id, id), commit=True)
    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def create_table_products(self):
        sql = """
        CREATE TABLE Products (
            id int,
            name varchar(255),
            description text,
            price int,
            qty int,
            category varchar(180),
            discount int,
            image varchar(255),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    def add_product(self, id:int, name:str = None, description:str = None, price: int = None, qty: int= None,category:int = None,discount:int = None, image:str = None):
        sql = """INSERT INTO Products (id, name, description, price, qty, category, discount, image) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                 """

        self.execute(sql, parameters=(id, name, description, price, qty, category, discount, image), commit=True)


    def select_all_products(self):
        sql = """
        SELECT * FROM Products
        """
        return self.execute(sql, fetchall=True)

    def select_product(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Products where id=1 AND Name='John'"
        sql = "SELECT * FROM Products WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)


    def get_product_id(self, category: str):
        sql = "SELECT * FROM Products WHERE category = ?"
        return self.execute(sql, (category, ), fetchall=True)

    # Create Categories table
    def create_table_categories(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender INTEGER NOT NULL
        );
        """
        self.execute(sql, commit=True)

    def add_category(self, id: int, name: str, gender: bool):
        sql = """
        INSERT INTO Categories(id, name, gender) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, gender), commit=True)

    def select_all_categories(self):
        sql = """
        SELECT * FROM Categories
        """
        return self.execute(sql, fetchall=True)

    def select_category(self, **kwargs):
        sql = """
        SELECT * FROM Categories WHERE
        """
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def get_category_gender(self, gender:bool):
        sql = "SELECT * FROM Categories WHERE gender = ?"
        return self.execute(sql, (gender,), fetchall=True)



        # self.execute(sql, parameters=(id, name, description, price, qty, category_id, image_path), commit=True)

    def get_product_details(self, product_id):
        sql = """
        SELECT id, name, description, price, qty, category, image
        FROM Products 
        WHERE id = ?
        """
        return self.execute(sql, (product_id,), fetchone=True)

    def create_table_orders(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            user_id INTEGER,
            quantity INTEGER,
            total_price INTEGER,
            FOREIGN KEY (product_id) REFERENCES Products (id),
            FOREIGN KEY (user_id) REFERENCES Users (id)
        );
        """
        self.execute(sql, commit=True)

    def save_order(self, user_id: int, product_id: int, quantity: int, total_price: int):
        # Here, implement the logic to save the order to your database
        sql = """
        INSERT INTO Orders (user_id, product_id, quantity, total_price)
        VALUES (?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, product_id, quantity, total_price),commit=True)

    def get_user_orders(self, user_id):
        sql = "SELECT product_id, quantity, total_price FROM orders WHERE user_id = ?"
        return self.execute(sql, (user_id,), fetchall=True)


    def add_to_cart(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Basket (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            user_id INTEGER,
            quantity INTEGER,
            total_price INTEGER,
            FOREIGN KEY (product_id) REFERENCES Products (id),
            FOREIGN KEY (user_id) REFERENCES Users (id)
        );
        """
        self.execute(sql, commit=True)

    def save_cart(self, user_id: int, product_id: int, quantity: int, total_price: int):
        # Here, implement the logic to save the order to your database
        sql = """
        INSERT INTO Basket (user_id, product_id, quantity, total_price)
        VALUES (?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, product_id, quantity, total_price),commit=True)

    def users_cart(self, user_id):
        sql = """
            SELECT * FROM Basket WHERE user_id = ?
        """
        return self.execute(sql, (user_id,), fetchall=True)

    def get_basket_items(self, user_id):
        sql = """
        SELECT * FROM Basket WHERE user_id = ?
        """
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    def update_basket_item(self, user_id, product_id, new_quantity):
        product_price = self.get_product_price(product_id)
        if product_price is None:
            print(f"Error: Product ID {product_id} not found in the database.")
            raise ValueError(f"Product with ID {product_id} not found.")
        total_price = new_quantity * product_price
        sql = """
        UPDATE Basket 
        SET quantity = ?, total_price = ? 
        WHERE user_id = ? AND product_id = ?
        """
        self.execute(sql, parameters=(new_quantity, total_price, user_id, product_id))

    def add_to_basket(self, user_id, product_id, quantity):
        product_price = self.get_product_price(product_id)
        if product_price is None:
            print(f"Error: Product ID {product_id} not found in the database.")
            raise ValueError(f"Product with ID {product_id} not found.")
        total_price = quantity * product_price
        sql = """
        INSERT INTO Basket (user_id, product_id, quantity, total_price) 
        VALUES (?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, product_id, quantity, total_price), commit=True)

    def get_product_price(self, product_id: int):
        sql = "SELECT price FROM Products WHERE id = ?"
        result = self.execute(sql, (product_id,), fetchone=True)
        if result:
            return result[0]  # Return the price from the result tuple
        return None  # Return None if the product was not found

    def get_basket_items_with_details(self, user_id):
        sql = """
        SELECT b.id, b.product_id, p.name, b.quantity, b.total_price 
        FROM Basket b
        JOIN Products p ON b.product_id = p.id
        WHERE b.user_id = ?
        """
        return self.execute(sql, (user_id,), fetchall=True)


    def add_to_like(self):
        sql = """
    CREATE TABLE IF NOT EXISTS Like (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES Products (id),
        FOREIGN KEY (user_id) REFERENCES Users (id)
        );
        """
        self.execute(sql, commit=True)







