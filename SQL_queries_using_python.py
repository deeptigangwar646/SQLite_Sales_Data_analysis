import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL
    )
''')

sales_data = [
    ('Product A', 5, 100),
    ('Product B', 3, 200),
    ('Product C', 8, 150),
    ('Product A', 2, 100),
    ('Product B', 4, 200),
]
cursor.executemany('INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)', sales_data)
conn.commit()

query = '''
    SELECT product,
           SUM(quantity) AS total_qty,
           SUM(quantity * price) AS revenue
    FROM sales
    GROUP BY product
'''
df = pd.read_sql_query(query, conn)
conn.close()

print(df)
df.plot(kind='bar', x='product', y='revenue', legend=False)
plt.ylabel('Revenue')
plt.title('Revenue by Product')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.savefig('sales_chart.png')
