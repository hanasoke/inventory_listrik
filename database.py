import sqlite3
from datetime import datetime

def init_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Tabel Kategori
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')
    
    # Tabel Products
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT,
            category_id INTEGER,
            price DECIMAL(10,2),
            stock INTEGER DEFAULT 0,
            min_stock INTEGER DEFAULT 5,
            sku TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')
    
    # Tabel Suppliers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT,
            phone TEXT,
            email TEXT
        )
    ''')
    
    # Tabel Transactions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            type TEXT CHECK(type IN ('IN', 'OUT')),
            quantity INTEGER,
            supplier_id INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id),
            FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
        )
    ''')
    
    # Insert sample data
    sample_categories = [
        ('Kabel', 'Berbagai jenis kabel listrik'),
        ('Saklar', 'Saklar dan stop kontak'),
        ('Lampu', 'Berbagai jenis lampu'),
        ('Perlengkapan Instalasi', 'Alat instalasi listrik')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)', sample_categories)
    
    sample_products = [
        ('Kabel NYY 2x2.5', 'Supercable', 1, 25000, 50, 10, 'KBL-NYY-2x2.5'),
        ('Saklar Tunggal', 'Broco', 2, 15000, 30, 5, 'SKL-TUNGGAL-01'),
        ('Lampu LED 18W', 'Philips', 3, 45000, 20, 5, 'LMP-LED-18W'),
        ('MCB 10A', 'Schneider', 4, 80000, 15, 3, 'MCB-10A-SCH')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO products (name, brand, category_id, price, stock, min_stock, sku) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sample_products)
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn