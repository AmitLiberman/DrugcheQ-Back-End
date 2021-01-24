from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
from DB import DB
import drug_api

app = Flask(__name__)
cors = CORS(app)
api = Api(app)


class InteractionCheck(Resource):
    def get(self):
        drugs_sent = request.args
        interaction_dict = drug_api.find_interaction(list(drugs_sent.keys()))
        data_base = DB()
        names = data_base.fetch_all_data('''SELECT english_name,hebrew_name
                   FROM drug_name''')
        for row in names:
            print("english name = ", row[0], )
            print("hebrew name ", row[1])
        data_base.close_connection()
        return jsonify(interaction_dict)


api.add_resource(InteractionCheck, '/check')

if __name__ == '__main__':
    app.run(debug=True)
