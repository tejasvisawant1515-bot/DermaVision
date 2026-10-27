import os
import uuid
import json
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify, send_from_directory
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import Config
from database import db_manager
from ai_engine import skin_analyzer
from products_data import generate_recommendations

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database tables and seed products
with app.app_context():
    db_manager.init_db()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.before_request
def ensure_session_identity():
    if 'guest_id' not in session:
        session['guest_id'] = uuid.uuid4().hex


@app.context_processor
def inject_globals():
    """Injects current logged-in user and cart count into all templates."""
    current_user = None
    if 'user_id' in session:
        current_user = db_manager.get_user_by_id(session['user_id'])

    user_id = session.get('user_id')
    session_id = session.get('guest_id') if not user_id else None
    cart_count = db_manager.get_cart_count(user_id=user_id, session_id=session_id)

    return dict(current_user=current_user, cart_count=cart_count)


# ==========================================
# MAIN ROUTES
# ==========================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'GET':
        return render_template('analyze.html')

    # Handle POST submission
    budget = request.form.get('budget', 1000.0)
    try:
        budget = float(budget)
    except ValueError:
        budget = 1000.0

    image_file = request.files.get('image_file')
    captured_data = request.form.get('captured_image') # Base64 from camera

    saved_filename = None

    if image_file and image_file.filename != '':
        if not allowed_file(image_file.filename):
            flash('Invalid file format. Please upload JPG, PNG, or WebP.', 'danger')
            return redirect(url_for('analyze'))
        
        ext = image_file.filename.rsplit('.', 1)[1].lower()
        saved_filename = f"skin_{uuid.uuid4().hex[:12]}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
        image_file.save(filepath)

    elif captured_data and captured_data.startswith('data:image'):
        # Decode base64 camera image
        import base64
        try:
            header, encoded = captured_data.split(',', 1)
            file_data = base64.b64decode(encoded)
            saved_filename = f"camera_{uuid.uuid4().hex[:12]}.jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
            with open(filepath, 'wb') as f:
                f.write(file_data)
        except Exception as e:
            flash(f'Failed to process captured camera image: {str(e)}', 'danger')
            return redirect(url_for('analyze'))
    else:
        flash('Please upload a facial photo or capture one using your camera.', 'warning')
        return redirect(url_for('analyze'))

    # Run AI Analysis
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
        ai_result = skin_analyzer.analyze_image(filepath, app.config['UPLOAD_FOLDER'])

        skin_type = ai_result['skin_type']
        concerns = ai_result['concerns']
        scores = ai_result['scores']
        annotated_image = ai_result['annotated_image']

        # Generate Budget-Based Recommendations & Routine
        recs = generate_recommendations(skin_type, concerns, budget)

        # Store in Database
        user_id = session.get('user_id') # None if guest
        concerns_str = ", ".join(concerns)

        analysis_id = db_manager.save_analysis(
            user_id=user_id,
            original_image=saved_filename,
            analyzed_image=annotated_image,
            skin_type=skin_type,
            primary_concerns=concerns_str,
            scores=scores,
            selected_budget=budget,
            recommended_products=recs['products'],
            routine=recs['routine']
        )

        # Also store recent guest analysis in session
        session['recent_analysis_id'] = analysis_id

        return redirect(url_for('results', analysis_id=analysis_id))

    except Exception as e:
        flash(f'Error analyzing image: {str(e)}', 'danger')
        return redirect(url_for('analyze'))


@app.route('/results/<int:analysis_id>')
def results(analysis_id):
    analysis = db_manager.get_analysis_by_id(analysis_id)
    if not analysis:
        flash('Analysis report not found.', 'warning')
        return redirect(url_for('analyze'))

    # Prepare scores and budget calculation
    scores = {
        'sebum': analysis.get('sebum_score', 0),
        'acne': analysis.get('acne_score', 0),
        'pigmentation': analysis.get('pigmentation_score', 0),
        'dark_spots': analysis.get('dark_spots_score', 0),
        'texture': analysis.get('texture_score', 0),
        'redness': analysis.get('redness_score', 0)
    }

    products = analysis.get('recommended_products', [])
    total_cost = sum(p.get('price_inr', 0) for p in products)

    concerns_list = [c.strip() for c in analysis.get('primary_concerns', '').split(',') if c.strip()]

    return render_template(
        'results.html',
        analysis=analysis,
        scores=scores,
        concerns_list=concerns_list,
        products=products,
        total_cost=round(total_cost, 2),
        routine=analysis.get('routine', {})
    )


@app.route('/api/update_budget/<int:analysis_id>', methods=['POST'])
def update_budget(analysis_id):
    """Allows user to change budget on the fly and recomputes products & routines."""
    data = request.get_json() or {}
    new_budget = data.get('budget', 1000.0)
    try:
        new_budget = float(new_budget)
    except ValueError:
        new_budget = 1000.0

    analysis = db_manager.get_analysis_by_id(analysis_id)
    if not analysis:
        return jsonify({'success': False, 'error': 'Analysis not found'}), 404

    concerns = [c.strip() for c in analysis.get('primary_concerns', '').split(',') if c.strip()]
    recs = generate_recommendations(analysis['skin_type'], concerns, new_budget)

    # Update in database
    conn, engine = db_manager.get_connection()
    cursor = conn.cursor()
    placeholder = "%s" if engine == 'mysql' else "?"
    cursor.execute(f"""
        UPDATE analysis_history 
        SET selected_budget = {placeholder},
            recommended_products_json = {placeholder},
            routine_json = {placeholder}
        WHERE id = {placeholder}
    """, (new_budget, json.dumps(recs['products']), json.dumps(recs['routine']), analysis_id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        'success': True,
        'products': recs['products'],
        'total_cost': recs['total_cost'],
        'routine': recs['routine'],
        'within_budget': recs['within_budget']
    })


@app.route('/history')
def history():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your complete skin analysis history and order records.', 'info')
        # If guest has a recent analysis, redirect to it
        if 'recent_analysis_id' in session:
            return redirect(url_for('results', analysis_id=session['recent_analysis_id']))
        return redirect(url_for('login'))

    user_history = db_manager.get_user_history(user_id)
    user_orders = db_manager.get_user_orders(user_id)
    return render_template('history.html', history=user_history, orders=user_orders)


@app.route('/products')
def products():
    skin_type = request.args.get('skin_type', 'All')
    category = request.args.get('category', '')
    max_price = request.args.get('max_price', '')

    all_prods = db_manager.get_all_products(
        skin_type=skin_type if skin_type != 'All' else None,
        category=category if category else None
    )

    if max_price:
        try:
            p_limit = float(max_price)
            all_prods = [p for p in all_prods if p['price_inr'] <= p_limit]
        except ValueError:
            pass

    return render_template(
        'products.html',
        products=all_prods,
        selected_skin_type=skin_type,
        selected_category=category,
        max_price=max_price
    )


def get_current_cart_context():
    """Helper to calculate cart line items, subtotals, shipping and totals."""
    user_id = session.get('user_id')
    if not user_id and 'guest_id' not in session:
        session['guest_id'] = uuid.uuid4().hex
    session_id = session.get('guest_id') if not user_id else None
    items = db_manager.get_cart_items(user_id=user_id, session_id=session_id)
    subtotal = sum(item['item_total'] for item in items)
    # Free standard shipping on orders >= ₹499
    shipping = 0.0 if (subtotal >= 499.0 or subtotal == 0) else 49.0
    discount = 0.0
    total = round(subtotal + shipping - discount, 2)
    return {
        'items': items,
        'subtotal': round(subtotal, 2),
        'shipping': shipping,
        'discount': discount,
        'total': total,
        'user_id': user_id,
        'session_id': session_id
    }


# ==========================================
# E-COMMERCE: CART & CHECKOUT
# ==========================================

@app.route('/cart')
def view_cart():
    cart_ctx = get_current_cart_context()
    recent_analysis = None
    if 'recent_analysis_id' in session:
        recent_analysis = db_manager.get_analysis_by_id(session['recent_analysis_id'])
    return render_template('cart.html', cart=cart_ctx, analysis=recent_analysis)


@app.route('/api/cart/add', methods=['POST'])
def api_add_to_cart():
    data = request.get_json() or request.form.to_dict() or {}
    user_id = session.get('user_id')
    if not user_id and 'guest_id' not in session:
        session['guest_id'] = uuid.uuid4().hex
    session_id = session.get('guest_id') if not user_id else None

    # Support batch add (e.g. Add Complete Routine to Cart)
    products = data.get('products')
    if products and isinstance(products, list):
        added_count = 0
        for p in products:
            p_id = p.get('id') or p.get('product_id')
            qty = int(p.get('quantity', 1))
            if p_id:
                db_manager.add_to_cart(p_id, quantity=qty, user_id=user_id, session_id=session_id)
                added_count += 1
        cart_count = db_manager.get_cart_count(user_id=user_id, session_id=session_id)
        return jsonify({
            'success': True,
            'message': f'Successfully added {added_count} personalized products to your cart!',
            'cart_count': cart_count
        })

    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    if not product_id:
        return jsonify({'success': False, 'error': 'Product ID required'}), 400

    product = db_manager.get_product_by_id(product_id)
    if not product:
        return jsonify({'success': False, 'error': 'Product not found'}), 404

    db_manager.add_to_cart(product_id, quantity=quantity, user_id=user_id, session_id=session_id)
    cart_count = db_manager.get_cart_count(user_id=user_id, session_id=session_id)

    return jsonify({
        'success': True,
        'message': f'"{product["name"]}" added to your cart!',
        'cart_count': cart_count
    })


@app.route('/api/cart/update', methods=['POST'])
def api_update_cart():
    data = request.get_json() or {}
    cart_id = data.get('cart_id')
    quantity = int(data.get('quantity', 1))
    user_id = session.get('user_id')
    session_id = session.get('guest_id') if not user_id else None

    db_manager.update_cart_quantity(cart_id, quantity, user_id=user_id, session_id=session_id)
    cart_ctx = get_current_cart_context()
    cart_count = db_manager.get_cart_count(user_id=user_id, session_id=session_id)

    return jsonify({
        'success': True,
        'subtotal': cart_ctx['subtotal'],
        'shipping': cart_ctx['shipping'],
        'total': cart_ctx['total'],
        'cart_count': cart_count
    })


@app.route('/api/cart/remove', methods=['POST'])
def api_remove_cart():
    data = request.get_json() or {}
    cart_id = data.get('cart_id')
    user_id = session.get('user_id')
    session_id = session.get('guest_id') if not user_id else None

    db_manager.remove_from_cart(cart_id, user_id=user_id, session_id=session_id)
    cart_ctx = get_current_cart_context()
    cart_count = db_manager.get_cart_count(user_id=user_id, session_id=session_id)

    return jsonify({
        'success': True,
        'subtotal': cart_ctx['subtotal'],
        'shipping': cart_ctx['shipping'],
        'total': cart_ctx['total'],
        'cart_count': cart_count
    })


@app.route('/api/cart/clear', methods=['POST'])
def api_clear_cart():
    user_id = session.get('user_id')
    session_id = session.get('guest_id') if not user_id else None
    db_manager.clear_cart(user_id=user_id, session_id=session_id)
    return jsonify({'success': True, 'cart_count': 0})


@app.route('/checkout', methods=['GET'])
def checkout():
    cart_ctx = get_current_cart_context()
    if not cart_ctx['items']:
        flash('Your cart is empty. Please add recommended skincare products first.', 'warning')
        return redirect(url_for('products'))

    user_id = session.get('user_id')
    saved_addresses = db_manager.get_user_addresses(user_id) if user_id else []
    user = db_manager.get_user_by_id(user_id) if user_id else None

    return render_template(
        'checkout.html',
        cart=cart_ctx,
        saved_addresses=saved_addresses,
        user=user
    )


@app.route('/checkout/process', methods=['POST'])
def process_checkout():
    cart_ctx = get_current_cart_context()
    if not cart_ctx['items']:
        if request.is_json:
            return jsonify({'success': False, 'error': 'Cart is empty'}), 400
        flash('Your shopping cart is empty.', 'warning')
        return redirect(url_for('products'))

    data = request.get_json() if request.is_json else request.form.to_dict()

    full_name = data.get('full_name', '').strip()
    phone = data.get('phone', '').strip()
    address_line1 = data.get('address_line1', '').strip()
    address_line2 = data.get('address_line2', '').strip()
    city = data.get('city', '').strip()
    state = data.get('state', '').strip()
    pincode = data.get('pincode', '').strip()
    payment_method = data.get('payment_method', 'UPI')
    save_addr = data.get('save_address') in ['1', 'true', True, 'on']
    shipping_speed = data.get('shipping_speed', 'standard')

    if not full_name or not phone or not address_line1 or not city or not state or not pincode:
        if request.is_json:
            return jsonify({'success': False, 'error': 'Please fill all required delivery address fields.'}), 400
        flash('Please fill all required delivery address fields.', 'danger')
        return redirect(url_for('checkout'))

    user_id = session.get('user_id')
    if user_id and save_addr:
        existing_addrs = db_manager.get_user_addresses(user_id)
        db_manager.save_address(
            user_id=user_id,
            full_name=full_name,
            phone=phone,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            pincode=pincode,
            is_default=1 if not existing_addrs else 0
        )

    # Calculate shipping and total
    shipping_fee = 49.0 if shipping_speed == 'express' else cart_ctx['shipping']
    total_amount = round(cart_ctx['subtotal'] + shipping_fee - cart_ctx['discount'], 2)

    # Generate Order Number & Payment Transaction ID
    now_str = datetime.now().strftime('%Y%m%d')
    order_number = f"DV-{now_str}-{uuid.uuid4().hex[:6].upper()}"
    payment_id = f"PAY-INR-{uuid.uuid4().hex[:10].upper()}"
    payment_status = 'Pending' if payment_method == 'COD' else 'Paid'

    delivery_full_address = f"{address_line1}, {address_line2}".strip(', ')
    order_id = db_manager.create_order(
        user_id=user_id,
        order_number=order_number,
        delivery_name=full_name,
        delivery_phone=phone,
        delivery_address=delivery_full_address,
        delivery_city=city,
        delivery_state=state,
        delivery_pincode=pincode,
        subtotal=cart_ctx['subtotal'],
        shipping_fee=shipping_fee,
        discount=cart_ctx['discount'],
        total_amount=total_amount,
        payment_method=payment_method,
        payment_status=payment_status,
        payment_id=payment_id,
        order_status='Confirmed',
        items=cart_ctx['items']
    )

    # Empty user cart
    db_manager.clear_cart(user_id=user_id, session_id=cart_ctx['session_id'])

    # Save to session
    session['last_order_number'] = order_number

    if request.is_json:
        return jsonify({
            'success': True,
            'order_number': order_number,
            'redirect_url': url_for('order_confirmation', order_number=order_number)
        })

    flash('Order placed successfully! Thank you for trusting DermaVisionAI.', 'success')
    return redirect(url_for('order_confirmation', order_number=order_number))


@app.route('/order-confirmation/<order_number>')
def order_confirmation(order_number):
    order = db_manager.get_order_by_number(order_number)
    if not order:
        flash('Order not found.', 'warning')
        return redirect(url_for('index'))

    recent_analysis = None
    if 'recent_analysis_id' in session:
        recent_analysis = db_manager.get_analysis_by_id(session['recent_analysis_id'])

    return render_template('order_confirmation.html', order=order, analysis=recent_analysis)


@app.route('/orders')
def orders():
    user_id = session.get('user_id')
    if not user_id:
        if 'last_order_number' in session:
            return redirect(url_for('order_confirmation', order_number=session['last_order_number']))
        flash('Please log in to view your complete order history.', 'info')
        return redirect(url_for('login'))

    user_orders = db_manager.get_user_orders(user_id)
    return render_template('orders.html', orders=user_orders)


@app.route('/about')
def about():
    return render_template('about.html')


# ==========================================
# AUTHENTICATION
# ==========================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        full_name = request.form.get('full_name', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        age = request.form.get('age') or None
        gender = request.form.get('gender') or None

        if not username or not email or not password or not full_name:
            flash('All required fields must be completed.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if db_manager.get_user_by_username(username):
            flash('Username is already taken. Please choose another.', 'warning')
            return render_template('register.html')

        if db_manager.get_user_by_email(email):
            flash('Email is already registered. Please log in.', 'warning')
            return render_template('register.html')

        pwd_hash = generate_password_hash(password)
        try:
            user_id = db_manager.create_user(
                username=username,
                email=email,
                password_hash=pwd_hash,
                full_name=full_name,
                age=int(age) if age else None,
                gender=gender
            )
            session['user_id'] = user_id
            session['username'] = username
            session['full_name'] = full_name
            flash('Welcome to DermaVisionAI! Your account was created successfully.', 'success')

            # Associate previous guest analysis if exists
            if 'recent_analysis_id' in session:
                conn, engine = db_manager.get_connection()
                c = conn.cursor()
                pl = "%s" if engine == 'mysql' else "?"
                c.execute(f"UPDATE analysis_history SET user_id = {pl} WHERE id = {pl}", (user_id, session['recent_analysis_id']))
                conn.commit()
                c.close()
                conn.close()

            # Merge any guest cart
            if 'guest_id' in session:
                db_manager.merge_guest_cart(session['guest_id'], user_id)

            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Registration error: {str(e)}', 'danger')
            return render_template('register.html')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        login_input = request.form.get('login_input', '').strip()
        password = request.form.get('password', '')

        # Check by username or email
        user = db_manager.get_user_by_username(login_input)
        if not user:
            user = db_manager.get_user_by_email(login_input)

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            flash(f"Welcome back, {user['full_name']}!", 'success')

            # Associate any guest analysis performed prior to login
            if 'recent_analysis_id' in session:
                conn, engine = db_manager.get_connection()
                c = conn.cursor()
                pl = "%s" if engine == 'mysql' else "?"
                c.execute(f"UPDATE analysis_history SET user_id = {pl} WHERE id = {pl} AND user_id IS NULL", (user['id'], session['recent_analysis_id']))
                conn.commit()
                c.close()
                conn.close()

            # Merge any guest cart
            if 'guest_id' in session:
                db_manager.merge_guest_cart(session['guest_id'], user['id'])

            return redirect(url_for('index'))
        else:
            flash('Invalid username/email or password.', 'danger')
            return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been securely logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your profile.', 'info')
        return redirect(url_for('login'))

    user = db_manager.get_user_by_id(user_id)
    history = db_manager.get_user_history(user_id)
    orders = db_manager.get_user_orders(user_id)
    addresses = db_manager.get_user_addresses(user_id)
    return render_template('profile.html', user=user, history=history, orders=orders, addresses=addresses)


if __name__ == '__main__':
    print("[DermaVisionAI] Launching server on http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
