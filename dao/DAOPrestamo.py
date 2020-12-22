import pymysql
import settings

class DAOPrestamo:
    def connect(self):
        host = settings.MYSQL_HOST
        user = settings.MYSQL_USER
        password = settings.MYSQL_PASSWORD 
        db = settings.MYSQL_DB 
        return pymysql.connect(host, user, password, db)

    def read(self, userId):
        con = DAOPrestamo.connect(self)
        cur = con.cursor()
        try:
            cur.execute((   "SELECT * FROM prestamo "
                            "WHERE id_usuario=%s, "
                            "Finalizado=0"), (userId))
            data = cur.fetchall()
            print(data)
        except:
            return
        finally:
            con.close()
