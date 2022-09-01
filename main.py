from cmath import e
from flask import Flask,Response , request # Para fazer o sistema web
from flask_sqlalchemy import SQLAlchemy #Para acessar o banco de dados
import json

# Instanciando o Flask
app = Flask(__name__) 

#Configurando caminho para banco de dados
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:201019@localhost:3306/api_produtos'

# Instanciando o SQLAlchemy como db, nas configs do app Flask
db = SQLAlchemy(app)

''' ============================== Embalagem ===================================== '''

#Criando Model Embalagem
class Embalagem(db.Model):
    __tablename__ = 'Embalagens'
    id = db.Column(db.Integer(), primary_key=True)
    sigla = db.Column(db.String(5), nullable=False, unique=True)
    descricao = db.Column(db.String(200))


    #Método construtor da classe para o banco de dados
    def __init__(self, sigla, descricao):
        self.sigla = sigla
        self.descricao = descricao

        #Retornar JSON
    def to_json(self):
        return {
            "id": self.id,
            "sigla": self.sigla,
            "descricao": self.descricao
        }

    #Função para criar banco de dados dentro do app
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

            #Método para representar através de string
    def __repr__(self):
        return f'Embalagem(nome={self.sigla})'


#Criando table Produto
class Produto(db.Model):
    __tablename__ = 'Produtos'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.String(100), nullable=False)
    custo = db.Column(db.Float(), nullable=False)
    preco_venda = db.Column(db.Float(), nullable=False)
    cod_barras = db.Column(db.Integer(), nullable=False, unique=True)
    embalagem = db.Column(db.String(20), nullable=False)


    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'custo': self.custo,
            'preco_venda': self.preco_venda,
            'cod_barras': self.cod_barras,
            'embalagem': self.embalagem
        }

    #Método construtor da classe para o banco de dados
    def __init__(self, nome, descricao, custo, preco_venda, cod_barras, embalagem):
        self.nome = nome
        self.descricao = descricao
        self.custo = custo
        self.preco_venda = preco_venda
        self.cod_barras = cod_barras
        self.embalagem = embalagem

    #Função para criar banco de dados dentro do app
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


    #Método para representar através de string
    def __repr__(self):
        return f'Produto(nome={self.nome})'

db.create_all()


''' ===================================Rotas e métodos Flask'========================= '''
'''======================================== Embalagens ======================================================='''
#Fazendo página index para retornar todas as embalagens
@app.route('/embalagem', methods=['GET'])
def index():
    embalagem_objetos = Embalagem.query.all()
    embalagem_json = [embalagem.to_json() for embalagem in embalagem_objetos]
    return gera_response(200, 'embalagem', embalagem_json)

# Selecionar Individual
@app.route("/embalagem/<id>", methods=["GET"])
def embalagem_getById(id):
        embalagem_objeto = Embalagem.query.filter_by(id=id).first()
        embalagem_json = embalagem_objeto.to_json()
        return gera_response(200, "embalagem", embalagem_json)

@app.route('/embalagem', methods=['POST'])
def embalagem_post():
    body = request.get_json()

    try:
        embalagem = Embalagem(sigla=body['sigla'], descricao=body['descricao'])
        db.session.add(embalagem)
        db.session.commit()
        return gera_response(201, 'embalagem ', embalagem.to_json(), ' adicionada.')
    except Exception as e:
        print(e)
        return gera_response(400, 'erro')

# Atualizar
@app.route("/embalagem/<id>", methods=["PUT"])
def embalagem_put(id):
    embalagem_objeto = Embalagem.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('sigla' in body):
            embalagem_objeto.sigla = body['sigla']
        if('descricao' in body):
            embalagem_objeto.descricao = body['descricao']
        
        db.session.add(embalagem_objeto)
        db.session.commit()
        return gera_response(200, "Embalagem", embalagem_objeto.to_json(), "Atualizada com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Embalagem", {}, "Erro ao atualizar")

# Deletar
@app.route("/embalagem/<id>", methods=["DELETE"])
def embalagem_delete(id):
    embalagem_objeto = Embalagem.query.filter_by(id=id).first()

    try:
        db.session.delete(embalagem_objeto)
        db.session.commit()
        return gera_response(200, "embalagem", embalagem_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "embalagem", {}, "Erro ao deletar")

'''======================================== Produtos ======================================================='''

#Para retornar todos os produtos
@app.route('/produto', methods=['GET'])
def produto_get_all():
    produto_objetos = Produto.query.all()
    produto_json = [produto.to_json() for produto in produto_objetos]
    return gera_response(200, 'produto', produto_json)

# Selecionar Individual
@app.route("/produto/<id>", methods=["GET"])
def produto_get_Id(id):
        produto_objeto = Produto.query.filter_by(id=id).first()
        produto_json = produto_objeto.to_json()
        return gera_response(200, "produto", produto_json)


@app.route('/produto', methods=['POST'])
def produto_post():
    body = request.get_json()
    try:
        produto = Produto(nome=body['nome'],
             descricao=body['descricao'],
              custo=body['custo'],
               preco_venda=body['preco_venda'],
               cod_barras=body['cod_barras'],
               embalagem=body['embalagem']
               )
        db.session.add(produto)
        db.session.commit()
        return gera_response(201, 'produto ', produto.to_json(), ' adicionado.')
    except Exception as e:
        print(e)
        return gera_response(400, 'erro')

# Atualizar
@app.route("/produto/<id>", methods=["PUT"])
def produto_put(id):
    produto_objeto = Produto.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if('nome' in body):
            produto_objeto.nome = body['nome']
        if('descricao' in body):
            produto_objeto.descricao = body['descricao']
        if('custo' in body):
            produto_objeto.custo = body['custo']
        if('preco_venda' in body):
            produto_objeto.preco_venda = body['preco_venda']
        if('cod_barras' in body):
            produto_objeto.cod_barras = body['cod_barras']
        if('embalagem' in body):
            produto_objeto.embalagem = body['embalagem']

        db.session.add(produto_objeto)
        db.session.commit()
        return gera_response(200, "Produto", produto_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Produto", {}, "Erro ao atualizar")

# Deletar
@app.route("/produto/<id>", methods=["DELETE"])
def produto_delete(id):
    produto_objeto = Produto.query.filter_by(id=id).first()

    try:
        db.session.delete(produto_objeto)
        db.session.commit()
        return gera_response(200, "Produto", produto_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "Produto", {}, "Erro ao deletar")




#Método para simplificar as responses
def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)