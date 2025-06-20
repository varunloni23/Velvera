import mysql.connector
from app.database import get_db_connection, close_connection

# Sample products data
sample_products = [
    # Men's products
    {
        'name': 'Classic Fit Dress Shirt',
        'description': 'Elegant dress shirt made from premium cotton with a classic fit design. Perfect for formal occasions.',
        'price': 59.99,
        'stock': 50,
        'image_url': '/static/images/products/mens_dress_shirt.jpg',
        'category_id': 1  # Men
    },
    {
        'name': 'Slim Fit Chino Pants',
        'description': 'Comfortable and stylish chino pants with a slim fit design. Made from high-quality cotton blend.',
        'price': 79.99,
        'stock': 40,
        'image_url': '/static/images/products/mens_chino.jpg',
        'category_id': 1  # Men
    },
    {
        'name': 'Premium Wool Blazer',
        'description': 'Sophisticated wool blazer with a modern cut. Perfect for business meetings or special events.',
        'price': 199.99,
        'stock': 25,
        'image_url': '/static/images/products/mens_blazer.jpg',
        'category_id': 1  # Men
    },
    {
        'name': 'Luxury Leather Belt',
        'description': 'Handcrafted leather belt with a premium buckle. A timeless accessory for any outfit.',
        'price': 89.99,
        'stock': 60,
        'image_url': '/static/images/products/mens_belt.jpg',
        'category_id': 1  # Men
    },
    {
        'name': 'Cashmere Sweater',
        'description': 'Ultra-soft cashmere sweater that provides exceptional warmth and comfort during colder months.',
        'price': 149.99,
        'stock': 30,
        'image_url': '/static/images/products/mens_sweater.jpg',
        'category_id': 1  # Men
    },
    {
        'name': 'Tailored Suit',
        'description': 'Exquisitely tailored suit made from premium Italian fabric. Includes jacket and pants.',
        'price': 499.99,
        'stock': 15,
        'image_url': '/static/images/products/mens_suit.jpg',
        'category_id': 1  # Men
    },
    {
        'name': 'Silk Tie Collection',
        'description': 'Set of three luxury silk ties in complementary colors. Perfect for any formal occasion.',
        'price': 119.99,
        'stock': 45,
        'image_url': '/static/images/products/mens_ties.jpg',
        'category_id': 1  # Men
    },
    {
        'name': 'Premium Denim Jeans',
        'description': 'Stylish and durable jeans made from premium denim with perfect fit and comfort.',
        'price': 129.99,
        'stock': 55,
        'image_url': '/static/images/products/mens_jeans.jpg',
        'category_id': 1  # Men
    },
    {
        'name': 'Merino Wool Socks Set',
        'description': 'Set of five pairs of luxurious merino wool socks. Comfortable for all-day wear.',
        'price': 49.99,
        'stock': 70,
        'image_url': '/static/images/products/mens_socks.jpg',
        'category_id': 1  # Men
    },
    {
        'name': 'Premium Leather Wallet',
        'description': 'Handcrafted leather wallet with multiple card slots and a coin pocket. A perfect everyday accessory.',
        'price': 79.99,
        'stock': 65,
        'image_url': '/static/images/products/mens_wallet.jpg',
        'category_id': 1  # Men
    },
    
    # Women's products
    {
        'name': 'Silk Blouse',
        'description': 'Elegant silk blouse with a flattering cut. Perfect for both office wear and special occasions.',
        'price': 89.99,
        'stock': 45,
        'image_url': '/static/images/products/womens_blouse.jpg',
        'category_id': 2  # Women
    },
    {
        'name': 'Designer Pencil Skirt',
        'description': 'Sophisticated pencil skirt made from premium fabric with a comfortable stretch.',
        'price': 119.99,
        'stock': 35,
        'image_url': '/static/images/products/womens_skirt.jpg',
        'category_id': 2  # Women
    },
    {
        'name': 'Cashmere Cardigan',
        'description': 'Luxuriously soft cashmere cardigan that provides warmth without bulk. Available in multiple colors.',
        'price': 159.99,
        'stock': 30,
        'image_url': '/static/images/products/womens_cardigan.jpg',
        'category_id': 2  # Women
    },
    {
        'name': 'Designer Handbag',
        'description': 'Elegant leather handbag with gold-tone hardware. Spacious interior with multiple compartments.',
        'price': 249.99,
        'stock': 20,
        'image_url': '/static/images/products/womens_handbag.jpg',
        'category_id': 2  # Women
    },
    {
        'name': 'Tailored Blazer',
        'description': 'Sophisticated blazer with a tailored fit. Perfect for professional settings or elegant evenings out.',
        'price': 179.99,
        'stock': 25,
        'image_url': '/static/images/products/womens_blazer.jpg',
        'category_id': 2  # Women
    },
    {
        'name': 'Silk Scarf',
        'description': 'Luxurious silk scarf with an artistic print. A versatile accessory for any outfit.',
        'price': 69.99,
        'stock': 50,
        'image_url': '/static/images/products/womens_scarf.jpg',
        'category_id': 2  # Women
    },
    {
        'name': 'Designer Dress',
        'description': 'Elegant designer dress made from premium fabric. Perfect for special occasions.',
        'price': 299.99,
        'stock': 15,
        'image_url': '/static/images/products/womens_dress.jpg',
        'category_id': 2  # Women
    },
    {
        'name': 'Premium Leather Boots',
        'description': 'Stylish leather boots with a comfortable heel. Perfect for fall and winter seasons.',
        'price': 219.99,
        'stock': 30,
        'image_url': '/static/images/products/womens_boots.jpg',
        'category_id': 2  # Women
    },
    {
        'name': 'Designer Sunglasses',
        'description': 'Elegant designer sunglasses with UV protection. A perfect blend of style and functionality.',
        'price': 159.99,
        'stock': 40,
        'image_url': '/static/images/products/womens_sunglasses.jpg',
        'category_id': 2  # Women
    },
    {
        'name': 'Pearl Necklace',
        'description': 'Classic pearl necklace with sterling silver clasp. A timeless piece for any jewelry collection.',
        'price': 199.99,
        'stock': 25,
        'image_url': '/static/images/products/womens_necklace.jpg',
        'category_id': 2  # Women
    },
    
    # Kids' products - Let's add a Kids category first
    {
        'name': 'Cotton T-Shirt Set',
        'description': 'Set of three comfortable cotton t-shirts in different colors. Perfect for everyday wear.',
        'price': 39.99,
        'stock': 60,
        'image_url': '/static/images/products/kids_tshirt.jpg',
        'category_id': 5  # Kids (we'll create this category)
    },
    {
        'name': 'Denim Jeans',
        'description': 'Durable denim jeans with adjustable waist. Perfect for active kids.',
        'price': 49.99,
        'stock': 55,
        'image_url': '/static/images/products/kids_jeans.jpg',
        'category_id': 5  # Kids
    },
    {
        'name': 'Winter Jacket',
        'description': 'Warm and water-resistant winter jacket with hood. Keeps children cozy in cold weather.',
        'price': 89.99,
        'stock': 40,
        'image_url': '/static/images/products/kids_jacket.jpg',
        'category_id': 5  # Kids
    },
    {
        'name': 'School Backpack',
        'description': 'Durable and spacious backpack with multiple compartments. Perfect for school or day trips.',
        'price': 59.99,
        'stock': 50,
        'image_url': '/static/images/products/kids_backpack.jpg',
        'category_id': 5  # Kids
    },
    {
        'name': 'Sneakers',
        'description': 'Comfortable and stylish sneakers with good support. Perfect for active play.',
        'price': 69.99,
        'stock': 45,
        'image_url': '/static/images/products/kids_sneakers.jpg',
        'category_id': 5  # Kids
    },
    {
        'name': 'Pajama Set',
        'description': 'Soft and cozy pajama set with fun prints. Made from 100% cotton for comfortable sleep.',
        'price': 44.99,
        'stock': 65,
        'image_url': '/static/images/products/kids_pajama.jpg',
        'category_id': 5  # Kids
    },
    {
        'name': 'Summer Dress',
        'description': 'Lightweight cotton dress with floral print. Perfect for warm summer days.',
        'price': 54.99,
        'stock': 35,
        'image_url': '/static/images/products/kids_dress.jpg',
        'category_id': 5  # Kids
    },
    {
        'name': 'Rain Boots',
        'description': 'Waterproof rain boots with fun designs. Keeps little feet dry during rainy days.',
        'price': 39.99,
        'stock': 50,
        'image_url': '/static/images/products/kids_rainboots.jpg',
        'category_id': 5  # Kids
    },
    {
        'name': 'Winter Hat and Gloves Set',
        'description': 'Warm knitted hat and gloves set. Perfect for cold winter days.',
        'price': 29.99,
        'stock': 70,
        'image_url': '/static/images/products/kids_winterset.jpg',
        'category_id': 5  # Kids
    },
    {
        'name': 'Swim Set',
        'description': 'Quick-dry swim set with UV protection. Perfect for beach or pool days.',
        'price': 34.99,
        'stock': 55,
        'image_url': '/static/images/products/kids_swimset.jpg',
        'category_id': 5  # Kids
    }
]

def add_kids_category():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database")
        return False
    
    cursor = conn.cursor()
    try:
        # Check if Kids category already exists
        cursor.execute("SELECT * FROM categories WHERE name = 'Kids'")
        if cursor.fetchone() is None:
            # Add Kids category
            cursor.execute("INSERT INTO categories (name, description) VALUES (%s, %s)", 
                          ('Kids', 'Clothing and accessories for children'))
            conn.commit()
            print("Kids category added successfully")
        else:
            print("Kids category already exists")
        return True
    except mysql.connector.Error as e:
        print(f"Error adding Kids category: {e}")
        return False
    finally:
        close_connection(conn, cursor)

def add_sample_products():
    # First, add Kids category if it doesn't exist
    if not add_kids_category():
        return
    
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database")
        return
    
    cursor = conn.cursor()
    try:
        # Add sample products
        for product in sample_products:
            cursor.execute("""
                INSERT INTO products (name, description, price, stock, image_url, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                product['name'],
                product['description'],
                product['price'],
                product['stock'],
                product['image_url'],
                product['category_id']
            ))
        
        conn.commit()
        print(f"Successfully added {len(sample_products)} sample products")
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"Error adding sample products: {e}")
    finally:
        close_connection(conn, cursor)

if __name__ == "__main__":
    add_sample_products() 