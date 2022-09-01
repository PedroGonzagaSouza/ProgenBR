from db import db
from controllers.embalagem import Embalagem, EmbalagemList
from controllers.produto import Produto, ProdutoList
from server.instance import server



api = server.api
app = server.app

api.add_resource(EmbalagemList, '/embalagem/<int:id>')
api.add_resource(Embalagem, '/embalagem')

api.add_resource(Produto, '/produto')
api.add_resource(ProdutoList, '/produto/<int:id>')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    server.run()
    