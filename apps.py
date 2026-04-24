from flask import Flask, render_template, request, redirect, flash, session, url_for
from database import conectar

apps = Flask(__name__)

apps.secret_key = "123456789"


# --Login
@apps.route('/')
def mostrar_login():
    return render_template("login.html")


#--Index
@apps.route('/index')
def index():
    if 'usuario' not in session:
        return redirect(url_for('mostrar_login'))
    
    con = conectar()
    cursor = con.cursor()

    sql = "SELECT * FROM usuarios"
    cursor.execute(sql)
    lista = cursor.fetchall()

    sql = "SELECT * FROM empleados"
    cursor.execute(sql)
    empleados = cursor.fetchall()

    return render_template("index.html", usuario=session['usuario'], lista=lista, empleados=empleados)

#--Index Empleado

@apps.route('/indexpleado')
def indexpleado():
    if 'usuario' not in session:
        return redirect(url_for('mostrar_login'))
    
    con = conectar()
    cursor = con.cursor()

    sql = "SELECT * FROM usuarios"
    cursor.execute(sql)
    lista = cursor.fetchall()

    sql = "SELECT * FROM empleados"
    cursor.execute(sql)
    empleados = cursor.fetchall()

    return render_template("AccessEmple.html", usuario=session['usuario'], lista=lista, empleados=empleados)
#--
@apps.route('/login', methods=["POST"])
def login_form():

    user = request.form['txtusuario']
    password = request.form['txtcontrasena']

    con = conectar()
    cursor = con.cursor()

    sql = "SELECT * FROM usuarios WHERE usuario = %s AND password = %s"
    cursor.execute(sql, (user, password))

    resultado = cursor.fetchone()

    if resultado:
        rol = resultado[3]

        # -- Guardar información del usuario en sesión
        session['usuario'] = user
        session['rol'] = rol

        if rol == "administrador":
            return redirect(url_for('index'))
        else:
            return redirect(url_for('indexpleado'))
    else:
        flash("Usuario/Contraseña Incorrectos", "danger")
        return redirect(url_for('mostrar_login'))

#--Logout
@apps.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('mostrar_login'))


# --Guardar usuario
@apps.route('/guardar_usuario', methods=['POST'])
def guardar_usuario():
    if 'usuario' not in session:
        return redirect(url_for('mostrar_login'))

    usuario = request.form['txtusuario']
    password = request.form['txtcontrasena']
    rolusu = request.form['txtrol']
    documento = request.form['txtdocumento']

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE documento = %s", (documento,))
    existente = cursor.fetchone()

    if existente:
        flash("Usuario Con Documento Existente", "warning")
    else:
        sql = "INSERT INTO usuarios (usuario, password, rol, documento) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (usuario, password, rolusu, documento))
        con.commit()
        flash("Usuario Registrado", "success")

    return redirect(url_for('index'))

#--Eliminar usuario
@apps.route('/eliminar/<int:id>')
def eliminarusu(id):
    if 'usuario' not in session:
        return redirect(url_for('mostrar_login'))

    con = conectar()
    cursor = con.cursor()

    #--Buscar Usuario
    sql = "SELECT rol FROM usuarios WHERE id_usu = %s"
    cursor.execute(sql, (id,))
    usuario = cursor.fetchone()

    #--Validar Rol
    if usuario:
        rol = usuario[0]
        if rol == 'admin':
            flash("No Se Puede Eliminar un Administrador", "danger")
        else:
            cursor.execute("DELETE FROM usuarios WHERE id_usu = %s", (id,))
            con.commit()
            flash("Usuario Eliminado", "success")

    cursor.close()
    con.close()
    return redirect(url_for('index'))

# --Guardar empleado
@apps.route('/guardar_empleado', methods=['POST'])
def guardar_empleado():

    nombre = request.form['txtnombre']
    apellido = request.form['txtapellido']
    documento = request.form['txtdocumento']
    cargo = request.form['txcargo']
    horasextras = int(request.form['txthorasextras'])
    bonificacion = float(request.form['txtbonificacion'])
    id_dep = request.form['txtarea']

    #--Salario
    if cargo.lower() == "gerente":
        salariobase = 5000000
    elif cargo.lower() == "administrador":
        salariobase = 3500000
    elif cargo.lower() == "contador":
        salariobase = 2800000
    else:
        salariobase = 1800000

    totalextras = horasextras * 3000
    salariobru = salariobase + totalextras + bonificacion
    salud = salariobru * 0.04
    pension = salariobru * 0.04
    salarioneto = salariobru - salud - pension


    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM empleados WHERE documento = %s", (documento,))
    existente = cursor.fetchone()

    if existente:
        flash("Empleado Con Documento Existente", "warning")
    else:
        cursor.execute("""INSERT INTO empleados (documento, nombre, apellido, cargo, salariobase, horasextras, bonificacion, salud, pension, salarioneto, id_dep)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (documento, nombre, apellido, cargo, salariobase, horasextras, bonificacion, int(salud), int(pension), int(salarioneto), id_dep))

        con.commit()
        flash("Empleado Registrado", "success")

    return redirect(url_for('index'))

#--Eliminar empleado

@apps.route('/eliminaremple/<int:id>')
def eliminaremple(id):
    con = conectar()
    cursor = con.cursor()
    
    cursor.execute("SELECT documento FROM empleados WHERE id = %s", (id,))
    empleado = cursor.fetchone()
    if empleado:
        documento = empleado[0]
    
    
        cursor.execute("DELETE FROM empleados WHERE id = %s", (id,))
        cursor.execute("DELETE FROM usuarios WHERE documento = %s", (documento,))
        con.commit()
        flash("Empleado Eliminado", "success")
        
    cursor.close()
    con.close()
    return redirect(url_for("index"))


#--Editar usuario

@apps.route('/editarusu/<int:id>')
def editarusu(id):

    if 'usuario' not in session:
        return redirect(url_for('mostrar_login'))
    
    con = conectar()
    cursor = con.cursor()

    sql1 = "SELECT * FROM usuarios WHERE id_usu = %s"
    cursor.execute(sql1, (id,))
    usuario = cursor.fetchone()

    cursor.close()
    con.close()

    return render_template("editarusuario.html", usu=usuario)

#-- Editar Empleado Por el Usuario

#--Actualizar Form
@apps.route('/actualizar_usuarios', methods=['POST'])
def actualizar_usuarios():

    id = request.form['id']
    usuario = request.form['txtusuario']
    password = request.form['txtpassword']

    con = conectar()
    cursor = con.cursor()

    sqla = "UPDATE usuarios SET usuario=%s, password=%s WHERE id_usu=%s"
    cursor.execute(sqla, (usuario, password, id))
    con.commit()

    cursor.close()
    con.close()

    flash("Usuario Actualizado", "success")
    return redirect(url_for('index'))

#--Editar empleado

@apps.route('/editaremple/<int:id>')
def editaremple(id):

    if 'usuario' not in session:
        return redirect(url_for('mostrar_login'))

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM empleados WHERE id = %s", (id,))
    empleado = cursor.fetchone()

    cursor.close()
    con.close()

    return render_template("editarempleado.html", emp=empleado)

#--Actualizar la información del formulario
@apps.route('/actualizar_empleado', methods=['POST'])
def actualizar_empleados():

    id = request.form['id']
    nombre = request.form['txtnombre']
    apellido = request.form['txtapellido']
    cargo = request.form['txtcargo']
    horasextras = int(request.form['txthorasextras'])
    bonificacion = float(request.form['txtbonificacion'])
    id_dep = request.form['txtid_dep']

    #-- Pal Salario
    if cargo.lower() == "gerente":
        salariobase = 5000000
    elif cargo.lower() == "administrador":
        salariobase = 3500000
    elif cargo.lower() == "contador":
        salariobase = 2800000
    else:
        salariobase = 1800000


    totalextras = horasextras * 3000
    salariobru = salariobase + totalextras + bonificacion
    salud = salariobru * 0.04
    pension = salariobru * 0.04
    salarioneto = salariobru - salud - pension


    con = conectar()
    cursor = con.cursor()

    sqle = "UPDATE empleados SET nombre=%s, apellido=%s, cargo=%s, horasextras=%s, bonificacion=%s, id_dep=%s, salarioneto=%s WHERE id=%s"
    cursor.execute(sqle, (nombre, apellido, cargo, horasextras, bonificacion, id_dep, salarioneto, id))
    con.commit()

    cursor.close()
    con.close()

    flash("Empleado Actualizado", "success")
    return redirect(url_for('index'))
    
#______________________________________________________________________

@apps.route('/editemplefrom/<int:id>')
def editemplefrom(id):

    if 'usuario' not in session:
        return redirect(url_for('mostrar_login'))

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM empleados WHERE id = %s", (id,))
    empleado = cursor.fetchone()

    cursor.close()
    con.close()

    return render_template("EditUserEmple.html", emp=empleado)

#--Actualizar la información del formulario
@apps.route('/update_emple', methods=['POST'])
def update_emple():

    id = request.form['id']
    nombre = request.form['txtnombre']
    apellido = request.form['txtapellido']
    cargo = request.form['txtcargo']
    id_dep = request.form['txtid_dep']

    con = conectar()
    cursor = con.cursor()

    sqle = "UPDATE empleados SET nombre=%s, apellido=%s, cargo=%s, id_dep=%s WHERE id=%s"
    cursor.execute(sqle, (nombre, apellido, cargo, id_dep, id))
    con.commit()

    cursor.close()
    con.close()

    flash("Empleado Actualizado", "success")
    return redirect(url_for('indexpleado'))
    


if __name__ == '__main__':
    apps.run(debug=True)
