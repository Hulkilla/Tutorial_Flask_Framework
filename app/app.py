from flask import Flask, render_template, request, redirect, url_for, jsonify
# pip install flask-mysqldb --> para tratar con bbdd dentro de la app
from flask_mysqldb import MySQL
app = Flask(__name__)

# Conexión MySQL
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Cuatro4444'
app.config['MYSQL_DB'] = 'fermentation'
# Igual puedo conectarme a mis tablas
try: 
    conexion = MySQL(app) #Conexión entre la bbdd y la app
    print("Conexión correcta a la bbdd")
except:
    print("No se ha conectado a la bbdd")

@app.before_request
def before_request():
    print("Antes de la petición")
#Acción antes de la petición

@app.after_request
def after_request(response):
    print("Despues de la petición")
    return response
#Acción después de la petición

@app.route("/")
def index():
    cursos = ['PHP', 'Python', 'Java', 'Kotlin', 'Dart', 'JavaScript']
    data = {
        'titulo': 'Index123',
        'bienvenida': '¡Saludos!',
        'cursos': cursos,
        'numero_cursos': len(cursos)
    }
    return render_template("index.html", data = data)


@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data = {
        'titulo': 'contacto',
        'nombre': nombre,
        'edad': edad
    }
    return render_template('contacto.html', data=data)



def query_string():
    print(request) #se ha utilizado un get
    print(request.args)
    print(request.args.get("param1")) #Nos estamos trayendo en parametro1 de la url
    print(request.args.get("param2"))
    return "todo"

@app.route('/cursos')
def listar_cursos():
    data={}
    try:
        cursor=conexion.connection.cursor()
        sql = "SELECT * FROM fermentation.substrato"
        cursor.execute(sql)
        cursos=cursor.fetchall()
        data['cursos']=cursos
        data['mensaje'] = 'Exito'
    except Exception as ex:
        data['mensaje']=f'Error: {ex}'
    return jsonify(data)


def pagina_no_encontrada(error):
    # return render_template('404.html'), 404
    return redirect(url_for('index'))
    ## Aqui tenemos dos opciones, o una página de error o redirigir a la pagina principal

if __name__=='__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug = True, port = 5000)