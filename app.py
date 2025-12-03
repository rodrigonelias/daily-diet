from flask import Flask, request, jsonify
from database import db
from models.user import User_Diet
from models.diet import Diet_User, Diet
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key" #secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3307/flask-crud'#'sqlite:///database.db' # URI - Caminho onde o banco será conectado

login_manager = LoginManager()
db.init_app(app) # iniciando o banco de dados no apicativo
login_manager.init_app(app)

login_manager.login_view = 'login' # vai pegar a rota de login 


@login_manager.user_loader
def load_user(user_id): # recuperar o nosso objeto cadastrado no banco de dados
   return User_Diet.query.get(user_id)

@app.route('/user', methods=["POST"])
def create_user():
   data = request.json # recuperar o que o usuário envia pelo Postman
   username = data.get("username")
   password = data.get("password")

   if username and password:
      hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
      user = User_Diet(username=username, password=hashed_password, role='user')
      db.session.add(user)
      db.session.commit()
      return jsonify({"message":"Usuário cadastrado com sucesso"})
   return jsonify({"message":"Dados inválidos"}), 400


if __name__ == '__main__':
    app.run(debug=True)
