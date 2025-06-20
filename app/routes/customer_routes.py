from flask import render_template, redirect, url_for, request, flash, session, jsonify
from app import app
from app.models import Product, Category, Cart, Order
from app.routes.auth_routes import login_required

@app.route('/')
def home():
    featured_products = Product.get_all(limit=8)
    categories = Category.get_all()
    return render_template('customer/home.html', 
                          products=featured_products, 
                          categories=categories)

@app.route('/products')
def products():
    category_id = request.args.get('category', type=int)
    categories = Category.get_all()
    
    if category_id:
        products = Product.get_all(category_id=category_id)
        category = Category.get_by_id(category_id)
        category_name = category['name'] if category else 'Unknown'
    else:
        products = Product.get_all()
        category_name = 'All Products'
    
    return render_template('customer/products.html', 
                          products=products, 
                          categories=categories,
                          current_category=category_id,
                          category_name=category_name)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.get_by_id(product_id)
    
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('products'))
    
    related_products = Product.get_all(limit=4, category_id=product['category_id'])
    
    return render_template('customer/product_detail.html', 
                          product=product,
                          related_products=related_products)

@app.route('/cart')
@login_required
def cart():
    user_id = session.get('user_id')
    cart_items = Cart.get_user_cart(user_id)
    
    total = sum(item['subtotal'] for item in cart_items)
    
    return render_template('customer/cart.html', 
                          cart_items=cart_items,
                          total=total)

@app.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    user_id = session.get('user_id')
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    
    if not product_id:
        flash('Invalid product', 'danger')
        return redirect(request.referrer or url_for('products'))
    
    success, message = Cart.add_item(user_id, product_id, quantity)
    
    if success:
        flash('Product added to cart', 'success')
    else:
        flash(f'Error: {message}', 'danger')
    
    return redirect(request.referrer or url_for('products'))

@app.route('/cart/update', methods=['POST'])
@login_required
def update_cart():
    cart_id = request.form.get('cart_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    
    if not cart_id:
        return jsonify({'success': False, 'message': 'Invalid cart item'})
    
    success, message = Cart.update_quantity(cart_id, quantity)
    
    return jsonify({'success': success, 'message': message})

@app.route('/cart/remove/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    success, message = Cart.remove_item(cart_id)
    
    if success:
        flash('Item removed from cart', 'success')
    else:
        flash(f'Error: {message}', 'danger')
    
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    user_id = session.get('user_id')
    cart_items = Cart.get_user_cart(user_id)
    
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('products'))
    
    total = sum(item['subtotal'] for item in cart_items)
    
    if request.method == 'POST':
        shipping_address = request.form.get('shipping_address')
        payment_method = request.form.get('payment_method')
        
        if not shipping_address or not payment_method:
            flash('Please fill all required fields', 'danger')
            return render_template('customer/checkout.html', 
                                  cart_items=cart_items,
                                  total=total)
        
        success, result = Order.create(
            user_id=user_id,
            total_amount=total,
            shipping_address=shipping_address,
            payment_method=payment_method
        )
        
        if success:
            flash('Order placed successfully', 'success')
            return redirect(url_for('order_confirmation', order_id=result))
        else:
            flash(f'Error: {result}', 'danger')
    
    return render_template('customer/checkout.html', 
                          cart_items=cart_items,
                          total=total)

@app.route('/order/confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    user_id = session.get('user_id')
    
    order, items = Order.get_order_details(order_id)
    
    if not order or order['user_id'] != user_id:
        flash('Order not found', 'danger')
        return redirect(url_for('orders'))
    
    return render_template('customer/order_confirmation.html', 
                          order=order,
                          items=items)

@app.route('/orders')
@login_required
def orders():
    user_id = session.get('user_id')
    orders = Order.get_user_orders(user_id)
    
    return render_template('customer/orders.html', orders=orders)

@app.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    user_id = session.get('user_id')
    
    order, items = Order.get_order_details(order_id)
    
    if not order or order['user_id'] != user_id:
        flash('Order not found', 'danger')
        return redirect(url_for('orders'))
    
    return render_template('customer/order_detail.html', 
                          order=order,
                          items=items) 