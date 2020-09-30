from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(25), unique=True, nullable=False)
    descripcion = db.Column(db.String(80), nullable=False)
    icono = db.Column(db.String(80), unique=True, nullable=False)
    
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
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "icono": self.icono
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
            "email": self.email,
            # do not serialize the password, its a security breach
        }