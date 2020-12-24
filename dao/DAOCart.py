import pymysql
import settings
from dao.DAOUsuario import DAOUsuario
from dao.DAOComponente import DAOComponente


class DAOCart:
    def connect(self):
        host = settings.MYSQL_HOST
        user = settings.MYSQL_USER
        password = settings.MYSQL_PASSWORD 
        db = settings.MYSQL_DB 
        return pymysql.connect(host, user, password, db)

    def getUsers(self):
        print("asdfasd")
        con = DAOCart.connect(self)
        cur = con.cursor()
        print("connected")
        try:
            cur.execute("SELECT id_usuario FROM cart")
            data = cur.fetchall()
            print(data)
            users = list(dict.fromkeys(data)) 
            print(users[0][0])
            if not users:
                print( "There are not users")
                return []
            db = DAOUsuario()
            return db.readUsingIdList(users[0])
            
        except Exception as e:
            print("Exception occured in DAOCart:{}".format(e))
            return
        finally:
            con.close()

    def getComponentesFromUser(self, userId):
        con = DAOCart.connect(self)
        cur = con.cursor()
        try:
            cur.execute("SELECT id_componente FROM cart where id_usuario=%s", (userId))
            data = cur.fetchall()
            dataParsed = []
            for d in data:
                dataParsed.append(d[0])
            db = DAOComponente()
            return db.readUsingIdList(dataParsed)
            
        except Exception as e:
            print("Exception occured in DAOCart:{}".format(e))
            return
        finally:
            con.close()
