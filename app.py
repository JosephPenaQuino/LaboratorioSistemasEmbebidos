from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.datastructures import ImmutableDict
import settings

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
        user = request.form['usuario']
        password = int(request.form['contraseña'])
        print("Usuario: %s" % user)
        print("Contraseña: %s" % password)
        for x in range(len(data)):
            print ("data[%d][1]: %s" % (x, data[x][1]))
            print ("data[%d][2]: %s" % (x, data[x][2]))
            print(type(password))
            print(type(data[x][2]))
            if data[x][1] == user:
                print("Usuarios iguales")
                if data[x][2] == password:
                    print("Ingreso Exitoso")
                    if data[x][6]:
                        return render_template('lista-usuarios.html', usuarios = data)
                    else:
                        return render_template('equipos.html', equipos = dataEquipos)
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
        edad = request.form['edad']
        rol = request.form['rol']
        print(user,password,nom,apell,edad,rol)
        cur = mysql.connection.cursor()
        cur.execute('insert usuarios(username,password,nombre,apellido,edad,rol) values(%s,%s,%s,%s,%s,%s)',(user,password,nom,apell,edad,rol))
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
        edad = request.form['edad']
        rol = request.form['rol']
        cur = mysql.connection.cursor()
        cur.execute(""" update usuarios 
                        set username = %s,password = %s,nombre = %s,apellido = %s,edad = %s,rol = %s where id = %s """,(user,password,nom,apell,edad,rol,id))
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
        img = request.form['imagen']
        print(nom,desc,stock,img)
        cur = mysql.connection.cursor()
        cur.execute('insert componente(nombre,descripcion,stock,imagen) values(%s,%s,%s,%s)',(nom,desc,stock,img))
        mysql.connection.commit()
        flash('Usuario actualizado correctamente')
        return redirect(url_for('listadoEquipos'))
    return 'Usuario'

@app.route('/editEquipos/<id>')
def edit_equipos(id):
    cursor = mysql.connection.cursor()
    cursor.execute('select * from equipos where id = %s', {id})
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
        cur.execute(""" update equipos 
                        set nombre = %s,descripcion = %s,stock = %s,imagen = %s where id = %s """,(nom,desc,stock,img,id))
        mysql.connection.commit()
        flash('Contacto actualizado correctamente')
        return redirect(url_for('listadoEquipos'))


@app.route('/addToCart/<id>')
def addToCart(id):

    cur = mysql.connection.cursor()

    cur.execute("SELECT id FROM users WHERE username = '" + session['username'] + "'")
    id_usuario = cur.fetchone()[0]
    try:
        cur.execute("INSERT INTO cart (id_usuarios, id_componente) VALUES (?, ?)", (id_usuario, id))
        mysql.connection.commit()
        msg = "Added successfully"
    except:
        mysql.connection.rollback()
        msg = "Error occured"
    mysql.connection.close()
    return redirect(url_for('root'))

# @app.route("/cart")
# def cart():
#     if 'email' not in session:
#         return redirect(url_for('loginForm'))
#     loggedIn, firstName, noOfItems = getLoginDetails()
#     email = session['email']
#     with sqlite3.connect('database.db') as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT userId FROM users WHERE email = '" + email + "'")
#         userId = cur.fetchone()[0]
#         cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, kart WHERE products.productId = kart.productId AND kart.userId = " + str(userId))
#         products = cur.fetchall()
#     totalPrice = 0
#     for row in products:
#         totalPrice += row[2]
#     return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)
#
# @app.route("/removeFromCart")
# def removeFromCart():
#     if 'email' not in session:
#         return redirect(url_for('loginForm'))
#     email = session['email']
#     productId = int(request.args.get('productId'))
#     with sqlite3.connect('database.db') as conn:
#         cur = conn.cursor()
#         cur.execute("SELECT userId FROM users WHERE email = '" + email + "'")
#         userId = cur.fetchone()[0]
#         try:
#             cur.execute("DELETE FROM kart WHERE userId = " + str(userId) + " AND productId = " + str(productId))
#             conn.commit()
#             msg = "removed successfully"
#         except:
#             conn.rollback()
#             msg = "error occured"
#     conn.close()
#     return redirect(url_for('root'))

if __name__ == "__main__":
    app.run(port=4000, debug=True, use_reloader=True)
