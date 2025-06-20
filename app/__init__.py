from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'velvra_secret_key'
bcrypt = Bcrypt(app)

# Register context processors
from app.context_processors import inject_categories
app.context_processor(inject_categories)

from app.routes import customer_routes, admin_routes, auth_routes 