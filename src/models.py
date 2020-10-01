from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(25), unique=True, nullable=False)
    descripcion = db.Column(db.String(80), nullable=False)
    icono = db.Column(db.String(80), unique=True, nullable=False)
    productos = db.relationship('Producto', lazy=True)

    def __repr__(self):
        return '<Categoria %r>' % self.nombre
    
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

    def serializar(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "icono": self.icono
        }

    def modificar_categoria(self,diccionario):
        if "nombre" in diccionario:
            self.nombre = diccionario["nombre"]
        if "descripcion" in diccionario:
            self.descripcion = diccionario["descripcion"]
        if "icono" in diccionario:
            self.icono = diccionario["icono"]
        return True


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), unique=False, nullable=False)
    descripcion = db.Column(db.String(100), unique=False, nullable=False)
    categoria_id = db.Column(db.Integer(), db.ForeignKey(Categoria.id))

    def __repr__(self):
        return '<Producto %r>' % self.titulo

    def serialize(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descripcion": self.descripcion
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }