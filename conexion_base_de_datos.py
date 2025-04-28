import pymysql

class ConexionBaseDatos:
    def __init__(self, host, usuario, contrasena, nombre_base_datos):
        self.host = host
        self.usuario = usuario
        self.contrasena = contrasena
        self.nombre_base_datos = nombre_base_datos
        self.conexion = None

    def conectar(self):
        """Establece la conexión con la base de datos"""
        try:
            self.conexion = pymysql.connect(
                host=self.host,
                user=self.usuario,
                password=self.contrasena,
                db=self.nombre_base_datos,
                cursorclass=pymysql.cursors.DictCursor  # Esto nos devuelve los resultados como diccionarios
            )
            print("Conexión a la base de datos establecida correctamente.")
        except pymysql.Error as error:
            print("Error al conectar a la base de datos:", error)
            raise  # Es recomendable hacer un raise para que el error se gestione adecuadamente

    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos"""
        if self.conexion:
            self.conexion.close()
            print("Conexión a la base de datos cerrada correctamente.")

    def ejecutar_consulta(self, consulta, valores=None):
        """Ejecuta una consulta SQL (para INSERT, UPDATE, DELETE)"""
        try:
            with self.conexion.cursor() as cursor:
                # Ejecutar consulta
                if valores:
                    cursor.execute(consulta, valores)
                else:
                    cursor.execute(consulta)

                # Confirmar la transacción
                self.conexion.commit()  # Aquí confirmamos la transacción
                print("Consulta ejecutada correctamente.")
                
                # Retorna el ID del último registro insertado
                return cursor.lastrowid
        except pymysql.Error as error:
            print("Error al ejecutar la consulta:", error)
            self.conexion.rollback()  # En caso de error, revertimos la transacción
            return None

    def consultar_datos(self, consulta, valores=None):
        """Realiza una consulta SQL SELECT"""
        try:
            with self.conexion.cursor() as cursor:
                if valores:
                    cursor.execute(consulta, valores)
                else:
                    cursor.execute(consulta)
                
                # Traemos todos los resultados de la consulta
                resultados = cursor.fetchall()
            return resultados
        except pymysql.Error as error:
            print("Error al consultar datos:", error)
            return None

    def eliminar_datos(self, consulta):
        """Ejecuta una consulta para eliminar datos"""
        self.ejecutar_consulta(consulta)
        print("Datos eliminados correctamente.")

    def modificar_datos(self, consulta):
        """Ejecuta una consulta para modificar datos"""
        self.ejecutar_consulta(consulta)
        print("Datos modificados correctamente.")
        
if __name__ == "__main__":
    host = 'localhost'
    usuario = 'root'
    contrasena = ''
    nombre_base_datos = 'inventario_de_equipos_tecnologicos'

    conexion_db = ConexionBaseDatos(host, usuario, contrasena, nombre_base_datos)
    conexion_db.conectar()

    # Ejemplo de consultaXD
    consulta_select = "SELECT * FROM login"
    resultados = conexion_db.consultar_datos(consulta_select)
    print("Resultados de la consulta SELECT:")
    print(resultados)

    # Ejemplo de eliminaciónXD
    consulta_delete = "DELETE FROM usuarios WHERE id = 1"
    conexion_db.eliminar_datos(consulta_delete)

    # Ejemplo de modificaciónXD
    consulta_update = "UPDATE usuarios SET nombre = 'Nuevo Nombre' WHERE id = 2"
    conexion_db.modificar_datos(consulta_update)

    # Ejemplo de registroXD
    consulta_insert = "INSERT INTO usuarios (nombre, email) VALUES ('Nuevo Usuario', 'nuevo_usuario@example.com')"
    conexion_db.registrar_datos(consulta_insert)

    # Cerrar la conexión cuando hayas terminadoXD
    conexion_db.cerrar_conexion()
    
    conexion_db = ConexionBaseDatos(host, usuario, contrasena, nombre_base_datos)
    conexion_db.conectar()
    consulta = "SELECT idproveedor, nombre FROM proveedor;"
    proveedores = conexion_db.consultar_datos(consulta)
    print (proveedores)
    conexion_db.cerrar_conexion()

  