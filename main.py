from fastapi import FastAPI, HTTPException #HTTPException is used to handle or raise exception at fd
import psycopg2  #lib to connect to PostgreSQL database
from pydantic import BaseModel #to validate the data in dict (json)

app = FastAPI() #object of FastAPI class is created 

connection = psycopg2.connect(
    host = 'localhost',
    port = '5432',
    database = 'postgres',
    user = 'postgres',
    password = 'nikita'
)

cursor = connection.cursor()  #cursor object is created to execute SQL queries

class Student(BaseModel): #inheritance Student is child class of BaseModel class
    id: int 
    name: str 
    course: str

#Get all students from the database
@app.get('/students')  #API endpoint to get all students
def get_all_students(): 
    cursor.execute('select * from students')
    rows = cursor.fetchall()
    print(rows)  #[(101, 'sita', 'AI'), (102, 'Nikita', 'data analytics')]  
    
    #convert this list of tuples into list of dictionaries
    result = []
    for row in rows:
        result.append({
            'id': row[0],
            'name' : row[1],
            'course' : row[2]
        })
    return result  #sends result to browser

#get single student
@app.get('/students/{id}')  #path parameters are given in {} , id is a fastapi var
def get_single_student(id : int):
    #print(id, type(id)) #str coz its coming from db in json format
    
    try:
        cursor.execute('select * from students where id=%s', (id,))  #%s -string coz query is string id-col, (id)- variable  (id,)-tuple
        row = cursor.fetchone() #tuple
        return{
            'id' : row[0],
            'name' : row[1],
            'course': row[2]
        }
    except:
        raise HTTPException(status_code=404, detail='Invalid student ID')
        
    
# Create Student Record
@app.post('/students')
def create_student_record(student : Student): #validate json using type hinting but the data is not validated its done using class based validation
    #student is object of Student class, attributes of student id name course
    
    print(student.id)
    print(student.name)
    print(student.course)
    
    try:
        cursor.execute('insert into students values (%s, %s, %s)', (student.id, student.name, student.course))
        connection.commit() #to save in a db
        raise HTTPException(status_code=201, detail='Student record created successfully')
    except psycopg2.IntegrityError:
        connection.rollback()
        raise HTTPException(status_code=404, detail='Student ID already exists')
        
