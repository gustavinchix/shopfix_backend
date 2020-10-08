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
#endpoints Usuario
#======================================
@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {

        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

#======================================
#endpoints productos
#======================================
#consulta y crear
@app.route('/productos', methods=['GET','POST'])
def chequear_producto():
    #Validando el methodo usado en la peticion
    if request.method == 'GET':
        #Selecciona todos los resgistros de la tabla categoria y asiganrlo a una vairale
        productos = Producto.query.all() #.all() para devolverlo como lista

        #Validr si hay params en la url
        name = request.args.get("productname")
        if name is not None:
            productos_filtrados = filter(lambda producto: name in producto.name, productos)
        else:
            productos_filtrados = productos
        #Serializar la lista
        productos_serializados=list(map(lambda producto: producto.serialize(), productos))               
        #devolver lista de categorias serializadas
        return jsonify(productos_serializados), 200
    else:
        #Crea una variable y asigna el diccionario de datos para crear la categoria
        insumo_producto = request.json
        if insumo_producto is None:
            return jsonify ({
                "resultado": "No envio la informacion para crear el producto"
            }),400
        if (
            "titulo" not in insumo_producto or 
            "descripcion" not in insumo_producto or 
            "precio" not in insumo_producto or
            "imagen" not in insumo_producto or
            "categoria_id" not in insumo_producto 
            ):
            return jsonify({
                "resultado": "Debe indicar un titulo, descripcion, precio, imagen y categoria para crear el producto"
            }),400
        #Validar que no venga vacio
        if (
            insumo_producto["titulo"] == "" or
            insumo_producto["descripcion"] == "" or
            insumo_producto["precio"] == "" or
            insumo_producto["imagen"] == "" or
            insumo_producto["categoria_id"] == "" 
        ):
            return jsonify({
                "resultado": "Debe indicar un titulo, descripcion, precio, imagen y categoria para crear el producto"
            })
        nuevo_producto = Producto.registrar_producto(
            insumo_producto["titulo"],
            insumo_producto["descripcion"],
            insumo_producto["precio"],
            insumo_producto["imagen"],
            insumo_producto["categoria_id"]
        )
        #agregar a la base de datos
        db.session.add(nuevo_producto)
        try:
            db.session.commit()
            #Si el commit es exitoso se devuelve la ifo de nueva categoria
            return jsonify(nuevo_producto.serialize()),201
        except Exception as error:
            db.session.rollback()
            print(f"{error.args} {type(error)}")
            return jsonify({
                "resultado": f"{error.args}"
            }), 500

#Consulta, edicion, borrar
@app.route('/productos/<producto_id>', methods=['GET','PATCH','DELETE'])
def rud_productos(producto_id):
    #Crear una vairable y asignar una cat en especifico
    producto = Producto.query.get(producto_id)
    #Validar si la producto existe
    if isinstance(producto, Producto):
        if request.method == 'GET':            
            #devolver lista de productos serializadas
            return jsonify(producto.serialize()), 200
        elif request.method == 'PATCH':
            #recuperar diccionar del body del request
            diccionario = request.json
            #actualizar propiedades que vengan en el dicc
            producto.modificar_producto(diccionario)
            #guardar cambio en BD, hacer commit
            try:
                db.session.commit()
                #devolver la producto serializada
                return jsonify(producto.serialize()), 200
            except Exception as error:
                db.session.rollback()
                print(f"{error.args} {type(error)}")
                return jsonify({
                    "resultado": f"{error.args}"
                }), 500
        else:
            #remover la producto de  la BD, hacer commit, return 204
            db.session.delete(producto)
            try:
                db.session.commit()
                #devolver delete exitoso
                return jsonify({
                    "resultado": "Se ha eliminado la producto exitosamente"
                }), 200
            except Exception as error:
                db.session.rollback()
                print(f"{error.args} {type(error)}")
                return jsonify({
                    "resultado": f"{error.args}"
                }), 500
    else:
        return jsonify({
            "resultado":"La producto no existe"
        }), 404

#======================================
#endpoints productos
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


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
