from flask import Flask, Blueprint
from flask_restx import Api

class Server():
    def __init__(self):
        self.app = Flask(__name__)

        self.blueprint = Blueprint('api', __name__, url_prefix='/api')

        self.api = Api(self.blueprint,
         title='API_ProgenBR',
         doc='/docs')
        self.app.register_blueprint(self.blueprint)

        self.app.config['SQLALCHEMY_DATABASE_URI']='postgresql://glqlulliosqsci:56b2644bd6dfd4bcb17e8de2bac1b11154bf6739c46b00de1a7f8c347375c766@ec2-44-207-126-176.compute-1.amazonaws.com:5432/d6hdqr5u742pmj'
        #self.app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:201019@localhost:3306/api_produtos'
        self.app.config['PROPAGATE_EXCEPTIONS'] = True
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


        self.embalagem_ns = self.embalagem_ns()
        self.produtos_ns = self.produtos_ns()
    

    #Namespaces
    def produtos_ns(self):
        return self.api.namespace(name='Produtos', description='Produtos', path='/produtos')

    def embalagem_ns(self):
        return self.api.namespace(name='Embalagens', description='Embalagens', path='/embalagens')

    
    #Rodar a api
    def run(self):
        self.app.run(
            port=5000,
            host='0.0.0.0',
            debug=True )

server = Server()