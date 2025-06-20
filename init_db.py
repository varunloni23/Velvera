import mysql.connector
import os

def init_database():
    # Database connection parameters
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Varunloni@12'
    }
    
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Read and execute SQL script
        with open('database/velvra_db.sql', 'r') as f:
            sql_script = f.read()
        
        # Split script into individual statements
        statements = sql_script.split(';')
        
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        print("Database initialized successfully!")
        
        # Create uploads directory if it doesn't exist
        os.makedirs('app/static/images/products', exist_ok=True)
        print("Product images directory created.")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed.")

if __name__ == "__main__":
    init_database() 