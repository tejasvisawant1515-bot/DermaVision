import os
import json
import sqlite3
from config import Config

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    MySQLError = Exception


class DatabaseManager:
    def __init__(self):
        self.db_type = 'sqlite'
        self.test_connection()

    def test_connection(self):
        """Tests MySQL connection; falls back to SQLite if unreachable."""
        if Config.DB_TYPE == 'mysql' and MYSQL_AVAILABLE:
            try:
                # Test connection to MySQL server
                conn = mysql.connector.connect(
                    host=Config.MYSQL_HOST,
                    port=Config.MYSQL_PORT,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    connection_timeout=2
                )
                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.MYSQL_DB}` DEFAULT CHARACTER SET utf8mb4;")
                conn.commit()
                cursor.close()
                conn.close()
                self.db_type = 'mysql'
                print(f"[DatabaseManager] Successfully connected to MySQL database: {Config.MYSQL_DB}")
                return
            except Exception as e:
                print(f"[DatabaseManager] MySQL not reachable ({e}). Switching seamlessly to SQLite fallback.")
                self.db_type = 'sqlite'
        else:
            self.db_type = 'sqlite'

    def get_connection(self):
        """Returns an active connection and cursor dict/tuple."""
        if self.db_type == 'mysql':
            try:
                conn = mysql.connector.connect(
                    host=Config.MYSQL_HOST,
                    port=Config.MYSQL_PORT,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    database=Config.MYSQL_DB
                )
                return conn, 'mysql'
            except Exception as e:
                print(f"[DatabaseManager] MySQL reconnect failed ({e}). Using SQLite fallback.")
                self.db_type = 'sqlite'

        # SQLite Connection
        conn = sqlite3.connect(Config.SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        return conn, 'sqlite'

    def init_db(self):
        """Creates tables and populates seed data if empty."""
        conn, engine = self.get_connection()
        cursor = conn.cursor()

        if engine == 'mysql':
            # Create MySQL tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    age INT DEFAULT NULL,
                    gender VARCHAR(20) DEFAULT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(150) NOT NULL,
                    brand VARCHAR(100) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    price_inr DECIMAL(10, 2) NOT NULL,
                    target_skin_type VARCHAR(50) NOT NULL,
                    target_concerns VARCHAR(255) NOT NULL,
                    key_ingredients VARCHAR(255) NOT NULL,
                    description TEXT,
                    image_url VARCHAR(255) DEFAULT NULL,
                    budget_tier VARCHAR(30) NOT NULL,
                    usage_time VARCHAR(30) NOT NULL DEFAULT 'Both',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT DEFAULT NULL,
                    original_image VARCHAR(255) NOT NULL,
                    analyzed_image VARCHAR(255) DEFAULT NULL,
                    skin_type VARCHAR(50) NOT NULL,
                    primary_concerns VARCHAR(255) NOT NULL,
                    sebum_score FLOAT DEFAULT 0.0,
                    acne_score FLOAT DEFAULT 0.0,
                    pigmentation_score FLOAT DEFAULT 0.0,
                    dark_spots_score FLOAT DEFAULT 0.0,
                    texture_score FLOAT DEFAULT 0.0,
                    redness_score FLOAT DEFAULT 0.0,
                    selected_budget DECIMAL(10, 2) DEFAULT 1000.00,
                    recommended_products_json LONGTEXT,
                    routine_json LONGTEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS addresses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT DEFAULT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20) NOT NULL,
                    address_line1 VARCHAR(255) NOT NULL,
                    address_line2 VARCHAR(255) DEFAULT '',
                    city VARCHAR(100) NOT NULL,
                    state VARCHAR(100) NOT NULL,
                    pincode VARCHAR(20) NOT NULL,
                    is_default INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cart_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT DEFAULT NULL,
                    session_id VARCHAR(100) DEFAULT NULL,
                    product_id INT NOT NULL,
                    quantity INT DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_number VARCHAR(50) NOT NULL UNIQUE,
                    user_id INT DEFAULT NULL,
                    delivery_name VARCHAR(100) NOT NULL,
                    delivery_phone VARCHAR(20) NOT NULL,
                    delivery_address TEXT NOT NULL,
                    delivery_city VARCHAR(100) NOT NULL,
                    delivery_state VARCHAR(100) NOT NULL,
                    delivery_pincode VARCHAR(20) NOT NULL,
                    subtotal DECIMAL(10, 2) NOT NULL,
                    shipping_fee DECIMAL(10, 2) DEFAULT 0.00,
                    discount DECIMAL(10, 2) DEFAULT 0.00,
                    total_amount DECIMAL(10, 2) NOT NULL,
                    payment_method VARCHAR(50) NOT NULL,
                    payment_status VARCHAR(30) DEFAULT 'Paid',
                    payment_id VARCHAR(100) DEFAULT NULL,
                    order_status VARCHAR(30) DEFAULT 'Confirmed',
                    items_json LONGTEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            conn.commit()

            # Check if products need seeding
            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]
            if count == 0:
                self._seed_default_products(cursor, engine)
                conn.commit()

        else:
            # Create SQLite tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    age INTEGER DEFAULT NULL,
                    gender TEXT DEFAULT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    brand TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price_inr REAL NOT NULL,
                    target_skin_type TEXT NOT NULL,
                    target_concerns TEXT NOT NULL,
                    key_ingredients TEXT NOT NULL,
                    description TEXT,
                    image_url TEXT DEFAULT NULL,
                    budget_tier TEXT NOT NULL,
                    usage_time TEXT NOT NULL DEFAULT 'Both',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER DEFAULT NULL,
                    original_image TEXT NOT NULL,
                    analyzed_image TEXT DEFAULT NULL,
                    skin_type TEXT NOT NULL,
                    primary_concerns TEXT NOT NULL,
                    sebum_score REAL DEFAULT 0.0,
                    acne_score REAL DEFAULT 0.0,
                    pigmentation_score REAL DEFAULT 0.0,
                    dark_spots_score REAL DEFAULT 0.0,
                    texture_score REAL DEFAULT 0.0,
                    redness_score REAL DEFAULT 0.0,
                    selected_budget REAL DEFAULT 1000.00,
                    recommended_products_json TEXT,
                    routine_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS addresses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER DEFAULT NULL,
                    full_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    address_line1 TEXT NOT NULL,
                    address_line2 TEXT DEFAULT '',
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    pincode TEXT NOT NULL,
                    is_default INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cart_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER DEFAULT NULL,
                    session_id TEXT DEFAULT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_number TEXT NOT NULL UNIQUE,
                    user_id INTEGER DEFAULT NULL,
                    delivery_name TEXT NOT NULL,
                    delivery_phone TEXT NOT NULL,
                    delivery_address TEXT NOT NULL,
                    delivery_city TEXT NOT NULL,
                    delivery_state TEXT NOT NULL,
                    delivery_pincode TEXT NOT NULL,
                    subtotal REAL NOT NULL,
                    shipping_fee REAL DEFAULT 0.00,
                    discount REAL DEFAULT 0.00,
                    total_amount REAL NOT NULL,
                    payment_method TEXT NOT NULL,
                    payment_status TEXT DEFAULT 'Paid',
                    payment_id TEXT DEFAULT NULL,
                    order_status TEXT DEFAULT 'Confirmed',
                    items_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
                );
            """)
            conn.commit()

            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]
            if count == 0:
                self._seed_default_products(cursor, engine)
                conn.commit()

        cursor.close()
        conn.close()
        print(f"[DatabaseManager] Database initialized successfully on engine: {engine}")

    def _seed_default_products(self, cursor, engine):
        """Populates seed products into products table."""
        from products_data import SEED_PRODUCTS
        placeholder = "%s" if engine == 'mysql' else "?"
        query = f"""
            INSERT INTO products (name, brand, category, price_inr, target_skin_type, target_concerns, key_ingredients, description, budget_tier, usage_time)
            VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
        """
        for p in SEED_PRODUCTS:
            cursor.execute(query, (
                p['name'], p['brand'], p['category'], p['price_inr'],
                p['target_skin_type'], p['target_concerns'], p['key_ingredients'],
                p['description'], p['budget_tier'], p['usage_time']
            ))

    # --- User Operations ---
    def create_user(self, username, email, password_hash, full_name, age=None, gender=None):
        conn, engine = self.get_connection()
        cursor = conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        try:
            cursor.execute(f"""
                INSERT INTO users (username, email, password_hash, full_name, age, gender)
                VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
            """, (username, email, password_hash, full_name, age, gender))
            conn.commit()
            user_id = cursor.lastrowid
            return user_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_user_by_username(self, username):
        conn, engine = self.get_connection()
        cursor = conn.cursor(dictionary=True) if engine == 'mysql' else conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        cursor.execute(f"SELECT * FROM users WHERE username = {placeholder}", (username,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(row) if row else None

    def get_user_by_email(self, email):
        conn, engine = self.get_connection()
        cursor = conn.cursor(dictionary=True) if engine == 'mysql' else conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        cursor.execute(f"SELECT * FROM users WHERE email = {placeholder}", (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(row) if row else None

    def get_user_by_id(self, user_id):
        conn, engine = self.get_connection()
        cursor = conn.cursor(dictionary=True) if engine == 'mysql' else conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        cursor.execute(f"SELECT * FROM users WHERE id = {placeholder}", (user_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(row) if row else None

    # --- Analysis History ---
    def save_analysis(self, user_id, original_image, analyzed_image, skin_type,
                      primary_concerns, scores, selected_budget, recommended_products, routine):
        conn, engine = self.get_connection()
        cursor = conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        try:
            cursor.execute(f"""
                INSERT INTO analysis_history (
                    user_id, original_image, analyzed_image, skin_type, primary_concerns,
                    sebum_score, acne_score, pigmentation_score, dark_spots_score,
                    texture_score, redness_score, selected_budget,
                    recommended_products_json, routine_json
                ) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder},
                          {placeholder}, {placeholder}, {placeholder}, {placeholder},
                          {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
            """, (
                user_id,
                original_image,
                analyzed_image,
                skin_type,
                primary_concerns,
                scores.get('sebum', 0.0),
                scores.get('acne', 0.0),
                scores.get('pigmentation', 0.0),
                scores.get('dark_spots', 0.0),
                scores.get('texture', 0.0),
                scores.get('redness', 0.0),
                float(selected_budget),
                json.dumps(recommended_products),
                json.dumps(routine)
            ))
            conn.commit()
            analysis_id = cursor.lastrowid
            return analysis_id
        finally:
            cursor.close()
            conn.close()

    def get_analysis_by_id(self, analysis_id):
        conn, engine = self.get_connection()
        cursor = conn.cursor(dictionary=True) if engine == 'mysql' else conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        cursor.execute(f"SELECT * FROM analysis_history WHERE id = {placeholder}", (analysis_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            return None
        data = dict(row)
        if isinstance(data.get('recommended_products_json'), str):
            try:
                data['recommended_products'] = json.loads(data['recommended_products_json'])
            except Exception:
                data['recommended_products'] = []
        if isinstance(data.get('routine_json'), str):
            try:
                data['routine'] = json.loads(data['routine_json'])
            except Exception:
                data['routine'] = {}
        return data

    def get_user_history(self, user_id, limit=20):
        conn, engine = self.get_connection()
        cursor = conn.cursor(dictionary=True) if engine == 'mysql' else conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        cursor.execute(f"""
            SELECT * FROM analysis_history 
            WHERE user_id = {placeholder}
            ORDER BY created_at DESC 
            LIMIT {limit}
        """, (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        results = []
        for r in rows:
            item = dict(r)
            if isinstance(item.get('recommended_products_json'), str):
                try:
                    item['recommended_products'] = json.loads(item['recommended_products_json'])
                except Exception:
                    item['recommended_products'] = []
            if isinstance(item.get('routine_json'), str):
                try:
                    item['routine'] = json.loads(item['routine_json'])
                except Exception:
                    item['routine'] = {}
            results.append(item)
        return results

    # --- Products & Recommendation ---
    def get_all_products(self, skin_type=None, category=None):
        conn, engine = self.get_connection()
        cursor = conn.cursor(dictionary=True) if engine == 'mysql' else conn.cursor()
        query = "SELECT * FROM products WHERE 1=1"
        params = []
        placeholder = "%s" if engine == 'mysql' else "?"

        if skin_type and skin_type != 'All':
            query += f" AND (target_skin_type = {placeholder} OR target_skin_type = 'All')"
            params.append(skin_type)
        if category:
            query += f" AND category = {placeholder}"
            params.append(category)

        query += " ORDER BY category, price_inr ASC"
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(r) for r in rows]

    def get_product_by_id(self, product_id):
        conn, engine = self.get_connection()
        cursor = conn.cursor(dictionary=True) if engine == 'mysql' else conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        cursor.execute(f"SELECT * FROM products WHERE id = {placeholder}", (product_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(row) if row else None

    # --- Cart Operations ---
    def get_cart_items(self, user_id=None, session_id=None):
        if not user_id and not session_id:
            return []
        conn, engine = self.get_connection()
        cursor = conn.cursor(dictionary=True) if engine == 'mysql' else conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"

        if user_id:
            query = f"""
                SELECT c.id as cart_id, c.quantity, c.product_id,
                       p.name, p.brand, p.category, p.price_inr, p.target_skin_type,
                       p.target_concerns, p.key_ingredients, p.description, p.image_url
                FROM cart_items c
                JOIN products p ON c.product_id = p.id
                WHERE c.user_id = {placeholder}
                ORDER BY c.created_at ASC
            """
            cursor.execute(query, (user_id,))
        else:
            query = f"""
                SELECT c.id as cart_id, c.quantity, c.product_id,
                       p.name, p.brand, p.category, p.price_inr, p.target_skin_type,
                       p.target_concerns, p.key_ingredients, p.description, p.image_url
                FROM cart_items c
                JOIN products p ON c.product_id = p.id
                WHERE c.session_id = {placeholder}
                ORDER BY c.created_at ASC
            """
            cursor.execute(query, (session_id,))

        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        items = []
        for r in rows:
            item = dict(r)
            item['item_total'] = round(float(item['price_inr']) * int(item['quantity']), 2)
            items.append(item)
        return items

    def add_to_cart(self, product_id, quantity=1, user_id=None, session_id=None):
        if not user_id and not session_id:
            return False
        conn, engine = self.get_connection()
        cursor = conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"

        # Check existing item in cart
        if user_id:
            check_q = f"SELECT id, quantity FROM cart_items WHERE user_id = {placeholder} AND product_id = {placeholder}"
            cursor.execute(check_q, (user_id, product_id))
        else:
            check_q = f"SELECT id, quantity FROM cart_items WHERE session_id = {placeholder} AND product_id = {placeholder}"
            cursor.execute(check_q, (session_id, product_id))

        existing = cursor.fetchone()
        if existing:
            cart_id = existing[0] if isinstance(existing, (tuple, list)) else existing['id']
            curr_qty = existing[1] if isinstance(existing, (tuple, list)) else existing['quantity']
            new_qty = curr_qty + quantity
            update_q = f"UPDATE cart_items SET quantity = {placeholder} WHERE id = {placeholder}"
            cursor.execute(update_q, (new_qty, cart_id))
        else:
            if user_id:
                ins_q = f"INSERT INTO cart_items (user_id, product_id, quantity) VALUES ({placeholder}, {placeholder}, {placeholder})"
                cursor.execute(ins_q, (user_id, product_id, quantity))
            else:
                ins_q = f"INSERT INTO cart_items (session_id, product_id, quantity) VALUES ({placeholder}, {placeholder}, {placeholder})"
                cursor.execute(ins_q, (session_id, product_id, quantity))

        conn.commit()
        cursor.close()
        conn.close()
        return True

    def update_cart_quantity(self, cart_id, quantity, user_id=None, session_id=None):
        conn, engine = self.get_connection()
        cursor = conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"

        if quantity <= 0:
            if user_id:
                cursor.execute(f"DELETE FROM cart_items WHERE id = {placeholder} AND user_id = {placeholder}", (cart_id, user_id))
            else:
                cursor.execute(f"DELETE FROM cart_items WHERE id = {placeholder} AND session_id = {placeholder}", (cart_id, session_id))
        else:
            if user_id:
                cursor.execute(f"UPDATE cart_items SET quantity = {placeholder} WHERE id = {placeholder} AND user_id = {placeholder}", (quantity, cart_id, user_id))
            else:
                cursor.execute(f"UPDATE cart_items SET quantity = {placeholder} WHERE id = {placeholder} AND session_id = {placeholder}", (quantity, cart_id, session_id))

        conn.commit()
        cursor.close()
        conn.close()
        return True

    def remove_from_cart(self, cart_id, user_id=None, session_id=None):
        conn, engine = self.get_connection()
        cursor = conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        if user_id:
            cursor.execute(f"DELETE FROM cart_items WHERE id = {placeholder} AND user_id = {placeholder}", (cart_id, user_id))
        else:
            cursor.execute(f"DELETE FROM cart_items WHERE id = {placeholder} AND session_id = {placeholder}", (cart_id, session_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def clear_cart(self, user_id=None, session_id=None):
        conn, engine = self.get_connection()
        cursor = conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        if user_id:
            cursor.execute(f"DELETE FROM cart_items WHERE user_id = {placeholder}", (user_id,))
        elif session_id:
            cursor.execute(f"DELETE FROM cart_items WHERE session_id = {placeholder}", (session_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def get_cart_count(self, user_id=None, session_id=None):
        if not user_id and not session_id:
            return 0
        conn, engine = self.get_connection()
        cursor = conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        if user_id:
            cursor.execute(f"SELECT COALESCE(SUM(quantity), 0) FROM cart_items WHERE user_id = {placeholder}", (user_id,))
        else:
            cursor.execute(f"SELECT COALESCE(SUM(quantity), 0) FROM cart_items WHERE session_id = {placeholder}", (session_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return int(row[0]) if row and row[0] is not None else 0

    def merge_guest_cart(self, session_id, user_id):
        if not session_id or not user_id:
            return
        guest_items = self.get_cart_items(session_id=session_id)
        for item in guest_items:
            self.add_to_cart(item['product_id'], quantity=item['quantity'], user_id=user_id)
        self.clear_cart(session_id=session_id)

    # --- Address Operations ---
    def save_address(self, user_id, full_name, phone, address_line1, address_line2, city, state, pincode, is_default=0):
        conn, engine = self.get_connection()
        cursor = conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        try:
            cursor.execute(f"""
                INSERT INTO addresses (user_id, full_name, phone, address_line1, address_line2, city, state, pincode, is_default)
                VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
            """, (user_id, full_name, phone, address_line1, address_line2 or '', city, state, pincode, is_default))
            conn.commit()
            addr_id = cursor.lastrowid
            return addr_id
        finally:
            cursor.close()
            conn.close()

    def get_user_addresses(self, user_id):
        if not user_id:
            return []
        conn, engine = self.get_connection()
        cursor = conn.cursor(dictionary=True) if engine == 'mysql' else conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        cursor.execute(f"SELECT * FROM addresses WHERE user_id = {placeholder} ORDER BY is_default DESC, created_at DESC", (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [dict(r) for r in rows]

    # --- Order Operations ---
    def create_order(self, user_id, order_number, delivery_name, delivery_phone,
                     delivery_address, delivery_city, delivery_state, delivery_pincode,
                     subtotal, shipping_fee, discount, total_amount, payment_method,
                     payment_status, payment_id, order_status, items):
        conn, engine = self.get_connection()
        cursor = conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        items_json = json.dumps(items)
        try:
            cursor.execute(f"""
                INSERT INTO orders (
                    order_number, user_id, delivery_name, delivery_phone,
                    delivery_address, delivery_city, delivery_state, delivery_pincode,
                    subtotal, shipping_fee, discount, total_amount,
                    payment_method, payment_status, payment_id, order_status,
                    items_json
                ) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder},
                          {placeholder}, {placeholder}, {placeholder}, {placeholder},
                          {placeholder}, {placeholder}, {placeholder}, {placeholder},
                          {placeholder}, {placeholder}, {placeholder}, {placeholder},
                          {placeholder})
            """, (
                order_number, user_id, delivery_name, delivery_phone,
                delivery_address, delivery_city, delivery_state, delivery_pincode,
                float(subtotal), float(shipping_fee), float(discount), float(total_amount),
                payment_method, payment_status, payment_id, order_status,
                items_json
            ))
            conn.commit()
            order_id = cursor.lastrowid
            return order_id
        finally:
            cursor.close()
            conn.close()

    def get_order_by_number(self, order_number):
        conn, engine = self.get_connection()
        cursor = conn.cursor(dictionary=True) if engine == 'mysql' else conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        cursor.execute(f"SELECT * FROM orders WHERE order_number = {placeholder}", (order_number,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            return None
        data = dict(row)
        if isinstance(data.get('items_json'), str):
            try:
                data['items'] = json.loads(data['items_json'])
            except Exception:
                data['items'] = []
        return data

    def get_user_orders(self, user_id):
        if not user_id:
            return []
        conn, engine = self.get_connection()
        cursor = conn.cursor(dictionary=True) if engine == 'mysql' else conn.cursor()
        placeholder = "%s" if engine == 'mysql' else "?"
        cursor.execute(f"SELECT * FROM orders WHERE user_id = {placeholder} ORDER BY created_at DESC", (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        orders = []
        for r in rows:
            data = dict(r)
            if isinstance(data.get('items_json'), str):
                try:
                    data['items'] = json.loads(data['items_json'])
                except Exception:
                    data['items'] = []
            orders.append(data)
        return orders


db_manager = DatabaseManager()
