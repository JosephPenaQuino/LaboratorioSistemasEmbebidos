import pymysql
import settings
from dao.DAOUsuario import DAOUsuario

class DAOCart:
    def connect(self):
        host = settings.MYSQL_HOST
        user = settings.MYSQL_USER
        password = settings.MYSQL_PASSWORD 
        db = settings.MYSQL_DB 
        return pymysql.connect(host, user, password, db)

    def getUsers(self):
        con = DAOCart.connect(self)
        cur = con.cursor()
        try:
            cur.execute("SELECT id_usuario FROM cart")
            users = list(dict.fromkeys(cur.fetchall())) 
            if not users:
                return []
            db = DAOUsuario()
            return db.readUsingIdList(users)
            
        except Exception as e:
            print("Exception occured in DAOCart:{}".format(e))
            return
        finally:
            con.close()
