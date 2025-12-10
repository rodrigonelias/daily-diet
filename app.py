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


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password: 
        #login
        user = User_Diet.query.filter_by(username=username).first() # buscando no banco o primeiro registro referente ao usuário listado

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):#user.password == password:
         login_user(user)
         print(current_user.is_authenticated)
         return jsonify({"message": "Autenticação realizada com sucesso"})
    
    return jsonify({"message": "Credenciais inválidas"}), 400


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realziado com sucesso!"})



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


@app.route('/diet_user', methods=["POST"])
def create_diet():
   print("CONTENT TYPE:", request.content_type)
   print("RAW DATA:", request.data)
   print("JSON:", request.get_json(silent=True))
   data_json = request.get_json(silent=True)
   id_usuario = data_json.get("id_usuario")
   nome = data_json.get("nome")
   descricao = data_json.get("descricao")
   data = data_json.get("data")
   hora = data_json.get("hora")
   
   if id_usuario:

    registro = Diet.query.filter_by(hora=hora).first()
    if registro: 
        dentro_dieta = "Sim" 
    else: dentro_dieta = "Não"
     
   diet_user = Diet_User(id_usuario=id_usuario, nome=nome, descricao=descricao, data=data, hora=hora, dentro_dieta=dentro_dieta)
   db.session.add(diet_user)
   db.session.commit()
   return jsonify({"message":"Dieta cadastrada com sucesso"})

@app.route("/diet_user/<int:id_dieta_usu>", methods=["PUT"])
def update_diet_user(id_dieta_usu):
   payload = request.get_json()
   diet_user = Diet_User.query.get(id_dieta_usu)

   id_user = payload.get("id_usuario")
   user = User_Diet.query.get(id_user)
   
   if not user:
      return jsonify({"message":"Usuário não encontrado"}),404

  
   if user: #and payload.get("password")
      diet_user.id_usuario = payload.get("id_usuario")
      diet_user.nome = payload.get("nome")
      diet_user.descricao = payload.get("descricao")
      diet_user.data = payload.get("data")
      diet_user.hora = payload.get("hora")
      registro = Diet.query.filter_by(hora=payload.get("hora")).first()
      
      if registro: 
        diet_user.dentro_dieta = "Sim" 
      else: diet_user.dentro_dieta = "Não"
      db.session.commit()

      return jsonify({"message":f"Dieta {id_dieta_usu} atualizado com sucesso"})
   return jsonify({"message":"Dieta não encontrada"}),404
      
@app.route("/diet_user/<int:id_dieta_usu>", methods=["DELETE"]) # deletando as informações de usuário cadastrados no banco

def delete_user(id_dieta_usu):
   payload = request.json # recupera os dados que o usuário enviou
   diet_user = Diet_User.query.get(id_dieta_usu)
   if current_user.role != 'admin':
      return jsonify({"message":"Operação não permitida"}), 403
   if payload.get("id_usuario") == current_user.id:
      return jsonify({"message":"Deleção não permitida"}), 403

   if id_dieta_usu :
      db.session.delete(id_dieta_usu)
      db.session.commit()
      return jsonify({"message":f"Dieta {id_dieta_usu} deletada com sucesso"})
   return jsonify({"message":"Dieta não encontrada"}), 404

@app.route("diet_user/<int:id_usuario>", methods=["GET"])
def listar_dietas(id_usuario):
   dietas = Diet_User.query.filter_by(id_usuario=id_usuario).all()

   resultado = []
   for d in resultado:
       resultado.append({
            "id_dieta_usuario": d.id_dieta_usuario,
            "nome": d.nome,
            "descricao": d.descricao,
            "data": d.data,
            "hora": d.hora,
            "dentro_dieta": d.dentro_dieta
        })

   return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
