import pymysql
import os

class ConexionBaseDatos:
    def __init__(self, host, usuario, contrasena, nombre_base_datos, puerto=3306):
        self.host = host
        self.usuario = usuario
        self.contrasena = contrasena
        self.nombre_base_datos = nombre_base_datos
        self.puerto = puerto
        self.conexion = None

    def conectar(self):
        """Establece la conexión con la base de datos"""
        try:
            self.conexion = pymysql.connect(
                host=self.host,
                user=self.usuario,
                password=self.contrasena,
                db=self.nombre_base_datos,
                port=self.puerto,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Conexión a la base de datos establecida correctamente.")
        except pymysql.Error as error:
            print("Error al conectar a la base de datos:", error)
            raise

    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos"""
        if self.conexion:
            self.conexion.close()
            print("Conexión a la base de datos cerrada correctamente.")

    def ejecutar_consulta(self, consulta, valores=None):
        """Ejecuta una consulta SQL (INSERT, UPDATE, DELETE)"""
        try:
            with self.conexion.cursor() as cursor:
                if valores:
                    cursor.execute(consulta, valores)
                else:
                    cursor.execute(consulta)
                self.conexion.commit()
                print("Consulta ejecutada correctamente.")
                return cursor.lastrowid
        except pymysql.Error as error:
            print("Error al ejecutar la consulta:", error)
            self.conexion.rollback()
            return None

    def consultar_datos(self, consulta, valores=None):
        """Realiza una consulta SQL SELECT"""
        try:
            with self.conexion.cursor() as cursor:
                if valores:
                    cursor.execute(consulta, valores)
                else:
                    cursor.execute(consulta)
                resultados = cursor.fetchall()
            return resultados
        except pymysql.Error as error:
            print("Error al consultar datos:", error)
            return None

    def eliminar_datos(self, consulta, valores=None):
        """Ejecuta una consulta DELETE"""
        self.ejecutar_consulta(consulta, valores)
        print("Datos eliminados correctamente.")

    def modificar_datos(self, consulta, valores=None):
        """Ejecuta una consulta UPDATE"""
        self.ejecutar_consulta(consulta, valores)
        print("Datos modificados correctamente.")

if __name__ == "__main__":
    # Lee variables de entorno (para producción segura)
    host = os.getenv("DB_HOST", "centerbeam.proxy.rlwy.net")
    usuario = os.getenv("DB_USER", "root")
    contrasena = os.getenv("DB_PASSWORD", "oJoXRuCVYdHuUdGUTDQNOfTBKsFMEjPf")
    nombre_base_datos = os.getenv("DB_NAME", "railway")
    puerto = int(os.getenv("DB_PORT", 43729))

    conexion_db = ConexionBaseDatos(host, usuario, contrasena, nombre_base_datos, puerto)
    conexion_db.conectar()

    # Ejemplo de SELECT
    consulta_select = "SELECT * FROM departamento"
    resultados = conexion_db.consultar_datos(consulta_select)
    print("Resultados de la consulta SELECT:")
    print(resultados)

    # Ejemplo de DELETE (no ejecutará porque 'usuarios' no existe aún)
    # consulta_delete = "DELETE FROM usuarios WHERE id = 1"
    # conexion_db.eliminar_datos(consulta_delete)

    # Ejemplo de UPDATE (no ejecutará porque 'usuarios' no existe aún)
    # consulta_update = "UPDATE usuarios SET nombre = 'Nuevo Nombre' WHERE id = 2"
    # conexion_db.modificar_datos(consulta_update)

    # Cerrar conexión
    conexion_db.cerrar_conexion()

  