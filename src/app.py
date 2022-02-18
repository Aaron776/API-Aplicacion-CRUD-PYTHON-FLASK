from flask import Flask,jsonify,request
from config import config
from flask_mysqldb import MySQL
from validaciones import *

app=Flask(__name__)

conexion=MySQL(app) #conexion a la base de datos


@app.route('/')
def index():
    return '<h1>CURSOS</h1>'



@app.route('/cursos')
def listar_cursos():
    try:
        cursor=conexion.connection.cursor() #crear un cursor
        sql='SELECT codigo,nombre,creditos,profesor,paralelo,estado FROM curso'  #consulta SQL para listar cursos
        cursor.execute(sql) #ejecutar consulta
        datos=cursor.fetchall() #obtener todos los registros con fetchall
        cursos=[] #crear una lista vacia en donde almacenaremos los registros que me vienen de la base de datos
        for lista in datos: 
            curso_existente={'codigo':lista[0],
            'nombre':lista[1],
            'creditos':lista[2],
            'profesor':lista[3],
            'paralelo':lista[4],
            'estado':lista[5]
            }
            cursos.append(curso_existente) #agregar registro a la lista vacia
        return jsonify({'cursos':cursos}) #retornar la lista de cursos en formato json
    except Exception as e:
        return  jsonify({'error':'Error al listar los cursos'}),500 #retornar mensaje de error con formato json



def obtener_curso_bd(codigo):
    try:
        cursor = conexion.connection.cursor() # obtener un curso de la bas e de datos
        sql = "SELECT codigo, nombre, creditos,profesor,paralelo,estado FROM curso WHERE codigo = '{0}'".format(codigo) #consulta SQL para listar cursos
        cursor.execute(sql) #ejecutar consulta
        datos = cursor.fetchone() #obtener u solo registro con fetchone
        if datos != None:
            curso = {'codigo': datos[0], 
                     'nombre': datos[1], 
                     'creditos': datos[2],
                     'profesor':datos[3],
                     'paralelo':datos[4],
                    'estado':datos[5]}
            return curso
        else:
            return None
    except Exception as ex:
        raise ex

@app.route('/cursos/<codigo>',methods=['GET']) #ruta para obtener un curso en especifico por medio del codigo usando el metodo GET
def buscar_curso(codigo):
    try:
        un_curso = obtener_curso_bd(codigo) # llamo a la funcion donde obtengo un registro o un curso en este caso y a ese curso lo guardo en una variable
        if un_curso != None:
            return jsonify({'curso': un_curso, 'mensaje': "Curso encontrado."})
        else:
            return jsonify({'mensaje': "Curso no encontrado."}),404
    except Exception as ex:
        return jsonify({'mensaje': "Error"}),500



@app.route('/cursos',methods=['POST']) #ruta para crear un curso usando el metodo POST
def ingresar_nuevo_curso():
    #print(request.json)
     if (validar_codigo(request.json['codigo']) and validar_nombre(request.json['nombre']) and validar_creditos(request.json['creditos']) and validar_profesor(request.json['profesor']) and validar_paralelo(request.json['paralelo']) and validar_estado(request.json['estado'])):
        try:
            curso = obtener_curso_bd(request.json['codigo'])
            if curso != None:
                return jsonify({'mensaje': "Código ya existe, no se puede duplicar."})
            else:
                cursor = conexion.connection.cursor()
                sql="INSERT INTO curso (codigo,nombre,creditos,profesor,paralelo,estado) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')".format(request.json['codigo'],request.json['nombre'],request.json['creditos'],request.json['profesor'],request.json['paralelo'],request.json['estado']) #consulta SQL para insertar un curso
                cursor.execute(sql) #ejecutar consulta
                conexion.connection.commit() #confirmar los cambios en la base de datos cuando se ingresa un registro,se lo modifica o elimina
                return jsonify({'mensaje':'Curso ingresado con exito'}),201

        except Exception as ex:
            return jsonify({'mensaje':'Error al ingresar el curso'}),500



@app.route('/cursos/<codigo>', methods=['PUT']) #ruta para modificar un curso usando el metodo PUT
def actualizar_curso(codigo):
    if (validar_codigo(codigo) and validar_nombre(request.json['nombre']) and validar_creditos(request.json['creditos'])and validar_profesor(request.json['profesor']) and validar_paralelo(request.json['paralelo']) and validar_estado(request.json['estado'])):
        try:
            curso = obtener_curso_bd(codigo)
            if curso != None:
                cursor = conexion.connection.cursor()
                sql = "UPDATE curso SET nombre = '{0}', creditos = {1},profesor = '{2}',paralelo = '{3}',estado = '{4}' WHERE codigo = '{5}'".format(request.json['nombre'], request.json['creditos'],request.json['profesor'],request.json['paralelo'],request.json['estado'], codigo) #consulta SQL para modificar un curso
                cursor.execute(sql) #ejecutar consulta
                conexion.connection.commit()  # Confirma la acción de actualización del curso.
                return jsonify({'mensaje': "Curso actualizado."}),201
            else:
                return jsonify({'mensaje': "Curso no encontrado."}),404
        except Exception as ex:
            return jsonify({'mensaje': "Error"}),500
    else:
        return jsonify({'mensaje': "Parámetros inválidos"}),500


@app.route('/cursos/<codigo>', methods=['DELETE']) #ruta para eliminar un curso usando el metodo DELETE
def eliminar_curso(codigo):
    try:
        curso = obtener_curso_bd(codigo)
        if curso != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM curso WHERE codigo = '{0}'".format(codigo)   #consulta SQL para eliminar un curso
            cursor.execute(sql)  #ejecutar consulta
            conexion.connection.commit()  # Confirma la acción de eliminación.
            return jsonify({'mensaje': "Curso eliminado."})
        else:
            return jsonify({'mensaje': "Curso no encontrado."}),404
    except Exception as ex:
        return jsonify({'mensaje': "Error"}),500


def pagina_no_econtrada(error):
    return '<h1>Pagina no encontrada</h1>', 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_econtrada)
    app.run()