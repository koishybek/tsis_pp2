import psycopg2

DB_HOST="localhost"
DB_NAME="snake_game"
DB_USER="postgres"
DB_PASS="Sherlok123"
DB_PORT=5432

def get_connection():
    return psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)

def create_tables():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS "user" (id SERIAL PRIMARY KEY,username VARCHAR(100) UNIQUE NOT NULL);')
    cursor.execute('CREATE TABLE IF NOT EXISTS user_score (id SERIAL PRIMARY KEY,user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,level INTEGER NOT NULL,score INTEGER NOT NULL);')
    conn.commit()
    cursor.close()
    conn.close()

def get_or_create_user(username):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT id FROM "user" WHERE username=%s;',(username,))
    row=cursor.fetchone()
    if row is not None:
        user_id=row[0]
    else:
        cursor.execute('INSERT INTO "user" (username) VALUES (%s) RETURNING id;', (username,))
        user_id=cursor.fetchone()[0]
        conn.commit()
    cursor.close()
    conn.close()
    return user_id

def get_latest_user_score(user_id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT level,score FROM user_score WHERE user_id=%s ORDER BY id DESC LIMIT 1;',(user_id,))
    row=cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return (row[0],row[1])
    return (1,0)

def save_user_score(user_id,level,score):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('INSERT INTO user_score (user_id,level,score) VALUES (%s,%s,%s);',(user_id,level,score))
    conn.commit()
    cursor.close()
    conn.close()
