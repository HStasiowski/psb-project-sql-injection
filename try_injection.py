import psycopg2

connection = psycopg2.connect(
    host="127.0.0.1",
    database="dellstore2",
    user="sqlinjection",
    password="3FS-DI"
)
with connection.cursor() as cursor:
    cursor.execute("SELECT username, password FROM customers;")
    print(cursor.fetchone())

username = "user1'; SELECT * FROM customers; --"

# Incorrect way: vulnerable to SQL Injection attack
with connection.cursor() as cursor:
    cursor.execute(f"SELECT firstname, lastname "
                   f"FROM customers WHERE username='{username}';")
    print(cursor.fetchone())

# Correct
with connection.cursor() as cursor:
    cursor.execute("SELECT firstname, lastname "
                   "FROM customers WHERE username=%(checked_username)s;",
                   {"checked_username": username})
    print(cursor.fetchone())
