from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.datastructures import ImmutableDict
import settings
from dao.DAOPrestamo import DAOPrestamo

app = Flask(__name__)

#mysql database
app.config['MYSQL_HOST'] = settings.MYSQL_HOST
app.config['MYSQL_USER'] = settings.MYSQL_USER
app.config['MYSQL_PASSWORD'] = settings.MYSQL_PASSWORD 
app.config['MYSQL_DB'] = settings.MYSQL_DB 

mysql = MySQL(app)

app.secret_key='mysecretkey'


#################### USUARIOS ###############################
@app.route('/')
def index():
    cursor =  mysql.connection.cursor()
    cursor.execute('select * from usuarios')
    data = cursor.fetchall()
    return render_template('index.html',contactos=data)
    #return 'Index - Diseño de software'

@app.route('/inicio')
def inicio():
    cursor =  mysql.connection.cursor()
    cursor.execute('select * from componente')
    data = cursor.fetchall()
    return render_template('equipos.html',equipos = data)
    #return 'Index - Diseño de software'
    

@app.route('/portal', methods=['POST'])
def acceso():
    cursor =  mysql.connection.cursor()
    cursor.execute('select * from usuarios')
    data = cursor.fetchall()

    cursorEquipos =  mysql.connection.cursor()
    cursorEquipos.execute('select * from componente')
    dataEquipos = cursorEquipos.fetchall()

    if request.method == 'POST':
        session['username'] = request.form['usuario']
        username = session['username']
        password = int(request.form['contraseña'])
        print("Usuario: %s" % username)
        print("Contraseña: %s" % password)
        for x in range(len(data)):
            print ("data[%d][1]: %s" % (x, data[x][1]))
            print ("data[%d][2]: %s" % (x, data[x][2]))
            print(type(password))
            print(type(data[x][2]))
            if data[x][1] == username:
                print("Usuarios iguales")
                if data[x][2] == password:
                    print("Ingreso Exitoso")
                    if data[x][6]:
                        return render_template('lista-usuarios.html', usuarios = data)
                    else:
                        print("User Id: {}".format(data[x][0]))
                        return render_template('equipos.html', userId=data[x][0], equipos=dataEquipos,usuario = session['username'])
                else:
                    print("Contraseña Incorrecta")
            else:
                print("Usuario no existe")
        return redirect(url_for('index'))


@app.route('/usuarios')
def usuarios():
    cursor =  mysql.connection.cursor()
    cursor.execute('select * from usuarios')
    data = cursor.fetchall()
    return render_template('lista-usuarios.html',usuarios = data)
    #return 'Index - Diseño de software'

@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    if request.method == 'POST':
        user = request.form['usuario']
        password = request.form['contraseña']
        nom = request.form['nombre']
        apell = request.form['apellido']
        telefono = request.form['telefono']
        admin = 1
        if request.form['rol'] == "estudiante":
           admin = 0 
        email = f'{user}@utec.edu.pe'
        print(user,password,nom,apell,admin)
        cur = mysql.connection.cursor()
        cur.execute('insert usuarios('
                    'username,codigo,'
                    'nombre,apellido,'
                    'admin,email, telefono) '
                    'values(%s,%s,%s,%s,%s,'
                    '%s,%s)',(user,password,nom,
                    apell,admin, email, telefono))


        mysql.connection.commit()
        flash('Usuario actualizado correctamente')
        return redirect(url_for('usuarios'))
    return 'Usuario'

@app.route('/editUser/<id>')
def edit_usuario(id):
    cursor = mysql.connection.cursor()
    cursor.execute('select * from usuarios where id = %s', {id})
    data = cursor.fetchall()
    return render_template('editUsuarios.html', usuario=data[0])

@app.route('/deleteUser/<id>')
def delete_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from usuarios where id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto actualizado correctamente')
    return redirect(url_for('usuarios'))

@app.route('/updateUsuario/<id>', methods=['POST'])
def update_usuario(id):
    if request.method == 'POST':
        user = request.form['usuario']
        password = request.form['contraseña']
        nom = request.form['nombre']
        apell = request.form['apellido']
        telefono = request.form['telefono']
        admin = request.form['rol']
        cur = mysql.connection.cursor()
        cur.execute((" update usuarios" 
                    "set username = %s,"
                    "codigo = %s,"
                    "nombre = %s,"
                    "apellido = %s,"
                    "telefono = %s,"
                    "admin = %s"
                    " where id = %s ")
                    ,(user, password, nom, apell, telefono, admin, id))
        mysql.connection.commit()
        flash('Contacto actualizado correctamente')
        return redirect(url_for('usuarios'))




@app.route('/lista-equipos')
def listadoEquipos():
    cursor =  mysql.connection.cursor()
    cursor.execute('select * from componente')
    data = cursor.fetchall()
    return render_template('lista-equipos.html',equipos = data)
    #return 'Index - Diseño de software'

@app.route('/add_equipo', methods=['POST'])
def add_equipo():
    if request.method == 'POST':
        nom = request.form['nombre']
        desc = request.form['descripcion']
        stock = request.form['stock']
        total = stock
        img = request.form['imagen']
        print(nom,desc,stock,img)
        cur = mysql.connection.cursor()
        cur.execute('insert componente(nombre,description,stock,image_url, total)'
                    'values(%s,%s,%s,%s,%s)',(nom,desc,stock,img,total))
        mysql.connection.commit()
        flash('Usuario actualizado correctamente')
        return redirect(url_for('listadoEquipos'))
    return 'Usuario'

@app.route('/editEquipos/<id>')
def edit_equipos(id):
    cursor = mysql.connection.cursor()
    cursor.execute('select * from componente where id = %s', {id})
    data = cursor.fetchall()
    return render_template('editEquipos.html', equipos=data[0])

@app.route('/deleteEquipos/<id>')
def delete_equipo(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from equipos where id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto actualizado correctamente')
    return redirect(url_for('listadoEquipos'))

@app.route('/updateEquipo/<id>', methods=['POST'])
def update_equipos(id):
    if request.method == 'POST':
        nom = request.form['nombre']
        desc = request.form['descripcion']
        stock = request.form['stock']
        img = request.form['imagen']
        cur = mysql.connection.cursor()
        cur.execute((" update componente "
                    "set nombre = %s,"
                    "description = %s,"
                    "stock = %s,"
                    "image_url = %s "
                    "where id = %s "),(nom,desc,stock,img,id))
        mysql.connection.commit()
        flash('Contacto actualizado correctamente')
        return redirect(url_for('listadoEquipos'))


@app.route('/addToCart')
def addToCart():
    id_componente = int(request.args.get('productId'))
    cur = mysql.connection.cursor()
    print(id_componente)
    cur.execute("SELECT id FROM usuarios WHERE username = '" + session['username'] + "'")
    id_usuario = cur.fetchone()[0]
    print(id_usuario)

    try:
        cur.execute("INSERT INTO cart (id_usuario, id_componente) VALUES (%s, %s)", (str(id_usuario), str(id_componente)))
        mysql.connection.commit()
        msg = "Added successfully"
    except:
        mysql.connection.rollback()
        msg = "Error occured"
    mysql.connection.close()
    return redirect(url_for('inicio'))

@app.route("/cart")
def cart():

    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM usuarios WHERE username = '" + session['username'] + "'")
    userId = cur.fetchone()[0]
    cur.execute("SELECT componente.id, componente.nombre, componente.stock, componente.image_url FROM componente, cart WHERE componente.id = cart.id_componente AND cart.id_usuario = " + str(userId))
    products = cur.fetchall()

    return render_template("cart.html", products = products, usuario = session['username'])

@app.route("/removeFromCart")
def removeFromCart():

    productId = int(request.args.get('productId'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM usuarios WHERE username = '" + session['username'] +  "'")
    userId = cur.fetchone()[0]
    try:
        cur.execute("DELETE FROM cart WHERE id_usuario = " + str(userId) + " AND id_componente = " + str(productId))
        mysql.connection.commit()
        msg = "removed successfully"
    except:
        mysql.connection.rollback()
        msg = "error occured"
    mysql.connection.close()
    return redirect(url_for('inicio'))


@app.route("/checkout", methods=['GET', 'POST'])
def payment():

    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM usuarios WHERE username = '" + session['username'] + "'")
    userId = cur.fetchone()[0]
    cur.execute(
        "SELECT componente.id, componente.nombre, componente.stock, componente.image_url FROM componente, cart WHERE componente.id = cart.id_componente AND cart.id_usuario = " + str(
            userId))
    products = cur.fetchall()

    cur.execute("DELETE FROM cart WHERE id = " + str(userId))
    mysql.connection.commit()

    return render_template("checkout.html", products=products,usuario = session['username'])


@app.route('/usuarioListaPrestamos/<userId>')
def usuario_lista_prestamos(userId):
    db = DAOPrestamo()
    data = db.read(userId)
    print("======================================")
    print("Data: ")
    print(data)
    return render_template('usuarioListaPrestamos.html', prestamo_componente=data)

@app.route('/devolverComponente/<prestamoId>')
def devolverComponente(prestamoId):
    db = DAOPrestamo()
    db.returnComponent(prestamoId)
    userId = db.getUserId(prestamoId)
    #data = db.read(userId)
    #return render_template('usuarioListaPrestamos.html', prestamo_componente=data)
    return usuario_lista_prestamos(userId)

@app.route('/lista-porConfirmar')
def admin_lista_prestamosConfirmar():
    db = DAOPrestamo()
    data = db.getPrestamosPorConfirmar()
    return render_template('listaPorConfirmar.html', prestamo_por_confirmar=data)

@app.route('/confirmarDevolucion/<prestamoId>')
def confirmar_devolucion(prestamoId):
    db = DAOPrestamo()
    db.confirmarDevolucion(prestamoId)
    data = db.getPrestamosPorConfirmar()
    return render_template('listaPorConfirmar.html', prestamo_por_confirmar=data)

@app.route('/negarDevolucion/<prestamoId>')
def negar_devolucion(prestamoId):
    db = DAOPrestamo()
    db.negarDevolucion(prestamoId)
    data = db.getPrestamosPorConfirmar()
    return render_template('listaPorConfirmar.html', prestamo_por_confirmar=data)

if __name__ == "__main__":
    app.run(port=4000, debug=True, use_reloader=True)
