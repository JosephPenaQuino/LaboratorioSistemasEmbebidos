import pymysql
import settings
from dao.DAOComponente import DAOComponente

class DAOPrestamo:
    def __init__(self):
        self.componenteDB = DAOComponente()

    def connect(self):
        host = settings.MYSQL_HOST
        user = settings.MYSQL_USER
        password = settings.MYSQL_PASSWORD 
        db = settings.MYSQL_DB 
        return pymysql.connect(host, user, password, db)

    def getPrestamosPorConfirmar(self):
        con = DAOPrestamo.connect(self)
        cur = con.cursor()
        data = []
        try:
            cur.execute((   "SELECT * FROM prestamo "
                            "WHERE Entregado=1 AND EntregaConfirmada=0"))
            prestamos = cur.fetchall()
            for prestamo in prestamos:
                component_id = prestamo[3]
                c = self.componenteDB.read(component_id)[0]
                data.append([prestamo[0],c[1],c[2],c[3],1,prestamo[1],prestamo[5],c[6]])
            return data
        except Exception as e:
            print("Exception occured in DAOPrestamo:{}".format(e))
            return
        finally:
            con.close()

    def getUserId(self, prestamoId):
        con = DAOPrestamo.connect(self)
        cur = con.cursor()
        try:
            cur.execute((   "SELECT id_usuario FROM prestamo "
                            "WHERE id=%s"), (prestamoId))
            return cur.fetchall()
        except Exception as e:
            print("Exception occured in DAOPrestamo:{}".format(e))
            return
        finally:
            con.close()

    def confirmarDevolucion(self, prestamoId):
        con = DAOPrestamo.connect(self)
        cur = con.cursor()
        try:
            cur.execute("UPDATE prestamo set EntregaConfirmada=1 WHERE id=%s",(prestamoId))
            con.commit()
        except Exception as e:
            print("Exception occured in DAOPrestamo:{}".format(e))
            return
        finally:
            con.close()

    def negarDevolucion(self, prestamoId):
        con = DAOPrestamo.connect(self)
        cur = con.cursor()
        try:
            cur.execute("UPDATE prestamo set Entregado=0 WHERE id=%s",(prestamoId))
            con.commit()
        except Exception as e:
            print("Exception occured in DAOPrestamo:{}".format(e))
            return
        finally:
            con.close()

    def returnComponent(self, prestamoId):
        con = DAOPrestamo.connect(self)
        cur = con.cursor()
        try:
            cur.execute("UPDATE prestamo set Entregado=1 WHERE id=%s",(prestamoId))
            con.commit()
        except Exception as e:
            print("Exception occured in DAOPrestamo:{}".format(e))
            return
        finally:
            con.close()

    def read(self, userId):
        con = DAOPrestamo.connect(self)
        cur = con.cursor()
        data = []
        try:
            cur.execute((   "SELECT * FROM prestamo "
                            "WHERE id_usuario=%s AND "
                            "Entregado=0"), (userId))
            prestamos = cur.fetchall()
            for prestamo in prestamos:
                component_id = prestamo[3]
                c = self.componenteDB.read(component_id)[0]
                data.append([prestamo[0],c[1],c[2],c[3],1,prestamo[1],prestamo[5],c[6]])
                
            print("Data: ")
            print(data)
            return data
        except Exception as e:
            print("Exception occured in DAOPrestamo:{}".format(e))
            return
        finally:
            con.close()
