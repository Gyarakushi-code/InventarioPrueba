
import sqlite3
import os

class ConexionBaseDatos:
    def __init__(self, nombre_archivo_db):
        self.nombre_archivo_db = nombre_archivo_db
        self.conexion = None

    def conectar(self):
        """Establece la conexión con la base de datos SQLite"""
        try:
            db_path = os.path.join(os.getcwd(), self.nombre_archivo_db)
            self.conexion = sqlite3.connect(db_path, check_same_thread=False)
            self.conexion.row_factory = sqlite3.Row
            print("Conexión a la base de datos SQLite establecida correctamente.")
        except sqlite3.Error as error:
            print("Error al conectar a la base de datos:", error)
            raise

    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos"""
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada correctamente.")

    def ejecutar_consulta(self, consulta, valores=None):
        """Ejecuta una consulta SQL (INSERT, UPDATE, DELETE)"""
        try:
            cursor = self.conexion.cursor()
            if valores:
                cursor.execute(consulta, valores)
            else:
                cursor.execute(consulta)
            self.conexion.commit()
            print("Consulta ejecutada correctamente.")
            return cursor.lastrowid
        except sqlite3.Error as error:
            print("Error al ejecutar consulta:", error)
            self.conexion.rollback()
            return None

    def consultar_datos(self, consulta, valores=None):
        """Realiza una consulta SQL SELECT"""
        try:
            cursor = self.conexion.cursor()
            if valores:
                cursor.execute(consulta, valores)
            else:
                cursor.execute(consulta)
            resultados = cursor.fetchall()
            return [dict(row) for row in resultados]
        except sqlite3.Error as error:
            print("Error al consultar datos:", error)
            return None

# --------- EJEMPLO DE USO ------------

if __name__ == "__main__":
    db_nombre = 'Inventario_de_equipos_tecnico.db'
    conexion_db = ConexionBaseDatos(db_nombre)
    conexion_db.conectar()

    # Ejemplo de SELECT
    consulta = "SELECT * FROM usuarios;"
    usuarios = conexion_db.consultar_datos(consulta)
    print("Usuarios encontrados:")
    print(usuarios)

    conexion_db.cerrar_conexion()
