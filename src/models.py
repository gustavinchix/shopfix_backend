from flask_sqlalchemy import SQLAlchemy
import os
from base64 import b64encode, b64decode
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(25), unique=True, nullable=False)
    descripcion = db.Column(db.String(80), nullable=False)
    icono = db.Column(db.String(80), nullable=False)
    productos = db.relationship('Producto', cascade="all, delete-orphan", lazy=True)

    def __str__(self):
        return f'{self.nombre}'

    def __init__(self,nombre,descripcion,icono):
        """crea y devuelve las instancias de la clase"""
        self.nombre = nombre
        self.descripcion = descripcion
        self.icono = icono

    
    @classmethod
   
    def registrar_categoria(cls, nombre, descripcion, icono):
        """
            normaliza insumos nombre e icono
            crea un objeto de la clase Categoria con dichos insumos
        """
        nueva_categoria = cls(
            nombre.lower().capitalize(),
            descripcion,
            icono
        )
        return nueva_categoria
    
    def modificar_categoria(self,diccionario):
        if "nombre" in diccionario:
            self.nombre = diccionario["nombre"]
        if "descripcion" in diccionario:
            self.descripcion = diccionario["descripcion"]
        if "icono" in diccionario:
            self.icono = diccionario["icono"]
        return True

    def serializar(self):
        return{
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "icono": self.icono
        }

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), unique=False, nullable=False)
    descripcion = db.Column(db.String(100), unique=False, nullable=False)
    precio = db.Column(db.Integer, unique=False, nullable=False)
    imagen = db.Column(db.String(150), unique=False, nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey(Categoria.id))


    def __init__(self, titulo, descripcion, precio, imagen, categoria_id):
        """crea y devuelve las instancias de la clase"""
        self.titulo = titulo
        self.descripcion = descripcion
        self.precio = precio
        self.imagen = imagen
        self.categoria_id = categoria_id

    def __repr__(self):
        return '<Producto %s>' % self.titulo
  
    @classmethod
    def registrar_producto(cls,titulo, descripcion, precio, imagen, categoria_id):
        nuevo_producto= cls(
            titulo.lower().capitalize(), 
            descripcion, 
            precio, 
            imagen, 
            categoria_id
            )
        return nuevo_producto

    def modificar_producto(self,diccionario):        
        if "titulo" in diccionario:
            self.titulo = diccionario["titulo"]
        if "descripcion" in diccionario:
            self.descripcion = diccionario["descripcion"]
        if "precio" in diccionario:
            self.precio = diccionario["precio"]
        if "imagen" in diccionario:
            self.imagen = diccionario["imagen"]
        if "categoria_id" in diccionario:
            self.categoria_id = diccionario["categoria_id"]
        return True

    def serialize(self):        
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "imagen": self.imagen,
            "precio": self.precio,
            "categoria_id": self.categoria_id
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean(), unique=False, nullable=False)
    password_hash = db.Column(db.String(250), unique=False, nullable=False)
    salt = db.Column(db.String(16), nullable=False)

    def __init__(self,email,is_admin,password_hash):
        self.email = email
        self.is_admin = is_admin
        self.salt = b64encode(os.urandom(4)).decode("utf-8")
        self.set_password(password_hash)

    def set_password(self, password_hash):
        self.password_hash = generate_password_hash(f"{password_hash}{self.salt}")

    def check_password(self, password_hash):
        """verifica el match entre los password"""
        return check_password_hash(self.password_hash, f"{password_hash}{self.salt}")

    def __repr__(self):
        return '<User %s>' % self.email

    @classmethod
    def registro_usuario(cls,email,password,is_admin):
        nuevo_usuario =cls(
            email.lower(),
            password,
            is_admin
        )
        return nuevo_usuario

    def serialize(self):
        return {
            "email": self.email.lower(),
            "is_admin": self.is_admin
        }
    