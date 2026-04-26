# database.py - Base de datos usando SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Usar ruta absoluta o relativa para la BD
import os
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'ppm.db')  # Sube un nivel
# O usa ruta directa:
# DB_PATH = "ppm.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    payer = Column(String)
    amount = Column(Integer)
    description = Column(String)


Base.metadata.create_all(engine)

# Crear sesión para interactuar con la BD
Session = sessionmaker(bind=engine)

# ========== FUNCIONES PARA USUARIOS ==========

def create_user(username, email, password):
    """
    Crea un nuevo usuario en la base de datos
    Retorna: el usuario creado o None si ya existe
    """
    session = Session()
    try:
        # Verificar si ya existe un usuario con ese email
        existing_user = session.query(User).filter(User.email == email).first()
        
        if existing_user:
            session.close()
            return None
        
        # Crear nuevo usuario
        new_user = User(
            username=username,
            email=email,
            hashed_password=password
        )
        session.add(new_user)
        session.commit()
        
        # Obtener el usuario creado
        user_data = {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }
        session.close()
        return user_data
    except Exception as e:
        session.rollback()
        session.close()
        print(f"Error al crear usuario: {e}")
        return None


def get_user_by_email(email):
    """
    Obtiene un usuario por su email
    Retorna: el usuario como diccionario o None
    """
    session = Session()
    try:
        user = session.query(User).filter(User.email == email).first()
        session.close()
        if user:
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "hashed_password": user.hashed_password
            }
        return None
    except Exception as e:
        session.close()
        print(f"Error al obtener usuario: {e}")
        return None


def get_user_by_username(username):
    """
    Obtiene un usuario por su username
    Retorna: el usuario como diccionario o None
    """
    session = Session()
    try:
        user = session.query(User).filter(User.username == username).first()
        session.close()
        if user:
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "hashed_password": user.hashed_password
            }
        return None
    except Exception as e:
        session.close()
        print(f"Error al obtener usuario: {e}")
        return None


def get_all_users():
    """
    Obtiene todos los usuarios
    Retorna: lista de usuarios
    """
    session = Session()
    try:
        users = session.query(User).all()
        session.close()
        return [
            {"id": u.id, "username": u.username, "email": u.email}
            for u in users
        ]
    except Exception as e:
        session.close()
        print(f"Error al obtener usuarios: {e}")
        return []


def update_user_password(email, new_password):
    """
    Actualiza la contraseña de un usuario
    Retorna: True si se actualizó, False si no
    """
    session = Session()
    try:
        user = session.query(User).filter(User.email == email).first()
        if user:
            user.hashed_password = new_password
            session.commit()
            session.close()
            return True
        session.close()
        return False
    except Exception as e:
        session.rollback()
        session.close()
        print(f"Error al actualizar contraseña: {e}")
        return False


def user_exists(email=None, username=None):
    """
    Verifica si existe un usuario con el email o username dado
    """
    session = Session()
    try:
        query = session.query(User)
        if email:
            query = query.filter(User.email == email)
        if username:
            query = query.filter(User.username == username)
        
        exists = query.first() is not None
        session.close()
        return exists
    except Exception as e:
        session.close()
        return False


print("Base de datos inicializada correctamente")