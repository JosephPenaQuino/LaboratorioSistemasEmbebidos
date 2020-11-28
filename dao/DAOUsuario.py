import pymysql

class DAOUsuario:
    def __init__(self, localhost, user, password, database):
        self.localhost = localhost
        self.user = user
        self.password = password
        self.database = database
        self.table = "usuarios"

    def _connect(self):
        return pymysql.connect(self.localhost, self.user, self.password, self.database)
    
    def read(self, id):
        con  = self._connect()
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute('SELECT * FROM usuarios')
            else:
                sql = "SELECT * FROM %s WHERE id=%s ORDER BY nombre ASC"
                cursor.execute(sql, (self.table, id))
            return cursor.fetchall()
        except:
            return
        finally:
            con.close()

    def insert(self, data):
        con = self._connect()
        cursor = con.cursor()
        username = data['username']
        nombre = data['nombre']
        apellido = data['apellido']
        codigo = data['codigo']
        admin = data['admin']
        email = data['email']
        telefono = data['telefono']

        try:
#            sql = "INSERT INTO %s(username,nombre,apellido,codigo,admin,email,telefono) VALUES('%s','%s',%s,'%s',%s,'%s',%s)"
           # sql = sql, (self.table, username,nombre,apellido,codigo,admin,email,telefono)
 #           cursor.execute(sql, (self.table, username,nombre,apellido,codigo,admin,email,telefono))
            sql = f"INSERT INTO {self.table}(username, nombre, apellido, codigo, admin, email, telefono) VALUES('{username}','{nombre}','{apellido}',{codigo},{admin},'{email}',{telefono})"
            print(sql)
            cursor.execute(sql)
            con.commit()
            return True
        except Exception as e:
            print("Exeception occured:{}".format(e))
        #except:
         #   print("Error at inserting")
            con.rollback()
            return False
        finally:
            con.close()

    def update(self, id, data):
        con = self._connect()
        cursor = con.cursor()
        username = data['username']
        nombre = data['nombre']
        apellido = data['apellido']
        codigo = data['codigo']
        admin = data['admin']
        email = data['email']
        telefono = data['telefono']

        try:
            sql = "UPDATE %s SET nombre=%s, telefono=%s, email=%s, username=%s, apellido=%s, codigo=%s, admin=%s WHERE id=%s"
            cursor.execute(sql, (self.table, nombre, telefono, email, username, apellido, codigo, admin, id))
            con.commit()
            return True
        except Exception as e:
            print("Exeception occured:{}".format(e))
            con.rollback()
            return False
        finally:
            con.close()

    def delete(self, id):
        con = self._connect()
        cursor = con.cursor()
        try:
            sql = 'DELETE FROM %s WHERE id=%s'
            cursor.execute(sql, (self.table, id))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
