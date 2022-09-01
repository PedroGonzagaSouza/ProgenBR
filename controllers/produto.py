from flask import request
from flask_restx import Resource, fields


from db import db
from models.models import ProdutoModel
from server.instance import server

from gera_response import gera_response

produtos_ns = server.produtos_ns

'''======================================== Produtos ======================================================='''
produto = produtos_ns.model('Produto', {
    'descricao': fields.String(description='Descrição do produto.'),
    'custo': fields.Float(),
    'preco_venda': fields.Float(),
    'cod_barras': fields.Integer(),
    'embalagem': fields.String()
})


class Produto(Resource):
#Para retornar todos os produtos
    def get_all():
        produto_objetos = ProdutoModel.query.all()
        produto_json = [produto.to_json() for produto in produto_objetos]
        return gera_response(200, 'produto', produto_json)

    # Selecionar Individual

    def get_id(id):
            produto_objeto = ProdutoModel.query.filter_by(id=id).first()
            produto_json = produto_objeto.to_json()
            return gera_response(200, "produto", produto_json)


    @produtos_ns.expect(produto)
    @produtos_ns.doc('Adicionar novo produto.')
    def post():
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
    def put(id):
        produto_objeto = ProdutoModel.query.filter_by(id=id).first()
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
    def delete(id):
        produto_objeto = ProdutoModel.query.filter_by(id=id).first()

        try:
            db.session.delete(produto_objeto)
            db.session.commit()
            return gera_response(200, "Produto", produto_objeto.to_json(), "Deletado com sucesso")
        except Exception as e:
            print('Erro', e)
            return gera_response(400, "Produto", {}, "Erro ao deletar")

