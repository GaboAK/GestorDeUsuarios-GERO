import mysql.connector

def conectar():
        #--Conexión a la base de datos
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='company'
    )
    if conn.is_connected():
        print('___Conexión exitosa a la base de datos___')
    return conn
conectar()