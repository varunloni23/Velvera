from app import bcrypt
from app.database import get_db_connection, close_connection

def fix_admin_password():
    # Generate a proper bcrypt hash for 'admin123'
    hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
    
    # Connect to the database
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database")
        return
    
    cursor = conn.cursor()
    try:
        # Update the admin user's password
        query = "UPDATE users SET password = %s WHERE username = 'admin'"
        cursor.execute(query, (hashed_password,))
        conn.commit()
        print("Admin password updated successfully!")
        print("You can now login with username 'admin' and password 'admin123'")
    except Exception as e:
        print(f"Error updating admin password: {e}")
    finally:
        close_connection(conn, cursor)

if __name__ == "__main__":
    fix_admin_password() 