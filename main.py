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
        drug_list_dict = []
        dict = {}
        for english_name, hebrew_name in english_hebrew.items():
            dict['name'] = english_name
            drug_list_dict.append(dict.copy())
            dict['name'] = hebrew_name
            drug_list_dict.append(dict.copy())
        data_base.close_connection()
        print(drug_list_dict)

        return jsonify(drug_list_dict)


# check interaction between drugs 1
class InteractionCheck(Resource):
    def get(self):
        drugs_sent = request.args
        drug_objects = []
        for drug in list(drugs_sent.keys()):
            drug_objects.append(DrugIdentifier(drug))

        interaction = DrugInteractions(drug_objects)
        return jsonify(interaction.interaction_results)

    # get stats of interactions


class InteractionStats(Resource):
    def get(self):
        stats = {}
        stats['symptoms'] = {}
        stats['symptoms']['עייפות'] = 100
        stats['symptoms']['חולשה'] = 70
        stats['symptoms']['כאב בטן'] = 50
        stats['symptoms']['אדמומיות'] = 30
        print(stats)
        return jsonify(stats)


# check interaction between drugs
class DrugSearch(Resource):
    def get(self):
        drug_sent = list(request.args.keys())[0]
        drug_details = DrugIdentifier(drug_sent)
        print(drug_details.build_search_answer())
        return jsonify(drug_details.build_search_answer())


class SideEfeecetReport(Resource):
    def post(self):
        real = True
        drug_sent = request.get_json(force=True)
        print(drug_sent)

        user_data = (drug_sent['factorName'], drug_sent['email'], drug_sent['phoneNumber'], drug_sent['sector'],
                     drug_sent['medicalSector'], real)
        drug_list = [item['name'] for item in drug_sent['drugList']]
        untilDate_list = [item['untilDate'] for item in drug_sent['drugList']]
        fromDate_list = [item['fromDate'] for item in drug_sent['drugList']]
        symptom_list = [item['name'] for item in drug_sent['symptomList']]
        severity_list = [item['severity'] for item in drug_sent['symptomList']]
        appearDate_list = [item['appearDate'] for item in drug_sent['symptomList']]

        report_data = (drug_list, fromDate_list, untilDate_list, severity_list, appearDate_list, symptom_list, real)
        print(report_data)
        data_base = DB()
        postgres_insert_query = """ INSERT INTO private_user_details (factor_name, email,phone,sector,medical_sector, real_data)\
         VALUES (%s,%s,%s,%s,%s,%s)"""
        data_base.insert_data_row(postgres_insert_query, user_data)
        postgres_insert_query = """INSERT INTO report_details (drugs,fromDate,untilDate, symptoms,severity,appearDate, real_data) VALUES \
        (%s,%s,%s, %s,%s,%s,%s) """
        data_base.insert_data_row(postgres_insert_query, report_data)
        data_base.close_connection()


api.add_resource(InteractionCheck, '/check')
api.add_resource(InteractionStats, '/stats')

api.add_resource(DrugSuggestions, '/suggest')
api.add_resource(DrugSearch, '/drug-search')
api.add_resource(SideEfeecetReport, '/side-effect-report')

if __name__ == '__main__':
    app.run(debug=True)
