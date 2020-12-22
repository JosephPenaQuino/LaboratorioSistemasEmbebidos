
import pymysql
import settings

class DAOComponente:
    def connect(self):
        host = settings.MYSQL_HOST
        user = settings.MYSQL_USER
        password = settings.MYSQL_PASSWORD 
        db = settings.MYSQL_DB 
        return pymysql.connect(host, user, password, db)

    def read(self, componenteId):
        con = DAOComponente.connect(self)
        cur = con.cursor()
        try:
            cur.execute((   "SELECT * FROM componente "
                            "WHERE id=%s"), (componenteId))
            return cur.fetchall()
        except Exception as e:
            print("Exeception occured in DAOComponente:{}".format(e))
            return
        finally:
            con.close()
