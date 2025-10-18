import os
import sqlite3
from utils.python_utils import print_table



db_path = os.path.join(os.path.dirname(__file__), 'data.db')
db = sqlite3.connect(db_path)

c = db.cursor()

# Создать новую таблицу
c.execute('''
    CREATE TABLE IF NOT EXISTS accounts(
        id INTEGER PRIMARY KEY,
        nickname TEXT,
        password INTEGER
    )
''')

# Вставить данные
c.execute('''
    INSERT INTO users (name, age) VALUES
    ('Alice', 3453245),
    ('Bob', 32456),
    ('Charlie', 24352453)
''')

# Удалить данные
c.execute('DELETE FROM users WHERE id > ?', ('3',))

# Oбновить данные
c.execute('UPDATE users SET age = ? WHERE name = ?', (28, 'Alice'))


c.execute('SELECT * FROM users')
print_table(c.fetchall())

db.commit()
db.close()