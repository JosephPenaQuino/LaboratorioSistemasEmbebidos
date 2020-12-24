
import pymysql
import settings

class DAOComponente:
    def connect(self):
        host = settings.MYSQL_HOST
        user = settings.MYSQL_USER
        password = settings.MYSQL_PASSWORD 
        db = settings.MYSQL_DB 
        return pymysql.connect(host, user, password, db)

    def readUsingIdList(self, componentesId):
        print("==========================")
        con = DAOComponente.connect(self)
        cur = con.cursor()
        try:
            if not componentesId:
                return []
            sql = "SELECT * FROM componente WHERE "
            for componenteId in componentesId:
                sql = sql + "id=" + str(componenteId) + " OR "
            sql = sql[:-4]
            print(sql)
            cur.execute(sql)
            componentes =  cur.fetchall()
            data = []
            for c in componentes:
                data.append([c[0],c[1],c[2],c[3], 1, None, None, c[6]])
            return data
        except Exception as e:
            print("Exeception occured in DAOComponente:{}".format(e))
            return
        finally:
            con.close()

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
