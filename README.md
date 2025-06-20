# Velvra - Luxury Clothing Store

Velvra is a stunning, fully functional clothing management system built with Flask. It features a luxurious design and includes functionalities for both customers and administrators.

## Features

### Customer Side
- Browse and search products
- Filter products by categories
- User registration and authentication
- Shopping cart functionality
- Checkout process with payment integration
- Order history and tracking

### Admin Side
- Dashboard with sales overview
- Product management (add, edit, delete)
- Category management
- Order management
- Payment status tracking

## Technologies Used

- **Backend**: Python, Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Authentication**: Flask-Bcrypt
- **Payment Processing**: Integrated payment gateway

## Installation and Setup

1. Clone the repository:
```
git clone https://github.com/yourusername/velvra.git
cd velvra
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up the MySQL database:
```
mysql -u root -p < database/velvra_db.sql
```

5. Run the application:
```
python run.py
```

6. Access the application:
   - Customer interface: http://localhost:5000/
   - Admin interface: http://localhost:5000/admin (login with admin/admin123)

## Project Structure

```
velvra/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/
│   │   ├── admin/
│   │   ├── customer/
│   │   └── partials/
│   ├── routes/
│   │   ├── admin_routes.py
│   │   ├── auth_routes.py
│   │   └── customer_routes.py
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   └── context_processors.py
├── database/
│   └── velvra_db.sql
├── run.py
└── requirements.txt
```

## Configuration

Database configuration can be modified in `app/database.py`.

## License

This project is licensed under the MIT License - see the LICENSE file for details. # Velvera
