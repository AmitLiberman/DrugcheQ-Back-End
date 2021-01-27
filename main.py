from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
from DB import DB
from InteractionCheck.DrugIdentifier import DrugIdentifier
from InteractionCheck.DrugInteractions import DrugInteractions

app = Flask(__name__)
cors = CORS(app)
api = Api(app)


class InteractionCheck(Resource):
    def get(self):
        drugs_sent = request.args
        # interaction_dict = drug_api.find_interaction(list(drugs_sent.keys()))
        drug_objects = []
        for drug in list(drugs_sent.keys()):
            drug_objects.append(DrugIdentifier(drug))
        interaction = DrugInteractions(drug_objects)
        return jsonify(interaction.build_interaction_results())


api.add_resource(InteractionCheck, '/check')

if __name__ == '__main__':
    app.run(debug=True)
