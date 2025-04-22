from flask import Flask, jsonify, request, send_file, url_for, render_template, redirect, flash
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
db = SQLAlchemy(app)
CORS(app, origins=['http://127.0.0.1:5500'])

# -------------------
# MODELOS
# -------------------

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'preco': self.preco,
        }

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    administrador = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'administrador': self.administrador,
            '_links': {
                'self': url_for('get_usuario', usuario_id=self.id, _external=True),
                'update': url_for('update_usuario', usuario_id=self.id, _external=True),
                'delete': url_for('delete_usuario', usuario_id=self.id, _external=True),
            }
        }

with app.app_context():
    db.create_all()

# -------------------
# ROTAS DE PRODUTO
# -------------------

@app.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    return jsonify([p.serialize() for p in produtos])

@app.route('/produtos/<int:produto_id>', methods=['GET'])
def get_produto(produto_id):
    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({'mensagem': 'Produto não encontrado'}), 404
    return jsonify(produto.serialize())

@app.route('/produtos', methods=['POST'])
def create_produto():
    dados = request.get_json()
    novo = Produto(nome=dados['nome'], preco=dados['preco'])
    db.session.add(novo)
    db.session.commit()
    return jsonify(novo.serialize()), 201

@app.route('/produtos/<int:produto_id>', methods=['PUT'])
def update_produto(produto_id):
    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({'mensagem': 'Produto não encontrado'}), 404
    dados = request.get_json()
    produto.nome = dados['nome']
    produto.preco = dados['preco']
    db.session.commit()
    return jsonify(produto.serialize())

@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({'mensagem': 'Produto não encontrado'}), 404
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'mensagem': 'Produto excluído com sucesso'}), 200

# -------------------
# ROTAS DE USUARIO
# -------------------

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.serialize() for u in usuarios])

@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    return jsonify(usuario.serialize())

@app.route('/usuarios', methods=['POST'])
def create_usuario():
    dados = request.get_json()
    novo = Usuario(nome=dados['nome'], email=dados['email'], telefone=dados['telefone'], senha=dados['senha'], administrador=dados.get('administrador', False))
    db.session.add(novo)
    db.session.commit()
    return jsonify(novo.serialize()), 201

@app.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    dados = request.get_json()
    usuario.nome = dados['nome']
    usuario.email = dados['email']
    usuario.telefone = dados['telefone']
    usuario.senha = dados['senha']
    usuario.administrador = dados.get('administrador', usuario.administrador)
    db.session.commit()
    return jsonify(usuario.serialize())

@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário excluído com sucesso'}), 200

# -------------------
# ROTA DE LOGIN
# -------------------

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados['email']
    senha = dados['senha']

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and usuario.senha == senha:  # Verifica diretamente a senha sem hash
        return jsonify({
            'success': True,
            'usuario': usuario.serialize()
        })
    else:
        return jsonify({
            'success': False,
            'mensagem': 'Email ou senha inválidos'
        }), 401


@app.route('/login-user', methods=['POST'])
def login_user():
    if request.is_json:
        # Requisição JSON
        dados = request.get_json()  # Obtém dados no formato JSON
    else:
        # Requisição de formulário
        dados = request.form.to_dict()  # Converte os dados do formulário para um dicionário

    email = dados.get('email')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({'mensagem': 'Email e senha são obrigatórios!'}), 400

    # Verificar se o email e senha correspondem a um usuário
    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario or usuario.senha != senha:  # Comparando as senhas diretamente
        return jsonify({'mensagem': 'Email ou senha inválidos!'}), 401

    # Se o login for bem-sucedido, retornar informações do usuário
    return jsonify({
        'mensagem': 'Login bem-sucedido',
        'administrador': usuario.administrador
    }), 200

@app.route('/login-user', methods=['GET'])
def login_page():
    return render_template('login.html')

# -------------------
# ROTA DE PÓS-LOGIN
# -------------------

# Página do Administrador
@app.route('/admin-page')
def admin_page():
    return render_template('admin_page.html')

# Página do Usuário Normal
@app.route('/user-page')
def user_page():
    return render_template('user_page.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login_user'))

# -------------------
# MAIN
# -------------------
if __name__ == '__main__':
    app.run(debug=True)