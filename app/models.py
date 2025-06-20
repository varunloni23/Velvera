from app.database import get_db_connection, close_connection
from app import bcrypt
from mysql.connector import Error

class User:
    @staticmethod
    def create(username, email, password, first_name, last_name, address=None, phone=None, is_admin=False):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        
        cursor = conn.cursor()
        try:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            query = """
                INSERT INTO users (username, email, password, first_name, last_name, address, phone, is_admin)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (username, email, hashed_password, first_name, last_name, address, phone, is_admin)
            cursor.execute(query, values)
            conn.commit()
            return True, cursor.lastrowid
        except Error as e:
            return False, str(e)
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            return user
        except Error:
            return None
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            return user
        except Error:
            return None
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            return user
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        return bcrypt.check_password_hash(stored_password, provided_password)


class Product:
    @staticmethod
    def get_all(limit=None, category_id=None):
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT p.*, c.name as category_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
            """
            
            if category_id:
                query += " WHERE p.category_id = %s"
                if limit:
                    query += " LIMIT %s"
                    cursor.execute(query, (category_id, limit))
                else:
                    cursor.execute(query, (category_id,))
            else:
                if limit:
                    query += " LIMIT %s"
                    cursor.execute(query, (limit,))
                else:
                    cursor.execute(query)
                    
            products = cursor.fetchall()
            return products
        except Error:
            return []
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def get_by_id(product_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT p.*, c.name as category_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                WHERE p.product_id = %s
            """
            cursor.execute(query, (product_id,))
            product = cursor.fetchone()
            return product
        except Error:
            return None
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def create(name, description, price, stock, image_url, category_id):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (name, description, price, stock, image_url, category_id)
            cursor.execute(query, values)
            conn.commit()
            return True, cursor.lastrowid
        except Error as e:
            return False, str(e)
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def update(product_id, name, description, price, stock, image_url, category_id):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        
        cursor = conn.cursor()
        try:
            query = """
                UPDATE products
                SET name = %s, description = %s, price = %s, stock = %s, 
                    image_url = %s, category_id = %s
                WHERE product_id = %s
            """
            values = (name, description, price, stock, image_url, category_id, product_id)
            cursor.execute(query, values)
            conn.commit()
            return True, "Product updated successfully"
        except Error as e:
            return False, str(e)
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def delete(product_id):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        
        cursor = conn.cursor()
        try:
            query = "DELETE FROM products WHERE product_id = %s"
            cursor.execute(query, (product_id,))
            conn.commit()
            return True, "Product deleted successfully"
        except Error as e:
            return False, str(e)
        finally:
            close_connection(conn, cursor)


class Category:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM categories"
            cursor.execute(query)
            categories = cursor.fetchall()
            return categories
        except Error:
            return []
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def get_by_id(category_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM categories WHERE category_id = %s"
            cursor.execute(query, (category_id,))
            category = cursor.fetchone()
            return category
        except Error:
            return None
        finally:
            close_connection(conn, cursor)


class Cart:
    @staticmethod
    def add_item(user_id, product_id, quantity=1):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        
        cursor = conn.cursor()
        try:
            # Check if item already exists in cart
            check_query = "SELECT * FROM cart WHERE user_id = %s AND product_id = %s"
            cursor.execute(check_query, (user_id, product_id))
            existing_item = cursor.fetchone()
            
            if existing_item:
                # Update quantity
                update_query = "UPDATE cart SET quantity = quantity + %s WHERE user_id = %s AND product_id = %s"
                cursor.execute(update_query, (quantity, user_id, product_id))
            else:
                # Insert new item
                insert_query = "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (user_id, product_id, quantity))
            
            conn.commit()
            return True, "Item added to cart"
        except Error as e:
            return False, str(e)
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def get_user_cart(user_id):
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT c.cart_id, c.quantity, p.product_id, p.name, p.price, p.image_url,
                       (p.price * c.quantity) as subtotal
                FROM cart c
                JOIN products p ON c.product_id = p.product_id
                WHERE c.user_id = %s
            """
            cursor.execute(query, (user_id,))
            cart_items = cursor.fetchall()
            return cart_items
        except Error:
            return []
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def update_quantity(cart_id, quantity):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        
        cursor = conn.cursor()
        try:
            query = "UPDATE cart SET quantity = %s WHERE cart_id = %s"
            cursor.execute(query, (quantity, cart_id))
            conn.commit()
            return True, "Cart updated successfully"
        except Error as e:
            return False, str(e)
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def remove_item(cart_id):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        
        cursor = conn.cursor()
        try:
            query = "DELETE FROM cart WHERE cart_id = %s"
            cursor.execute(query, (cart_id,))
            conn.commit()
            return True, "Item removed from cart"
        except Error as e:
            return False, str(e)
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def clear_cart(user_id):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        
        cursor = conn.cursor()
        try:
            query = "DELETE FROM cart WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            conn.commit()
            return True, "Cart cleared successfully"
        except Error as e:
            return False, str(e)
        finally:
            close_connection(conn, cursor)


class Order:
    @staticmethod
    def create(user_id, total_amount, shipping_address, payment_method):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        
        cursor = conn.cursor()
        try:
            # Create order
            order_query = """
                INSERT INTO orders (user_id, total_amount, shipping_address, payment_method)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(order_query, (user_id, total_amount, shipping_address, payment_method))
            order_id = cursor.lastrowid
            
            # Get cart items
            cursor.execute("""
                SELECT c.product_id, c.quantity, p.price
                FROM cart c
                JOIN products p ON c.product_id = p.product_id
                WHERE c.user_id = %s
            """, (user_id,))
            cart_items = cursor.fetchall()
            
            # Add order items
            for item in cart_items:
                product_id, quantity, price = item
                cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (%s, %s, %s, %s)
                """, (order_id, product_id, quantity, price))
                
                # Update product stock
                cursor.execute("""
                    UPDATE products
                    SET stock = stock - %s
                    WHERE product_id = %s
                """, (quantity, product_id))
            
            # Clear cart
            cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
            
            conn.commit()
            return True, order_id
        except Error as e:
            conn.rollback()
            return False, str(e)
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def get_user_orders(user_id):
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM orders WHERE user_id = %s ORDER BY order_date DESC"
            cursor.execute(query, (user_id,))
            orders = cursor.fetchall()
            return orders
        except Error:
            return []
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def get_order_details(order_id):
        conn = get_db_connection()
        if not conn:
            return None, []
        
        cursor = conn.cursor(dictionary=True)
        try:
            # Get order
            order_query = "SELECT * FROM orders WHERE order_id = %s"
            cursor.execute(order_query, (order_id,))
            order = cursor.fetchone()
            
            if not order:
                return None, []
            
            # Get order items
            items_query = """
                SELECT oi.*, p.name, p.image_url
                FROM order_items oi
                JOIN products p ON oi.product_id = p.product_id
                WHERE oi.order_id = %s
            """
            cursor.execute(items_query, (order_id,))
            items = cursor.fetchall()
            
            return order, items
        except Error:
            return None, []
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def update_status(order_id, status):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        
        cursor = conn.cursor()
        try:
            query = "UPDATE orders SET status = %s WHERE order_id = %s"
            cursor.execute(query, (status, order_id))
            conn.commit()
            return True, "Order status updated successfully"
        except Error as e:
            return False, str(e)
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def update_payment_status(order_id, payment_status):
        conn = get_db_connection()
        if not conn:
            return False, "Database connection error"
        
        cursor = conn.cursor()
        try:
            query = "UPDATE orders SET payment_status = %s WHERE order_id = %s"
            cursor.execute(query, (payment_status, order_id))
            conn.commit()
            return True, "Payment status updated successfully"
        except Error as e:
            return False, str(e)
        finally:
            close_connection(conn, cursor)
    
    @staticmethod
    def get_all_orders(limit=None):
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT o.*, u.username, u.email
                FROM orders o
                JOIN users u ON o.user_id = u.user_id
                ORDER BY o.order_date DESC
            """
            
            if limit:
                query += " LIMIT %s"
                cursor.execute(query, (limit,))
            else:
                cursor.execute(query)
                
            orders = cursor.fetchall()
            return orders
        except Error:
            return []
        finally:
            close_connection(conn, cursor) 