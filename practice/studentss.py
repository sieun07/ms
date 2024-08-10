import sqlite3

def create_table():
    connection = sqlite3.connect("studentss.db")
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS students
                   (id INTEGER PRIMARY KEY, name TEXT,
                   age INTEGER, major TEXT)''')
    
    connection.commit()
    connection.close()

create_table()

def insert_student(id, name, age, major):
    connection = sqlite3.connect("studentss.db")
    cusor = connection.cursor()

    cusor.execute('''INSERT INTO students (id, name, age, major)
                  VALUES (?, ?, ?, ?)''', (id, name, age, major),)
    
    connection.commit()
    connection.close()

#insert_student(1, 'kim', 20, "robotics")
#insert_student(4, 'lee', 25, "computer")

def query_students():
    connection = sqlite3.connect("studentss.db")
    cusor = connection.cursor()

    cusor.execute("SELECT * FROM students")
    rows = cusor.fetchall()
    
    connection.close()
    
    return rows



def update_student(student_id, name, age, major):
    connection = sqlite3.connect("studentss.db")
    cusor = connection.cursor()

    cusor.execute('''UPDATE students SET name = ?,
                  age = ?, major = ? WHERE id = ?''',
                  (name, age, major, student_id))
    
    connection.commit()
    connection.close()

update_student(4, "lee", 25, "computer enginnering")
print(query_students())