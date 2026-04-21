from flask import Flask, render_template, request,redirect
from database import conectar
#--Crear App 

app = Flask(__name__)

#--Ruta de Inicio

@app.route('/')
def inicio():
    return render_template('index.html')
#--Ruta para Guardar Usuario

@app.route('/guardar_usuario', methods=['POST'])
def guardar_usuario():

    usuario = request.form['txtusuario']
    password = request.form['txtcontrasena']
    rolusu = request.form['txtrol']
    documento = request.form['txtdocumento']

     #-- Conectar a la base de datos
    con = conectar()
    cursor = con.cursor()

    #--Crear SQL
    sql = "INSERT INTO usuarios (usuario, password, rol, documento) VALUES (%s, %s, %s, %s)"
    values = (usuario, password, rolusu, documento)

    #--Ejecutar SQL
    cursor.execute(sql, values)
    con.commit()

    return redirect('/')

#--Guardar Empleado
@app.route('/guardar_empleado', methods=['POST'])
def guardar_empleado():

    nombre = request.form['txtnombre']
    apellido = request.form['txtapellido']
    documento = request.form['txtdocumento']
    cargo = request.form['txcargo']
    horasextras = request.form['txthorasextras']
    bonificacion = request.form['txtbonificacion']
    area = request.form['txtarea']

    con = conectar()
    cursor = con.cursor()

    sql = "INSERT INTO empleados (nombre, apellido, documento, cargo, horas_extras, bonificacion, area) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (nombre, apellido, documento, cargo, horasextras, bonificacion, area)
    
    cursor.execute(sql, values)
    con.commit()

if __name__ == '__main__':
    app.run(debug=True)