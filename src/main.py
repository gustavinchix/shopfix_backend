"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Categoria, Producto
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#======================================
#endpoints Categorias
#======================================
#consulta y crear
@app.route('/categorias', methods=['GET','POST'])
def gestionar_categorias():

    """
        "GET": Devuelve lista de categorias
        "POST": Crear una categoria y devolver su infomacion
    """
    #Validando el methodo usado en la peticion
    if request.method == 'GET':
        #Selecciona todos los resgistros de la tabla categoria y asiganrlo a una vairale
        categorias = Categoria.query.all() #.all() para devolverlo como lista

        #Validr si hay params en la url
        name = request.args.get("categoryname")
        if name is not None:
            categorias_filtradas = filter(lambda categoria: name in categoria.nombre, categorias)
        else:
            categorias_filtradas = categorias
        #Serializar la lista
        categorias_serializadas=list(map(lambda categoria: categoria.serializar(), categorias))               
        #devolver lista de categorias serializadas
        return jsonify(categorias_serializadas), 200
    else:
        #Crea una variable y asigna el diccionario de datos para crear la categoria
        insumo_categoria = request.json
        if insumo_categoria is None:
            return jsonify ({
                "resultado": "No envio la informacion para crear la categoria"
            }),400
        if (
            "nombre" not in insumo_categoria or 
            "descripcion" not in insumo_categoria or 
            "icono" not in insumo_categoria
            ):
            return jsonify({
                "resultado": "Debe indicar un nombre, descripcion e icono para crear la categoria"
            }),400
        #Validar que no venga vacio
        if (
            insumo_categoria["nombre"] == "" or
            insumo_categoria["descripcion"] == "" or
            insumo_categoria["icono"] == ""

        ):
            return jsonify({
                "resultado": "Debe indicar un nombre e icono para crear la categoria"
            })
        nueva_categoria = Categoria.registrar_categoria(
            insumo_categoria["nombre"],
            insumo_categoria["descripcion"],
            insumo_categoria["icono"]
        )
        #agregar a la base de datos
        db.session.add(nueva_categoria)
        try:
            db.session.commit()
            #Si el commit es exitoso se devuelve la ifo de nueva categoria
            return jsonify(nueva_categoria.serializar()),201
        except Exception as error:
            db.session.rollback()
            print(f"{error.args} {type(error)}")
            return jsonify({
                "resultado": f"{error.args}"
            }), 500

#Consulta, edicion, borrar
@app.route('/categorias/<categoria_id>', methods=['GET','PUT','DELETE'])
def rud_categorias(categoria_id):
    #Crear una vairable y asignar una cat en especifico
    categoria = Categoria.query.get(categoria_id)
    #Validar si la categoria existe
    if isinstance(categoria, Categoria):
        if request.method == 'GET':            
            #devolver lista de categorias serializadas
            return jsonify(categoria.serializar()), 200
        elif request.method == 'PUT':
            #recuperar diccionar del body del request
            diccionario = request.json
            #actualizar propiedades que vengan en el dicc
            categoria.modificar_categoria(diccionario)
            #guardar cambio en BD, hacer commit
            try:
                db.session.commit()
                #devolver la categoria serializada
                return jsonify(categoria.serializar()), 200
            except Exception as error:
                db.session.rollback()
                print(f"{error.args} {type(error)}")
                return jsonify({
                    "resultado": f"{error.args}"
                }), 500
        else:
            #remover la categoria de  la BD, hacer commit, return 204
            db.session.delete(categoria)
            try:
                db.session.commit()
                #devolver delete exitoso
                return jsonify({
                    "resultado": "Se ha eliminado la categoria exitosamente"
                }), 200
            except Exception as error:
                db.session.rollback()
                print(f"{error.args} {type(error)}")
                return jsonify({
                    "resultado": f"{error.args}"
                }), 500
    else:
        return jsonify({
            "resultado":"La categoria no existe"
        }), 404


#======================================
#endpoints usuarios
#======================================
@app.route('/users/register', methods=['POST'])
def registar_usuario():
    if request.method == 'POST':
        insumo_usuario = request.json
        if insumo_usuario is None:
            return jsonify ({
                "resultado": "No envio la informacion para crear el producto"
            }),400
        if (
            "email" not in insumo_usuario or 
            "password" not in insumo_usuario
            ):
            return jsonify({
                "resultado": "Debe indicar un email y password"
            }),400
        #Validar que no venga vacio
        if (
            insumo_usuario["email"] == "" or
            insumo_usuario["password"] == "" 
        ):
            return jsonify({
                "resultado": "Debe indicar un email y password"
            })
        nuevo_usuario = User.registro_usuario(
            insumo_usuario["email"],
            insumo_usuario["password"]
        )
        #agregar a la base de datos
        db.session.add(nuevo_usuario)
        try:
            db.session.commit()
            #Si el commit es exitoso se devuelve la ifo de nueva categoria
            return jsonify(nuevo_usuario.serialize()),201
        except Exception as error:
            db.session.rollback()
            print(f"{error.args} {type(error)}")
            return jsonify({
                "resultado": f"{error.args}"
            }), 500


#======================================
#endpoints productos
#========================================
@app.route('/producto', methods=['GET'])
def chequear_producto():
     productos = Producto.query.all()
     todos_productos = list(map(lambda x: x.serialize(), productos))

     return jsonify(todos_productos), 200

@app.route('/producto', methods=['POST'])
def registrar_producto():

     request_body_producto = request.get_json()

     producto1 = Producto(titulo=request_body_producto["titulo"], descripcion=request_body_producto["descripcion"], imagen=request_body_producto["imagen"], precio=request_body_producto["precio"])
     db.session.add(producto1)
     db.session.commit()

     return jsonify(request_body_producto), 200

@app.route('/producto/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    
     request_body_producto = request.get_json()

     producto1 = Producto.query.get(producto_id)
     if producto1 is None:
         raise APIException('Producto not found', status_code=404)

     if "titulo" in request_body_producto:
         producto1.titulo = request_body_producto["titulo"]
     if "descripcion" in request_body_producto:
         producto1.descripcion = request_body_producto["descripcion"]
     if "imagen" in request_body_producto:
         producto1.imagen = request_body_producto["imagen"]
     if "precio" in request_body_producto:
         producto1.precio = request_body_producto["precio"]

     db.session.commit()

     return jsonify(request_body_producto), 200

@app.route('/producto/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    
     request_body_producto = request.get_json()

     producto1 = Producto.query.get(producto_id)
     if producto1 is None:
         raise APIException('Producto not found', status_code=404)

     db.session.delete(producto1)
     db.session.commit()

     return jsonify(f"Producto con id: {producto_id} eliminado exitosamente!"), 200


#this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
