from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
from DB import DB
from InteractionCheck.DrugIdentifier import DrugIdentifier
from InteractionCheck.DrugInteractions import DrugInteractions

app = Flask(__name__)
cors = CORS(app)
api = Api(app)


# suggestions for drug names when searching for one
class DrugSuggestions(Resource):
    def get(self):
        data_base = DB()
        drug_list = data_base.fetch_all_data(
            "SELECT english_name,hebrew_name FROM drug_name", '')
        english_hebrew = {}
        for drug in drug_list:
            english_name = drug[0].split()[0]
            hebrew_name = drug[1].split()[0]
            if english_name not in english_hebrew and hebrew_name not in english_hebrew:
                english_hebrew[english_name] = hebrew_name

        drug_list_dict = {}
        i = 0
        for english_name, hebrew_name in english_hebrew.items():
            drug_list_dict[i] = {}
            drug_list_dict[i]['name'] = english_name
            i += 1
        data_base.close_connection()

        return jsonify(drug_list_dict)


# check interaction between drugs
class InteractionCheck(Resource):
    def get(self):
        drugs_sent = request.args
        drug_objects = []
        for drug in list(drugs_sent.keys()):
            drug_objects.append(DrugIdentifier(drug))
        interaction = DrugInteractions(drug_objects)
        return jsonify(interaction.build_interaction_results())


# check interaction between drugs
class DrugSearch(Resource):
    def get(self):
        drug_sent = list(request.args.keys())[0]
        drug_details = DrugIdentifier(drug_sent)
        print(drug_details.build_search_answer())
        return jsonify(drug_details.build_search_answer())


api.add_resource(InteractionCheck, '/check')
api.add_resource(DrugSuggestions, '/suggest')
api.add_resource(DrugSearch, '/drug-search')

if __name__ == '__main__':
    app.run(debug=True)
