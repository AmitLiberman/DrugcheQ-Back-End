from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
 # from DB import DB
import drug_api

app = Flask(__name__)
cors = CORS(app)
api = Api(app)



class InteractionCheck(Resource):
    def get(self):
        drugs_sent = request.args
        interaction_dict = drug_api.find_interaction(list(drugs_sent.keys()))
        # data = request.get_json(force=True)
        # data_base = DB()
        # data_base.creat_table()
        # data_base.close_connection()
        return jsonify(interaction_dict)


api.add_resource(InteractionCheck, '/check')


if __name__ == '__main__':
    app.run(debug=True)
