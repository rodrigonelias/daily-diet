from database import db
from flask_login import UserMixin

class Diet_User(db.Model, UserMixin):
    # id (int), username(text), password (text)
    id_dieta_usuario = db.Column(db.Integer, primary_key=True) # definindo a coluna da tabela
    id_usuario = db.Column(db.Integer, db.ForeignKey('user.id')) 
    nome = db.Column(db.String(80), nullable=False, unique=True)
    descricao = db.Column(db.String(80), nullable=False)
    data = db.Column(db.String(80), nullable=False)
    hora = db.Column(db.String(80), nullable=False) 
    dentro_dieta = db.Column(db.String(80), nullable=False)

class Diet(db.Model, UserMixin):
    id_dieta = db.Column(db.Integer, primary_key=True)
    nome_dieta = db.Column(db.String(80), nullable=False, unique=True)
    periodo = db.Column(db.String(80), nullable=False, unique=True)
    hora = db.Column(db.String(80), nullable=False)
    itens = db.Column(db.String(200), nullable=False, unique=True)
    