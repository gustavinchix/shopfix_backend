from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(25), unique=True, nullable=False)
    descripcion = db.Column(db.String(80), nullable=False)
    icono = db.Column(db.String(80), nullable=False)
    productos = db.relationship('Producto', lazy=True)

    def __repr__(self):
        return '<Categoria %s>' % self.nombre
    
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
            "icono": self.icono,
            "productos_en_categoria": list(map(lambda x: x.serialize(), self.productos))
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
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean(), unique=False, nullable=False)

    def __init__(self,email,password,is_admin):
        self.email = email
        self.password = password
        self.is_admin = is_admin

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
    