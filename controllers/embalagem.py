from flask import request
from flask_restx import Resource, fields


from db import db
from models.models import EmbalagemModel
from server.instance import server

from gera_response import gera_response

embalagem_ns = server.embalagem_ns

#Esboço para o método post da API
embalagem = embalagem_ns.model('Embalagem', {
    'sigla': fields.String(description= 'Sigla da embalagem. "UN" "PCT"'),
    'descricao': fields.String(description= 'Descrição da embalagem.')    
})


'''======================================== Embalagens ======================================================='''
class Embalagem(Resource):
    #Fazendo página index para retornar todas as embalagens
    def get_all():
        embalagem_objetos = EmbalagemModel.query.all()
        embalagem_json = [embalagem.to_json() for embalagem in embalagem_objetos]
        return gera_response(200, 'embalagem', embalagem_json)

    # Selecionar Individual
    def get_id(id):
            embalagem_objeto = EmbalagemModel.query.filter_by(id=id).first()
            embalagem_json = embalagem_objeto.to_json()
            return gera_response(200, "embalagem", embalagem_json)

    @embalagem_ns.expect(embalagem)
    @embalagem_ns.doc('Adicionar novo produto.')
    def embalagem_post():
        body = request.get_json()

        try:
            embalagem = EmbalagemModel(sigla=body['sigla'], descricao=body['descricao'])
            db.session.add(embalagem)
            db.session.commit()
            return gera_response(201, 'embalagem ', embalagem.to_json(), ' adicionada.')
        except Exception as e:
            print(e)
            return gera_response(400, 'erro')

    # Atualizar
    def put(id):
        embalagem_objeto = EmbalagemModel.query.filter_by(id=id).first()
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
    def delete(id):
        embalagem_objeto = EmbalagemModel.query.filter_by(id=id).first()

        try:
            db.session.delete(embalagem_objeto)
            db.session.commit()
            return gera_response(200, "embalagem", embalagem_objeto.to_json(), "Deletado com sucesso")
        except Exception as e:
            print('Erro', e)
            return gera_response(400, "embalagem", {}, "Erro ao deletar")