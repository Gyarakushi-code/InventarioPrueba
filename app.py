from flask import Flask, render_template, request, redirect, url_for, session, flash, json, make_response, jsonify, send_from_directory, send_file
import pymysql
import os  
import time
from conexion_base_de_datos import ConexionBaseDatos
from fpdf import FPDF
from fpdf.enums import XPos, YPos
app = Flask(__name__)
app.secret_key = 'hola'  # Super necesario para las sesiones si 
DIRECTORIO_REPORTES = os.path.abspath('reportes') # NOMBRE DE LA CARPETA 
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'inventario_de_equipos_tecnologicos'

@app.route('/')
def inicio():
    var1 = True
    return render_template('home.html', var1=True)

@app.route('/login', methods=['POST'])
def verificarusuario():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    tipo_user = request.form['tipo_user']

    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()
    # Nuevas consultas de conteo
    total_usuarios = conexion_db.consultar_datos("SELECT COUNT(*) AS total FROM login")[0]['total']
    total_admins = conexion_db.consultar_datos("SELECT COUNT(*) AS total FROM login WHERE tipo_user = 'Administrador'")[0]['total']
    total_computadoras = conexion_db.consultar_datos("SELECT COUNT(*) AS total FROM inventario")[0]['total']
    total_otros = conexion_db.consultar_datos("SELECT COUNT(*) AS total FROM otros")[0]['total']
    consulta = """
        SELECT * 
        FROM login 
        WHERE usuario = %s AND contrasena = %s AND tipo_user = %s
    """
    resultados = conexion_db.consultar_datos(consulta, (usuario, contrasena, tipo_user))

    consulta_departamentos = "SELECT * FROM departamento"
    departamentos = conexion_db.consultar_datos(consulta_departamentos)
    conexion_db.cerrar_conexion()

    if resultados:
        usuario_activo = resultados[0]
        session['user_id'] = usuario_activo['id_usuario']
        session['username'] = usuario_activo['usuario']
        session['tipo_user'] = usuario_activo['tipo_user']
        session['avatar'] = usuario_activo.get('avatar', 'avatar-male.png')

        return render_template('home.html', var2=True, departamentos=departamentos, usuario_activo=usuario_activo,total_usuarios=total_usuarios,
        total_admins=total_admins,
        total_computadoras=total_computadoras,
        total_otros=total_otros)
    else:
        flash("Usuario o contraseña incorrectos. Inténtalo de nuevo.", "error")
        return redirect('/')
    
@app.route('/logout')
def logout():
    session.clear()  # Borra todos los datos de la sesión
    return redirect('/')

    
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')
  

    var2 = True
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()

    # Mantener tu consulta original
    consulta = "SELECT * FROM departamento"
    departamentos = conexion_db.consultar_datos(consulta)
    print(departamentos)

    # Nuevas consultas de conteo
    total_usuarios = conexion_db.consultar_datos("SELECT COUNT(*) AS total FROM login")[0]['total']
    total_admins = conexion_db.consultar_datos("SELECT COUNT(*) AS total FROM login WHERE tipo_user = 'Administrador'")[0]['total']
    total_computadoras = conexion_db.consultar_datos("SELECT COUNT(*) AS total FROM inventario")[0]['total']
    total_otros = conexion_db.consultar_datos("SELECT COUNT(*) AS total FROM otros")[0]['total']

    conexion_db.cerrar_conexion()

    return render_template(
        'home.html',
        var2=True,
        departamentos=departamentos,
        total_usuarios=total_usuarios,
        total_admins=total_admins,
        total_computadoras=total_computadoras,
        total_otros=total_otros
    )

class departamento:
    def __init__(self, nombre_dep, tipo_de_trabajo, encargado):
        self.nombre_dep = nombre_dep
        self.tipo_de_trabajo = tipo_de_trabajo
        self.encargado = encargado
 
@app.route('/dpt')
def dpt():
    if 'user_id' not in session:
        return redirect('/')
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()
    consulta = "SELECT * FROM departamento"
    departamentos = conexion_db.consultar_datos(consulta)
    print(departamentos)
    conexion_db.cerrar_conexion()
    
    
    return render_template('home.html', var4=True, departamentos=departamentos)
    return jsonify(departamentos)

@app.route('/departamento', methods=['POST'])
def registrar_departamento():
    if session.get('tipo_user') != 'Administrador':  # Validamos si el usuario es administrador
        return jsonify({'error': 'No tiene permisos para registrar un departamento'}), 403

    nombre_dep = request.form['nombre_dep']
    tipo_de_trabajo = request.form['tipo_de_trabajo']
    encargado = request.form['encargado']

    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()
    consulta = "INSERT INTO departamento (nombre_dep, tipo_de_trabajo, encargado) VALUES (%s, %s, %s)"
    valores = (nombre_dep, tipo_de_trabajo, encargado)
    conexion_db.ejecutar_consulta(consulta, valores)
    conexion_db.cerrar_conexion()
    return redirect('/dpt')
    
@app.route('/modificar_departamento/<int:id_departamento>', methods=['POST'])
def modificar_departamento(id_departamento): 
    if session.get('tipo_user') != 'Administrador':  # Verificar si el usuario es admin
        return "No tienes permisos para modificar este dato", 403  # Retornar un mensaje si no tiene permisos

    
    nombre_dep = request.form['nombre_dep']
    tipo_de_trabajo = request.form['tipo_de_trabajo']
    encargado = request.form['encargado']
    
    
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()
    consulta = "UPDATE departamento SET nombre_dep=%s, tipo_de_trabajo=%s, encargado=%s WHERE id_departamento=%s"
    valores = (nombre_dep, tipo_de_trabajo, encargado, id_departamento)
    conexion_db.ejecutar_consulta(consulta, valores)
    conexion_db.cerrar_conexion()

    return redirect('/dpt')  



@app.route('/eliminar_departamento/<int:id_departamento>', methods=['POST'])
def eliminar_departamento(id_departamento):
    if session.get('tipo_user') != 'Administrador':  # Verificar si el usuario es admin
        return "No tienes permisos para eliminar este dato", 403  # Retornar un mensaje si no tiene permisos

    
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()
    consulta = "DELETE FROM departamento WHERE id_departamento=%s"
    valores = (id_departamento,)
    try:
        conexion_db.ejecutar_consulta(consulta, valores)
        conexion_db.commit() 
    except Exception as e:
        print(f"Error al eliminar departamento: {e}")
    finally:
        conexion_db.cerrar_conexion()
    
    return redirect('/dpt') 
class equipos:
    def __init__(self,mac_placa, fuentes_de_poder, disco_duro, procesador, ram, fecha_ingreso, estado, otros):
        self.mac_placa = mac_placa
        self.fuentes_de_poder = fuentes_de_poder
        self.disco_duro = disco_duro
        self.procesador = procesador
        self.ram = ram
        self.fecha_ingreso = fecha_ingreso
        self.estado = estado
        self.otros = otros
    
@app.route('/equipos')
def equipos():
    if 'user_id' not in session:
        return redirect('/')
    id_departamento = session.get('id_departamento')  # Obtener el departamento seleccionado
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()

    if id_departamento:  # Filtrar por departamento seleccionado
        consulta_inventario = "SELECT * FROM inventario WHERE departamento_id = %s"
        inventarios = conexion_db.consultar_datos(consulta_inventario, (id_departamento,))

        consulta_otros = "SELECT * FROM otros WHERE idotros_iddepartamento = %s"
        otros = conexion_db.consultar_datos(consulta_otros, (id_departamento,))
    else:  # Mostrar todos los equipos y registros de otros si no hay departamento seleccionado
        consulta_inventario = "SELECT * FROM inventario"
        inventarios = conexion_db.consultar_datos(consulta_inventario)

        consulta_otros = "SELECT * FROM otros"
        otros = conexion_db.consultar_datos(consulta_otros)

    consulta_departamentos = "SELECT * FROM departamento"
    departamentos = conexion_db.consultar_datos(consulta_departamentos)

    conexion_db.cerrar_conexion()

    return render_template('home.html', var5=True, inventarios=inventarios, departamentos=departamentos, otros=otros)


@app.route('/seleccionar_departamento/<int:id_departamento>', methods=['GET'])
def seleccionar_departamento(id_departamento):
    session['id_departamento'] = id_departamento
    
    return redirect('/equipos')


@app.route('/inve', methods=['POST'])
def registrar_inventario():
    if session.get('tipo_user') != 'Administrador':  # Validamos si el usuario es administrador
        return jsonify({'error': 'No tiene permisos para registrar un equipo'}), 403

    nombre_pc = request.form['nombre_pc']
    mac_placa = request.form['mac_placa']
    fuentes_de_poder = request.form['fuentes_de_poder']
    disco_duro = request.form['disco_duro']
    procesador = request.form['procesador']
    ram = request.form['ram']
    fecha_ingreso = request.form['fecha_ingreso']
    estado = request.form['estado']

   
    departamento_id = request.form.get('departamento_id')  
    if not departamento_id:  
        departamento_id = session.get('id_departamento')

   
    if not departamento_id:
        return "Error: Selecciona un departamento antes de registrar el equipo.", 400

    try:
      
        conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
        conexion_db.conectar()

       
        consulta = """
            INSERT INTO inventario 
            (nombre_pc, mac_placa, fuentes_de_poder, disco_duro, procesador, ram, fecha_ingreso, estado, departamento_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (nombre_pc, mac_placa, fuentes_de_poder, disco_duro, procesador, ram, fecha_ingreso, estado, departamento_id)
        conexion_db.ejecutar_consulta(consulta, valores)
        print("Valores insertados:", valores)

   
        conexion_db.cerrar_conexion()

        
        return redirect('/equipos')

    except Exception as e:
        print("Error al registrar inventario:", e)
        return f"Error: {str(e)}", 500
    
@app.route('/modificar_inventario/<int:id_equipos>', methods=['POST'])

def modificar_inventario(id_equipos):
    if session.get('tipo_user') != 'Administrador':  # Verificar si el usuario es admin
        return "No tienes permisos para eliminar este dato", 403  # Retornar un mensaje si no tiene permisos
    nombre_pc = request.form['nombre_pc']
    mac_placa = request.form['mac_placa']
    fuentes_de_poder = request.form['fuentes_de_poder']
    disco_duro = request.form['disco_duro']
    procesador = request.form['procesador']
    ram = request.form['ram']
    fecha_ingreso = request.form['fecha_ingreso']
    estado = request.form['estado']
    
   
    
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()
    consulta = "UPDATE inventario SET nombre_pc=%s, mac_placa=%s, fuentes_de_poder=%s, disco_duro=%s, procesador=%s, ram=%s, fecha_ingreso=%s, estado=%s WHERE id_equipos=%s"
    valores = (nombre_pc, mac_placa, fuentes_de_poder, disco_duro, procesador, ram, fecha_ingreso, estado, id_equipos)
    conexion_db.ejecutar_consulta(consulta, valores)
    conexion_db.cerrar_conexion()
    return redirect('/equipos')


@app.route('/eliminar_inventario/<int:id_equipos>', methods=['POST'])
def eliminar_inventario(id_equipos ):
    if session.get('tipo_user') != 'Administrador':  # Verificar si el usuario es admin
        return "No tienes permisos para eliminar este dato", 403  # Retornar un mensaje si no tiene permisos
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()
    consulta = "DELETE FROM inventario WHERE id_equipos=%s"
    valores = (id_equipos,)
    try:
        conexion_db.ejecutar_consulta(consulta, valores)
        conexion_db.commit()  # Confirma la eliminación
    except Exception as e:
        print(f"Error al eliminar inventario: {e}")
    finally:
        conexion_db.cerrar_conexion()
    return redirect('/equipos')

@app.route('/otro', methods=['POST'])
def registrar_inventario_otro():
    if session.get('tipo_user') != 'Administrador':  # Validamos si el usuario es administrador
        return jsonify({'error': 'No tiene permisos para registrar un departamento'}), 403

    nombre_otros = request.form['nombre_otros']
    fecha_ingreso_otros = request.form['fecha_ingreso_otros']
    estado_otros = request.form['estado_otros']
    descripcion_otros = request.form['descripcion_otros']

   
    idotros_iddepartamento = request.form.get('idotros_iddepartamento')  
    if not idotros_iddepartamento:  
        idotros_iddepartamento = session.get('id_departamento')

   
    if not idotros_iddepartamento:
        return "Error: Selecciona un departamento antes de registrar el equipo.", 400

    try:
      
        conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
        conexion_db.conectar()

       
        consulta = """
            INSERT INTO otros 
            (descripcion_otros, estado_otros, fecha_ingreso_otros, nombre_otros, idotros_iddepartamento) 
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (descripcion_otros, estado_otros, fecha_ingreso_otros, nombre_otros, idotros_iddepartamento)
        conexion_db.ejecutar_consulta(consulta, valores)
        print("Valores insertados:", valores)

   
        conexion_db.cerrar_conexion()

        
        return redirect('/equipos')

    except Exception as e:
        print("Error al registrar inventario:", e)
        return f"Error: {str(e)}", 500
    
@app.route('/modificar_otros/<int:idotros>', methods=['POST'])
def modificar_otros(idotros):
    if session.get('tipo_user') != 'Administrador':  # Verificar si el usuario es admin
        return "No tienes permisos para eliminar este dato", 403  # Retornar un mensaje si no tiene permisos
    nombre_otros = request.form['nombre_otros']
    fecha_ingreso_otros = request.form['fecha_ingreso_otros']
    estado_otros = request.form['estado_otros']
    descripcion_otros = request.form['descripcion_otros']
    
   
    
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()
    consulta = "UPDATE otros SET nombre_otros=%s, fecha_ingreso_otros=%s, estado_otros=%s, descripcion_otros=%s WHERE idotros=%s"
    valores = (nombre_otros, fecha_ingreso_otros, estado_otros, descripcion_otros, idotros)
    conexion_db.ejecutar_consulta(consulta, valores)
    conexion_db.cerrar_conexion()
    return redirect('/equipos')


@app.route('/eliminar_otros/<int:idotros>', methods=['POST'])
def eliminar_otros(idotros ):
    if session.get('tipo_user') != 'Administrador':  # Verificar si el usuario es admin
        return "No tienes permisos para eliminar este dato", 403  # Retornar un mensaje si no tiene permisos
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()
    consulta = "DELETE FROM otros WHERE idotros=%s"
    valores = (idotros,)
    try:
        conexion_db.ejecutar_consulta(consulta, valores)
        conexion_db.commit()  # Confirma la eliminación
    except Exception as e:
        print(f"Error al eliminar otros: {e}")
    finally:
        conexion_db.cerrar_conexion()
    return redirect('/equipos')



class user:
    def __init__(self,user,contrasena,tipo_user):
        self.user = user
        self.contrasena = contrasena
        self.tipo_user = tipo_user
    
@app.route('/user')
def usuarios():
    if 'user_id' not in session:
        return redirect('/') 
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()
    
    consulta_logins = """
        SELECT * FROM login """
    logins = conexion_db.consultar_datos(consulta_logins)
    
    consulta_departamentos = "SELECT * FROM departamento"
    departamentos = conexion_db.consultar_datos(consulta_departamentos)
    
    conexion_db.cerrar_conexion()
    if 'user_id' not in session:
        return redirect('/login')  # Redirigir al login si no hay sesión activa
    
    # Recuperar datos del usuario activo desde la sesión
    usuario_activo = {
        'id_usuario': session['user_id'],
        'usuario': session['username'],
        'tipo_user': session['tipo_user'],
        'avatar': session.get('avatar', 'static/assets/img/avatar-male.png')
    }
    
    return render_template('home.html',var3=True , usuario_activo=usuario_activo, logins=logins,departamentos=departamentos )

@app.route('/registrar_user', methods=['POST'])
def registrar_user():
    # Obtener datos del formulario
    if session.get('tipo_user') != 'Administrador':  # Validamos si el usuario es administrador
        return jsonify({'error': 'No tiene permisos para registrar un departamento'}), 403

    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    tipo_user = request.form['tipo_user']
    avatar = request.form['avatar']  # Avatar seleccionado

    # Insertar en la tabla `login`
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()
    
    consulta_login = """INSERT INTO login (usuario, contrasena, tipo_user, avatar) 
                        VALUES (%s, %s, %s, %s)"""
    valores_login = (usuario, contrasena, tipo_user, avatar)
    
    conexion_db.ejecutar_consulta(consulta_login, valores_login)
    print("Usuario registrado:", valores_login)

    conexion_db.cerrar_conexion()

    return redirect('/user')  # Redirigir a la página donde se muestran los usuarios

@app.route('/modificar_user/<int:id_usuario>', methods=['POST'])
def modificar_user(id_usuario):
    if session.get('tipo_user') != 'Administrador':  # Verificar si el usuario es admin
        return "No tienes permisos para eliminar este dato", 403  # Retornar un mensaje si no tiene permisos
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    tipo_user = request.form['tipo_user']
    
    
   
    
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()
    consulta = "UPDATE login SET usuario=%s, contrasena=%s, tipo_user=%s WHERE id_usuario=%s"
    valores = (usuario, contrasena, tipo_user,  id_usuario)
    conexion_db.ejecutar_consulta(consulta, valores)
    conexion_db.cerrar_conexion()
    return redirect('/user')


@app.route('/eliminar_user/<int:id_usuario>', methods=['POST'])
def eliminar_user(id_usuario ):
    if session.get('tipo_user') != 'Administrador':  # Verificar si el usuario es admin
        return "No tienes permisos para eliminar este dato", 403  # Retornar un mensaje si no tiene permisos
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()
    consulta = "DELETE FROM login WHERE id_usuario=%s"
    valores = (id_usuario,)
    try:
        conexion_db.ejecutar_consulta(consulta, valores)
        conexion_db.commit()  # Confirma la eliminación
    except Exception as e:
        print(f"Error al eliminar otros: {e}")
    finally:
        conexion_db.cerrar_conexion()
    return redirect('/user')
    
@app.route('/reporte')
def reporte():
    if 'user_id' not in session:
        return redirect('/')
    var6 = True
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()

    # Consulta para obtener todos los departamentos
    consulta_departamentos = "SELECT * FROM departamento"
    departamentos = conexion_db.consultar_datos(consulta_departamentos)

   

    conexion_db.cerrar_conexion()
    ruta_reportes = 'static/reportes'
    
    # Obtener todos los archivos PDF de la carpeta
    reportes = [f for f in os.listdir(ruta_reportes) if f.endswith('.pdf')]
    return render_template('home.html', var6=var6, departamentos=departamentos, reportes=reportes)

@app.route('/crear_reporte', methods=['GET', 'POST'])
def crear_reporte():
    if session.get('tipo_user') != 'Administrador':  # Validamos si el usuario es administrador
        return jsonify({'error': 'No tiene permisos para registrar un departamento'}), 403

    id_usuario = session.get('user_id')  # Usamos session.get para evitar KeyError
    
    if request.method == 'POST':
        # Obtener el ID del departamento seleccionado desde el formulario
        id_departamento = request.form['id_departamento']
        # Obtener el ID del usuario de la sesión
        
        # Conectar a la base de datos
        conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
        conexion_db.conectar()
        
        # Consultar el nombre del departamento
        consulta_departamento = """SELECT nombre_dep FROM departamento WHERE id_departamento = %s"""
        depart = conexion_db.consultar_datos(consulta_departamento, (id_departamento,))
        if depart and isinstance(depart, list) and len(depart) > 0:
            if isinstance(depart[0], dict):
                nombre_departamento = depart[0].get('nombre_dep', 'Desconocido')
            else:
                nombre_departamento = depart[0][0]
        else:
            nombre_departamento = "Desconocido"
        
        # Consultar los equipos del departamento
        consulta_equipos = """
            SELECT nombre_pc, mac_placa, procesador, ram, fuentes_de_poder, disco_duro, fecha_ingreso, estado
            FROM inventario 
            WHERE departamento_id = %s
        """
        equipos = conexion_db.consultar_datos(consulta_equipos, (id_departamento,))
        
        # Consultar otros equipos relacionados
        consulta_otros = """
            SELECT descripcion_otros, estado_otros, fecha_ingreso_otros, nombre_otros
            FROM otros
            WHERE idotros_iddepartamento = %s
        """
        otros = conexion_db.consultar_datos(consulta_otros, (id_departamento,))
        
        # Generar el reporte en PDF
        pdf = FPDF('L', 'mm', 'Legal')
        pdf.add_page()
        # aca quiero colocar el codigo de imagen
        pdf.image('static/img/iuta-logo.png', x=280, y=5, w=50)  # Ajusta según el tamaño deseado
        pdf.ln(20)
        # Título
        pdf.set_font('Helvetica', 'B', 16)
        pdf.cell(350, 10, "Reporte de Equipos", ln=True, align='C')
        pdf.ln(10)
        
        # Departamento
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 10, f"Departamento: {nombre_departamento}", ln=True, align='L')
        
        
        # Primero, insertar el reporte en la base de datos para validar despuyes
       
        insertar_reporte = """
        INSERT INTO reporte (nombre_reporte, departamento_id, fecha_creacion, ruta_archivo, id_usuario)
        VALUES (%s, %s, NOW(), %s, %s)
        """
        conexion_db.ejecutar_consulta(insertar_reporte, (f"Reporte de {nombre_departamento}", id_departamento, "", id_usuario))

        consulta_reporte = """
        SELECT r.id_reporte, r.fecha_creacion, l.id_usuario, l.usuario 
        FROM reporte r
        LEFT JOIN login l ON r.id_usuario = l.id_usuario
        WHERE r.nombre_reporte = %s
        ORDER BY r.id_reporte DESC LIMIT 1
        """
        reporte = conexion_db.consultar_datos(consulta_reporte, (f"Reporte de {nombre_departamento}",))
        
        print("ID del usuario:", id_usuario)  # Verifica que id_usuario no sea None o ''
        
        if reporte:
            id_reporte = reporte[0]['id_reporte']
            fecha_creacion = reporte[0]['fecha_creacion'].strftime('%d/%m/%Y %H:%M:%S')
            id_usuario = reporte[0]['usuario'] if reporte[0]['usuario'] else 'Usuario Desconocido'
        else:
            id_reporte = 'Desconocido'
            fecha_creacion = 'Desconocida'
            id_usuario = 'Desconocido'

        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 10, f"Generado por: {id_usuario}", ln=True, align='L')  # Mostrar el usuario en el PDF
        
        # Mostrar el ID y la fecha de creación del reporte 
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 10, f"ID del Reporte: {id_reporte}", ln=True, align='L')
        pdf.cell(0, 10, f"Fecha de Creación: {fecha_creacion}", ln=True, align='L')
        pdf.ln(10)

        # Tabla de Equipos con su bordes y sus datos
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(50, 10, "Nombre del Equipo", border=1)
        pdf.cell(50, 10, "MAC Placa", border=1)
        pdf.cell(50, 10, "Procesador", border=1)
        pdf.cell(20, 10, "RAM", border=1)
        pdf.cell(35, 10, "Fuente de Poder", border=1)
        pdf.cell(35, 10, "Disco Duro", border=1)
        pdf.cell(35, 10, "Fecha de Ingreso", border=1)
        pdf.cell(30, 10, "Estado", border=1)
        pdf.ln()

        if equipos:
            for equipo in equipos:
                pdf.cell(50, 10, equipo['nombre_pc'], border=1)
                pdf.cell(50, 10, equipo['mac_placa'], border=1)
                pdf.cell(50, 10, equipo['procesador'], border=1)
                pdf.cell(20, 10, equipo['ram'], border=1)
                pdf.cell(35, 10, equipo['fuentes_de_poder'], border=1)
                pdf.cell(35, 10, equipo['disco_duro'], border=1)
                fecha_ingreso = equipo['fecha_ingreso'].strftime('%d/%m/%Y') if equipo['fecha_ingreso'] else ''
                pdf.cell(35, 10, fecha_ingreso, border=1)
                pdf.cell(30, 10, equipo['estado'], border=1)
                pdf.ln()
        else:
            pdf.cell(0, 10, "No hay equipos registrados en este departamento.", ln=True)

        # Tabla de Otros Equipos con su bordes y sus datos
        pdf.ln(10)
        pdf.cell(50, 10, "Nombre de otros equipos", border=1)
        pdf.cell(70, 10, "Descripcion", border=1)
        pdf.cell(50, 10, "Fecha de ingreso", border=1)
        pdf.cell(45, 10, "Estado del equipo", border=1)
        pdf.ln()

        if otros:
            for otro in otros:
                pdf.cell(50, 10, otro['nombre_otros'], border=1)
                pdf.cell(70, 10, otro['descripcion_otros'], border=1)
                fecha_ingreso_otros = otro['fecha_ingreso_otros'].strftime('%d/%m/%Y') if otro['fecha_ingreso_otros'] else ''
                pdf.cell(50, 10, fecha_ingreso_otros, border=1)
                pdf.cell(45, 10, otro['estado_otros'], border=1)
                pdf.ln()
        else:
            pdf.cell(0, 10, "No hay otros equipos registrados.", ln=True)

        # Guardar el archivo PDF
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        pdf_output = f"static/reportes/reporte_{nombre_departamento}_{timestamp}.pdf".replace(" ", "_")
        pdf.output(pdf_output)
        # Actualizar la ruta del archivo en la base de datos con su id
        actualizar_ruta_archivo = """
            UPDATE reporte SET ruta_archivo = %s WHERE id_reporte = %s
        """
        conexion_db.ejecutar_consulta(actualizar_ruta_archivo, (pdf_output, id_reporte))

        conexion_db.cerrar_conexion()
        return redirect(url_for('reporte'))
    
    else:
        # Consultar los departamentos de base de datos
        conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
        conexion_db.conectar()
        consulta_departamentos = "SELECT id_departamento, nombre_dep FROM departamento"
        departamentos = conexion_db.consultar_datos(consulta_departamentos)
        conexion_db.cerrar_conexion()

        return render_template('home.html', var6=True, departamentos=departamentos)


@app.route('/descargar_reporte/<reporte>')
def descargar_reporte(reporte):
    # Ruta completa a la carpeta de reportes hay se ven unicamente una sola ves 
    ruta_completa = os.path.join('static', 'reportes', reporte)
    
    # Verificar si el archivo existe
    if os.path.exists(ruta_completa):
        return send_file(ruta_completa, as_attachment=True)
    else:
        return "Archivo no encontrado", 404
    


@app.route('/reporte_global')
def reporte_global():
    if session.get('tipo_user') != 'Administrador':  # Validamos si el usuario es administrador
        return jsonify({'error': 'No tiene permisos para registrar un departamento'}), 403

    # Conectar a la base de datos
    conexion_db = ConexionBaseDatos(db_host, db_user, db_password, db_name)
    conexion_db.conectar()
     # Obtener el ID del usuario actual desde la sesión
    id_usuario = session.get('user_id')

    # Consultar el nombre del usuario basado en su id
    consulta_usuario = """
        SELECT usuario FROM login WHERE id_usuario = %s
    """
    usuario_data = conexion_db.consultar_datos(consulta_usuario, (id_usuario,))
    nombre_usuario = usuario_data[0]['usuario'] if usuario_data else "Usuario Desconocido"
    # Obtener todos los departamentos con sus equipos
    consulta_departamentos = """
        SELECT id_departamento, nombre_dep FROM departamento
    """
    departamentos = conexion_db.consultar_datos(consulta_departamentos)
    
    # Obtener la última fecha de creación
    consulta_fecha = """
    SELECT fecha_creacion_global FROM reporte_global 
    WHERE id_usuario_global = %s 
    ORDER BY id_reporte_global DESC LIMIT 1
    """
    fecha_data = conexion_db.consultar_datos(consulta_fecha, (id_usuario,))
    fecha_creacion = fecha_data[0]['fecha_creacion_global'].strftime('%d/%m/%Y %H:%M:%S') if fecha_data else "Fecha desconocida"

    # Insertar el reporte en la base de datos antes de generar el PDF
    consulta_insert = """
    INSERT INTO reporte_global (nombre_global, fecha_creacion_global, ruta_archivo_global, id_usuario_global)
    VALUES (%s, NOW(), %s, %s)
    """
    pdf_output = "static/reportes/reporte_global.pdf"
    conexion_db.ejecutar_consulta(consulta_insert, ("Reporte Global", pdf_output, id_usuario))

    # Obtener el ID del reporte recién insertado
    consulta_id = "SELECT LAST_INSERT_ID() AS id_reporte_global"
    id_reporte_data = conexion_db.consultar_datos(consulta_id)
    id_reporte_global = id_reporte_data[0]['id_reporte_global'] if id_reporte_data else "Desconocido"

    
    pdf = FPDF('L', 'mm', 'Legal')
    pdf.add_page()
    pdf.image('static/img/iuta-logo.png', x=280, y=5, w=50)  # Logo
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(350, 10, "Reporte Global de Equipos", ln=True, align='C')
    pdf.ln(10)
   # Agregar el nombre del usuario que genera el reporte
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, f"Generado por: {nombre_usuario}", ln=True, align='L')
    pdf.cell(0, 10, f"Fecha de Creación: {fecha_creacion}", ln=True, align='L')
    pdf.cell(0, 10, f"ID del Reporte: {id_reporte_global}", ln=True, align='L')
    for dep in departamentos:
        id_departamento = dep['id_departamento']
        nombre_departamento = dep['nombre_dep']

        # Agregar el nombre del departamento
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 10, f"Departamento: {nombre_departamento}", ln=True, align='L')
        pdf.ln(5)
        
        # Obtener los equipos del departamento
        consulta_equipos = """
            SELECT nombre_pc, mac_placa, procesador, ram, fuentes_de_poder, disco_duro, fecha_ingreso, estado
            FROM inventario 
            WHERE departamento_id = %s
        """
        equipos = conexion_db.consultar_datos(consulta_equipos, (id_departamento,))
         # Consultar otros equipos relacionados
        consulta_otros = """
            SELECT descripcion_otros, estado_otros, fecha_ingreso_otros, nombre_otros
            FROM otros
            WHERE idotros_iddepartamento = %s
        """
        otros = conexion_db.consultar_datos(consulta_otros, (id_departamento,))
        
        # Crear la tabla de equipos
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(50, 10, "Nombre del Equipo", border=1)
        pdf.cell(50, 10, "MAC Placa", border=1)
        pdf.cell(50, 10, "Procesador", border=1)
        pdf.cell(20, 10, "RAM", border=1)
        pdf.cell(35, 10, "Fuente de Poder", border=1)
        pdf.cell(35, 10, "Disco Duro", border=1)
        pdf.cell(35, 10, "Fecha de Ingreso", border=1)
        pdf.cell(30, 10, "Estado", border=1)
        pdf.ln()

        if equipos:
            for equipo in equipos:
                pdf.cell(50, 10, equipo['nombre_pc'], border=1)
                pdf.cell(50, 10, equipo['mac_placa'], border=1)
                pdf.cell(50, 10, equipo['procesador'], border=1)
                pdf.cell(20, 10, equipo['ram'], border=1)
                pdf.cell(35, 10, equipo['fuentes_de_poder'], border=1)
                pdf.cell(35, 10, equipo['disco_duro'], border=1)
                fecha_ingreso = equipo['fecha_ingreso'].strftime('%d/%m/%Y') if equipo['fecha_ingreso'] else ''
                pdf.cell(35, 10, fecha_ingreso, border=1)
                pdf.cell(30, 10, equipo['estado'], border=1)
                pdf.ln()
        else:
            pdf.cell(0, 10, "No hay equipos registrados en este departamento.", ln=True)
        # Tabla de Otros Equipos con su bordes y sus datos
        pdf.ln(10)
        pdf.cell(50, 10, "Nombre de otros equipos", border=1)
        pdf.cell(70, 10, "Descripcion", border=1)
        pdf.cell(50, 10, "Fecha de ingreso", border=1)
        pdf.cell(45, 10, "Estado del equipo", border=1)
        pdf.ln()
        
        if otros:
            for otro in otros:
                pdf.cell(50, 10, otro['nombre_otros'], border=1)
                pdf.cell(70, 10, otro['descripcion_otros'], border=1)
                fecha_ingreso_otros = otro['fecha_ingreso_otros'].strftime('%d/%m/%Y') if otro['fecha_ingreso_otros'] else ''
                pdf.cell(50, 10, fecha_ingreso_otros, border=1)
                pdf.cell(45, 10, otro['estado_otros'], border=1)
                pdf.ln()
        else:
            pdf.cell(0, 10, "No hay otros equipos registrados.", ln=True)
        pdf.ln(10)  # Espacio entre departamentos
 # Guardar el PDF
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    pdf_output = f"static/reportes/reporte_global_{timestamp}.pdf".replace(" ", "_")
    pdf.output(pdf_output)

    # Cerrar conexión y retornar el PDF
    conexion_db.cerrar_conexion()
    return redirect("/reporte")


@app.route('/eliminar_archivo_reporte', methods=['POST'])
def eliminar_archivo_reporte():
    if session.get('tipo_user') != 'Administrador':  # Validamos si el usuario es administrador
        return jsonify({'error': 'No tiene permisos para registrar un departamento'}), 403

    data = request.get_json()
    nombre_archivo = data.get('reporte')

    if not nombre_archivo:
        return jsonify({'success': False, 'mensaje': 'Nombre de archivo no recibido'})

    ruta_archivo = os.path.join(app.root_path, 'static', 'reportes', nombre_archivo)

    if os.path.exists(ruta_archivo):
        os.remove(ruta_archivo)
        return jsonify({'success': True, 'mensaje': 'Reporte eliminado correctamente'})
    else:
        return jsonify({'success': False, 'mensaje': 'El archivo no existe'})