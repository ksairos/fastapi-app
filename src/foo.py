from psycopg_pool import ConnectionPool

DATABASE_URL = "host=localhost port=5433 dbname=fastapi user=ksairos password=1298"

try:
    pool = ConnectionPool(conninfo=DATABASE_URL)
    print(pool.conninfo)
    print("connected")
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            posts = cursor.execute("SELECT * FROM posts").fetchall()
    print({"posts": posts})
except Exception as e:
    print("Error connecting to database")
    print(e)