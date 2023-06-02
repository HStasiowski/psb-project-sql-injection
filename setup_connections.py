import sqlite3

# Connect to the database
conn = sqlite3.connect("psb_project/connections-db/connections.db")
cursor = conn.cursor()

# Open and read SQL script
with open("psb_project/connections-db/setup_connections.sql", "r") as sql_file:
    sql_script = sql_file.read()

# Execute SQL script
try:
    cursor.executescript(sql_script)
except Exception as e:
    print(f"Connections DB was not created: f{e}")
else:
    conn.commit()
    print("Connections DB created successfully")

# Close the database connection
conn.close()