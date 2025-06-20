from flask import render_template, redirect, url_for, request, flash, session
from app import app
from app.models import Product, Category, Order, User
from app.routes.auth_routes import admin_required
from app.database import get_db_connection, close_connection
from mysql.connector import Error
import os
from werkzeug.utils import secure_filename

# Configure upload folder
UPLOAD_FOLDER = 'app/static/images/products'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin')
@admin_required
def admin_dashboard():
    recent_orders = Order.get_all_orders(limit=5)
    
    return render_template('admin/dashboard.html', 
                          recent_orders=recent_orders)

@app.route('/admin/products')
@admin_required
def admin_products():
    products = Product.get_all()
    categories = Category.get_all()
    
    return render_template('admin/products.html', 
                          products=products,
                          categories=categories)

@app.route('/admin/product/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    categories = Category.get_all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        stock = request.form.get('stock')
        category_id = request.form.get('category_id')
        
        # Validate form data
        if not all([name, price, stock, category_id]):
            flash('All fields are required', 'danger')
            return render_template('admin/product_form.html', categories=categories)
        
        # Handle image upload
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Create directory if it doesn't exist
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_url = f'/static/images/products/{filename}'
        
        # Create product
        success, result = Product.create(
            name=name,
            description=description,
            price=price,
            stock=stock,
            image_url=image_url,
            category_id=category_id
        )
        
        if success:
            flash('Product added successfully', 'success')
            return redirect(url_for('admin_products'))
        else:
            flash(f'Error: {result}', 'danger')
    
    return render_template('admin/product_form.html', categories=categories)

@app.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    product = Product.get_by_id(product_id)
    
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('admin_products'))
    
    categories = Category.get_all()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        stock = request.form.get('stock')
        category_id = request.form.get('category_id')
        
        # Validate form data
        if not all([name, price, stock, category_id]):
            flash('All fields are required', 'danger')
            return render_template('admin/product_form.html', 
                                  product=product,
                                  categories=categories)
        
        # Handle image upload
        image_url = product['image_url']
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Create directory if it doesn't exist
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_url = f'/static/images/products/{filename}'
        
        # Update product
        success, message = Product.update(
            product_id=product_id,
            name=name,
            description=description,
            price=price,
            stock=stock,
            image_url=image_url,
            category_id=category_id
        )
        
        if success:
            flash('Product updated successfully', 'success')
            return redirect(url_for('admin_products'))
        else:
            flash(f'Error: {message}', 'danger')
    
    return render_template('admin/product_form.html', 
                          product=product,
                          categories=categories)

@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    success, message = Product.delete(product_id)
    
    if success:
        flash('Product deleted successfully', 'success')
    else:
        flash(f'Error: {message}', 'danger')
    
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@admin_required
def admin_orders():
    orders = Order.get_all_orders()
    
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/order/<int:order_id>')
@admin_required
def admin_order_detail(order_id):
    order, items = Order.get_order_details(order_id)
    
    if not order:
        flash('Order not found', 'danger')
        return redirect(url_for('admin_orders'))
    
    return render_template('admin/order_detail.html', 
                          order=order,
                          items=items)

@app.route('/admin/order/status/<int:order_id>', methods=['POST'])
@admin_required
def admin_update_order_status(order_id):
    status = request.form.get('status')
    
    if not status:
        flash('Status is required', 'danger')
        return redirect(url_for('admin_order_detail', order_id=order_id))
    
    success, message = Order.update_status(order_id, status)
    
    if success:
        flash('Order status updated successfully', 'success')
    else:
        flash(f'Error: {message}', 'danger')
    
    return redirect(url_for('admin_order_detail', order_id=order_id))

@app.route('/admin/order/payment/<int:order_id>', methods=['POST'])
@admin_required
def admin_update_payment_status(order_id):
    payment_status = request.form.get('payment_status')
    
    if not payment_status:
        flash('Payment status is required', 'danger')
        return redirect(url_for('admin_order_detail', order_id=order_id))
    
    success, message = Order.update_payment_status(order_id, payment_status)
    
    if success:
        flash('Payment status updated successfully', 'success')
    else:
        flash(f'Error: {message}', 'danger')
    
    return redirect(url_for('admin_order_detail', order_id=order_id))

@app.route('/admin/categories')
@admin_required
def admin_categories():
    categories = Category.get_all()
    
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/category/add', methods=['POST'])
@admin_required
def admin_add_category():
    name = request.form.get('name')
    description = request.form.get('description', '')
    
    if not name:
        flash('Category name is required', 'danger')
        return redirect(url_for('admin_categories'))
    
    # Add category
    conn = get_db_connection()
    if not conn:
        flash('Database connection error', 'danger')
        return redirect(url_for('admin_categories'))
    
    cursor = conn.cursor()
    try:
        query = "INSERT INTO categories (name, description) VALUES (%s, %s)"
        cursor.execute(query, (name, description))
        conn.commit()
        flash('Category added successfully', 'success')
    except Error as e:
        flash(f'Error: {str(e)}', 'danger')
    finally:
        close_connection(conn, cursor)
    
    return redirect(url_for('admin_categories'))

@app.route('/admin/category/edit/<int:category_id>', methods=['POST'])
@admin_required
def admin_edit_category(category_id):
    name = request.form.get('name')
    description = request.form.get('description', '')
    
    if not name:
        flash('Category name is required', 'danger')
        return redirect(url_for('admin_categories'))
    
    # Update category
    conn = get_db_connection()
    if not conn:
        flash('Database connection error', 'danger')
        return redirect(url_for('admin_categories'))
    
    cursor = conn.cursor()
    try:
        query = "UPDATE categories SET name = %s, description = %s WHERE category_id = %s"
        cursor.execute(query, (name, description, category_id))
        conn.commit()
        flash('Category updated successfully', 'success')
    except Error as e:
        flash(f'Error: {str(e)}', 'danger')
    finally:
        close_connection(conn, cursor)
    
    return redirect(url_for('admin_categories'))

@app.route('/admin/category/delete/<int:category_id>', methods=['POST'])
@admin_required
def admin_delete_category(category_id):
    # Delete category
    conn = get_db_connection()
    if not conn:
        flash('Database connection error', 'danger')
        return redirect(url_for('admin_categories'))
    
    cursor = conn.cursor()
    try:
        # Check if category has products
        check_query = "SELECT COUNT(*) FROM products WHERE category_id = %s"
        cursor.execute(check_query, (category_id,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            flash('Cannot delete category with associated products', 'danger')
            return redirect(url_for('admin_categories'))
        
        query = "DELETE FROM categories WHERE category_id = %s"
        cursor.execute(query, (category_id,))
        conn.commit()
        flash('Category deleted successfully', 'success')
    except Error as e:
        flash(f'Error: {str(e)}', 'danger')
    finally:
        close_connection(conn, cursor)
    
    return redirect(url_for('admin_categories')) 