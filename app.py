from flask import jsonify

from db import db
from controllers.embalagem import Embalagem
from controllers.produto import Produto

from server.instance import server



api = server.api
app = server.app

api.add_resource(Embalagem, '/embalagens/<int:id>')


api.add_resource(Produto, '/produtos/<int:id>')


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    db.init_app(app)
    server.run()
    