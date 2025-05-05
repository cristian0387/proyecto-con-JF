import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_USER =os.environ["MYSQL_USER"]
MYSQL_PASSWORD =os.environ["MYSQL_PASSWORD"]
MYSQL_HOST =os.environ["MYSQL_HOST"]
MYSQL_PORT =os.environ["MYSQL_PORT"]

class connectDB:
    def __init__(self):
        self.connection= None
        self.connect() 
          
    def connect(self):
        if not self.connection or not self.connection.open:
           try:
               self.connection= pymysql.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PASSWORD, port=int(MYSQL_PORT),database="acusadoacusador")
               
               print("conexion exitosa a MYSQL")
           except Exception as e:
               print("Error enla conexion{e}")
        return self.connection
    
    def close_connetion(self):
        if  self.connection or self.connection.open:
            self.connection.close()
            print("conecion cerrada")
            
            
            
db_conn=connectDB()  

def get_db_connetion():
    return db_conn.connect()      
           

