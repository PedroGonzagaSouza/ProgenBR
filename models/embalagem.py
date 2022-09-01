from db import db



#Criando Model Embalagem
class EmbalagemModel(db.Model):
    __tablename__ = 'Embalagens'
    id = db.Column(db.Integer(), primary_key=True)
    sigla = db.Column(db.String(5), nullable=False)
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
        return f'EmbalagemModel(nome={self.sigla})'
