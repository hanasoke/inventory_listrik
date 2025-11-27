from flask import Flask, request, jsonify
from database import init_database, get_db_connection
import sqlite3

app = Flask(__name__)

# Initialize database
init_database()

# Helper function to dict
def row_to_dict(row):
    return dict(row) if row else None

# ===== CATEGORIES ENDPOINTS =====
@app.route('/categories', methods=['GET'])
def get_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return jsonify([row_to_dict(cat) for cat in categories])

@app.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO categories (name, description) VALUES (?, ?)',
            (data['name'], data.get('description'))
        )
        conn.commit()
        category_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': category_id, 'message': 'Category created successfully'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Category name already exists'}), 400

# ===== PRODUCTS ENDPOINTS =====
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    query = '''
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id
    '''
    products = conn.execute(query).fetchall()
    conn.close()
    return jsonify([row_to_dict(prod) for prod in products])

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (name, brand, category_id, price, stock, min_stock, sku)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'], data['brand'], data['category_id'], 
            data['price'], data.get('stock', 0), data.get('min_stock', 5), 
            data['sku']
        ))
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': product_id, 'message': 'Product created successfully'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'SKU already exists'}), 400

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    query = '''
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE p.id = ?
    '''
    product = conn.execute(query, (product_id,)).fetchone()
    conn.close()
    if product:
        return jsonify(row_to_dict(product))
    return jsonify({'error': 'Product not found'}), 404

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build dynamic update query
    update_fields = []
    values = []
    for field in ['name', 'brand', 'category_id', 'price', 'stock', 'min_stock']:
        if field in data:
            update_fields.append(f"{field} = ?")
            values.append(data[field])
    
    if not update_fields:
        return jsonify({'error': 'No fields to update'}), 400
    
    values.append(product_id)
    query = f'UPDATE products SET {", ".join(update_fields)} WHERE id = ?'
    
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    
    if cursor.rowcount == 0:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({'message': 'Product updated successfully'})

# ===== STOCK MANAGEMENT =====
@app.route('/products/<int:product_id>/stock-in', methods=['POST'])
def stock_in(product_id):
    data = request.get_json()
    quantity = data.get('quantity', 0)
    supplier_id = data.get('supplier_id')
    notes = data.get('notes', '')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Update product stock
        cursor.execute('UPDATE products SET stock = stock + ? WHERE id = ?', (quantity, product_id))
        
        # Record transaction
        cursor.execute('''
            INSERT INTO transactions (product_id, type, quantity, supplier_id, notes)
            VALUES (?, 'IN', ?, ?, ?)
        ''', (product_id, quantity, supplier_id, notes))
        
        conn.commit()
        conn.close()
        return jsonify({'message': 'Stock increased successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/products/<int:product_id>/stock-out', methods=['POST'])
def stock_out(product_id):
    data = request.get_json()
    quantity = data.get('quantity', 0)
    notes = data.get('notes', '')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if enough stock
    product = cursor.execute('SELECT stock FROM products WHERE id = ?', (product_id,)).fetchone()
    if not product or product['stock'] < quantity:
        conn.close()
        return jsonify({'error': 'Insufficient stock'}), 400
    
    try:
        # Update product stock
        cursor.execute('UPDATE products SET stock = stock - ? WHERE id = ?', (quantity, product_id))
        
        # Record transaction
        cursor.execute('''
            INSERT INTO transactions (product_id, type, quantity, notes)
            VALUES (?, 'OUT', ?, ?)
        ''', (product_id, quantity, notes))
        
        conn.commit()
        conn.close()
        return jsonify({'message': 'Stock decreased successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

# ===== REPORTS =====
@app.route('/reports/low-stock', methods=['GET'])
def get_low_stock():
    conn = get_db_connection()
    query = '''
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE p.stock <= p.min_stock
    '''
    products = conn.execute(query).fetchall()
    conn.close()
    return jsonify([row_to_dict(prod) for prod in products])

@app.route('/reports/transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    query = '''
        SELECT t.*, p.name as product_name, s.name as supplier_name
        FROM transactions t
        LEFT JOIN products p ON t.product_id = p.id
        LEFT JOIN suppliers s ON t.supplier_id = s.id
        ORDER BY t.created_at DESC
    '''
    transactions = conn.execute(query).fetchall()
    conn.close()
    return jsonify([row_to_dict(trans) for trans in transactions])

if __name__ == '__main__':
    app.run(debug=True, port=5000)