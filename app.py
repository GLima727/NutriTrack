from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for sessions

DATABASE = 'database/app.db'

# --- Database setup ---
def init_db():
    if not os.path.exists('database'):
        os.makedirs('database')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL
        )
    ''')
    
    # Create products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            price REAL NOT NULL,
            discounted_price REAL NOT NULL,
            image TEXT,
            location TEXT NOT NULL,
            supplier TEXT NOT NULL,
            target_user_type TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS user_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# --- Helper to query database ---
def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(query, args)
    rv = c.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    user_type = request.form['userType']

    existing_user = query_db('SELECT * FROM users WHERE username = ?', (username,), one=True)

    if existing_user:
        flash('Username already exists. Please choose another.', 'error')
        return redirect(url_for('home'))

    query_db('INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)',
             (username, password, user_type))
    flash('Registration successful! Please log in.', 'success')
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user_type = request.form['userType']

    user = query_db('SELECT * FROM users WHERE username = ? AND password = ? AND user_type = ?',
                    (username, password, user_type), one=True)

    if user:
        session['username'] = username
        session['user_type'] = user_type
        flash(f'Welcome {username}!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Login failed. Please check your credentials.', 'error')
        return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html', username=session['username'], user_type=session['user_type'])


@app.route('/products')
def products():
    if 'username' not in session:
        return redirect(url_for('home'))

    user_type = session['user_type']
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Find the user's ID
    c.execute('SELECT id FROM users WHERE username = ?', (session['username'],))
    user_id = c.fetchone()[0]

    # Find product IDs that this user already selected
    c.execute('SELECT product_id FROM user_products WHERE user_id = ?', (user_id,))
    selected_products = [row[0] for row in c.fetchall()]

    # Get products NOT selected yet, and matching user_type
    if selected_products:
        placeholders = ','.join(['?']*len(selected_products))
        query = f'''
            SELECT * FROM products
            WHERE id NOT IN ({placeholders})
            AND target_user_type = ?
        '''
        c.execute(query, (*selected_products, user_type))
    else:
        c.execute('SELECT * FROM products WHERE target_user_type = ?', (user_type,))
    
    products = c.fetchall()
    conn.close()
    if user_type == 'consumer':
        return render_template('products.html', products=products, username=session['username'], user_type=user_type)
    else:
        return render_template('products_org.html', products=products, username=session['username'], user_type=user_type)


@app.route('/select_product', methods=['POST'])
def select_product():
    if 'username' not in session:
        return redirect(url_for('home'))

    product_id = request.form['product_id']

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Find user ID
    c.execute('SELECT id FROM users WHERE username = ?', (session['username'],))
    user_id = c.fetchone()[0]

    # Insert into user_products
    c.execute('INSERT INTO user_products (user_id, product_id) VALUES (?, ?)', (user_id, product_id))
    
    conn.commit()
    conn.close()

    flash('Product selected successfully!', 'success')
    return redirect(url_for('products'))

@app.route('/deselect_product', methods=['POST'])
def deselect_product():
    if 'username' not in session:
        return redirect(url_for('home'))

    product_id = request.form['product_id']

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Find user ID
    c.execute('SELECT id FROM users WHERE username = ?', (session['username'],))
    user_id = c.fetchone()[0]

    # Delete the user-product link
    c.execute('DELETE FROM user_products WHERE user_id = ? AND product_id = ?', (user_id, product_id))
    
    conn.commit()
    conn.close()

    flash('Product deselected successfully!', 'success')
    return redirect(url_for('personal'))


@app.route('/personal')
def personal():
    if 'username' not in session:
        return redirect(url_for('home'))

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Find user ID
    c.execute('SELECT id FROM users WHERE username = ?', (session['username'],))
    user_id = c.fetchone()[0]

    # Join products that this user selected
    c.execute('''
        SELECT products.*
        FROM products
        JOIN user_products ON products.id = user_products.product_id
        WHERE user_products.user_id = ?
    ''', (user_id,))
    
    selected_products = c.fetchall()
    conn.close()

    return render_template('personal.html', products=selected_products, username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

# --- Start ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
