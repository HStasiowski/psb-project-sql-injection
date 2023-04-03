import sqlite3

# Connect to the database
conn = sqlite3.connect('connections.db')
cursor = conn.cursor()

# Create the "USER" table
cursor.execute('''drop table if exists  user;''')
cursor.execute('''
    
    CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);
         ''')
print("Table created successfully")

# # Create the trigger that updates another table
# cursor.execute('''
#     CREATE TRIGGER IF NOT EXISTS update_table_trigger
#     AFTER INSERT ON USER
#     BEGIN
#         UPDATE USER SET ID = ID + 1;
#     END;
# ''')
# print("Trigger created successfully")

# Close the database connection
conn.close()