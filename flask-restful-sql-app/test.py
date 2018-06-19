import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
# use cursor to execute commands
cursor.execute(create_table)

user = (1, 'jose', 'asdf')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

#insert many users at once
users = [
    (2, 'rolf', 'asdf'),
    (3, 'anne', 'xyz')
]
cursor.executemany(insert_query, users)

#select query to just see if its in the database
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
#good practise to close the connection
connection.close()