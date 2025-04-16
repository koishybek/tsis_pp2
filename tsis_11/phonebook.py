import psycopg2
import csv

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="TaikpanovRus12",
    host="localhost",
    port="1501"
)
cur = conn.cursor()

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PhoneBook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100),
            phone VARCHAR(15)
        );
    """)
    conn.commit()

def insert_user(username, phone):
    cur.execute("INSERT INTO PhoneBook (username, phone) VALUES (%s, %s);", (username, phone))
    conn.commit()

def update_user(old_username=None, old_phone=None, new_username=None, new_phone=None):
    if old_username:
        if new_username:
            cur.execute("UPDATE PhoneBook SET username = %s WHERE username = %s;", (new_username, old_username))
        if new_phone:
            cur.execute("UPDATE PhoneBook SET phone = %s WHERE username = %s;", (new_phone, old_username))
    elif old_phone:
        if new_username:
            cur.execute("UPDATE PhoneBook SET username = %s WHERE phone = %s;", (new_username, old_phone))
        if new_phone:
            cur.execute("UPDATE PhoneBook SET phone = %s WHERE phone = %s;", (new_phone, old_phone))
    conn.commit()

def query_data(filter_by=None, value=None):
    if filter_by == 'username':
        cur.execute("SELECT * FROM PhoneBook WHERE username = %s;", (value,))
    elif filter_by == 'phone':
        cur.execute("SELECT * FROM PhoneBook WHERE phone = %s;", (value,))
    else:
        cur.execute("SELECT * FROM PhoneBook;")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def delete_user(username=None, phone=None):
    if username:
        cur.execute("DELETE FROM PhoneBook WHERE username = %s;", (username,))
    elif phone:
        cur.execute("DELETE FROM PhoneBook WHERE phone = %s;", (phone,))
    conn.commit()

def query_by_pattern(pattern):
    cur.execute("SELECT * FROM PhoneBook WHERE username LIKE %s OR phone LIKE %s;", (f"%{pattern}%", f"%{pattern}%"))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def insert_or_update_user(username, phone):
    cur.execute("SELECT * FROM PhoneBook WHERE username = %s;", (username,))
    if cur.fetchone():
        cur.execute("UPDATE PhoneBook SET phone = %s WHERE username = %s;", (phone, username))
    else:
        cur.execute("INSERT INTO PhoneBook (username, phone) VALUES (%s, %s);", (username, phone))
    conn.commit()

def insert_multiple_users(users):
    incorrect_data = []
    for username, phone in users:
        if not phone.isdigit() or len(phone) != 11:
            incorrect_data.append((username, phone))
        else:
            cur.execute("INSERT INTO PhoneBook (username, phone) VALUES (%s, %s);", (username, phone))
    conn.commit()
    if incorrect_data:
        print("Некорректные данные:")
        for data in incorrect_data:
            print(data)
    return incorrect_data

def query_with_pagination(limit, offset):
    cur.execute("SELECT * FROM PhoneBook LIMIT %s OFFSET %s;", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def close():
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_table()

    insert_user("Alice", "12345678901")
    insert_user("Bob", "98765432101")
    insert_user("Ruslan", "87011014548")
    insert_user("Aliya", "43647527645")
    insert_user("Marya", "83463270000")

    update_user(old_username="Alice", new_phone="11111111111")

    print("Записи по шаблону 'Bob':")
    query_by_pattern('Bob')

    insert_or_update_user("Charlie", "55555555555")

    users = [("David", "12345678901"), ("Eve", "wrongphone"), ("Frank", "98765432101")]
    insert_multiple_users(users)

    print("Записи с пагинацией (limit=2, offset=0):")
    query_with_pagination(2, 0)

    delete_user(username="Bob")
    delete_user(phone="98765432101")

    print("После удаления:")
    query_data()

    close()
