from flask import render_template, redirect, url_for, request, flash, session
from app import app
from app.models import User
from functools import wraps

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Admin access decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login', next=request.url))
        
        if not session.get('is_admin'):
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('home'))
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        # Validate form data
        if not all([username, email, password, confirm_password, first_name, last_name]):
            flash('All fields are required', 'danger')
            return render_template('customer/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('customer/register.html')
        
        # Check if user already exists
        existing_user = User.get_by_username(username) or User.get_by_email(email)
        if existing_user:
            flash('Username or email already exists', 'danger')
            return render_template('customer/register.html')
        
        # Create new user
        success, result = User.create(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone=phone
        )
        
        if success:
            flash('Registration successful! Please login', 'success')
            return redirect(url_for('login'))
        else:
            flash(f'Registration failed: {result}', 'danger')
    
    return render_template('customer/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password', 'danger')
            return render_template('customer/login.html')
        
        user = User.get_by_username(username)
        
        if user and User.verify_password(user['password'], password):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            
            next_page = request.args.get('next')
            
            if user['is_admin']:
                return redirect(next_page or url_for('admin_dashboard'))
            else:
                return redirect(next_page or url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('customer/login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')
    user = User.get_by_id(user_id)
    
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('home'))
    
    return render_template('customer/profile.html', user=user) 