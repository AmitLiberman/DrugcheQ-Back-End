from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from DB import DB

app = Flask(__name__)
api = Api(app)


 class InteractionCheck(Resource):
    def get(self):
        drugs_sent = request.args
        for key,value in drugs_sent.items():
            print(key)
        # data = request.get_json(force=True)
        # data_base = DB()
        # data_base.creat_table()
        # data_base.close_connection()
        return drugs_sent


api.add_resource(InteractionCheck, '/check')

if __name__ == '__main__':
    app.run(debug=True)
