from db import db



#Criando table Produto
class ProdutoModel(db.Model):
    __tablename__ = 'Produtos'
    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
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
        return f'ProdutoModel(nome={self.nome})'
