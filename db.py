import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT,
            symbol TEXT,
            side TEXT,
            amount REAL,
            price REAL,
            strategy TEXT,
            sl REAL,
            tp REAL,
            timestamp DATETIME
        )
    ''')
    conn.commit()

def log_order(order, strategy, sl=None, tp=None):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order['id'],
        order['symbol'],
        order['side'],
        order['amount'],
        order.get('price'),
        strategy,
        sl,
        tp,
        datetime.now()
    ))
    conn.commit()
