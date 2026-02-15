import os

class Config:
    SECRET_KEY = 'clave-secreta-super-pro'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///inventario.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  