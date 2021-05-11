from DB import DB

if __name__ == '__main__':
    data_base = DB()

    real = False
    drug_list = [item['name'] for item in drug_sent['drugList']]
    untilDate_list = [item['untilDate'] for item in drug_sent['drugList']]
    fromDate_list = [item['fromDate'] for item in drug_sent['drugList']]
    symptom_list = [item['name'] for item in drug_sent['symptomList']]
    severity_list = [item['severity'] for item in drug_sent['symptomList']]
    appearDate_list = [item['appearDate'] for item in drug_sent['symptomList']]

    report_data = (drug_list, fromDate_list, untilDate_list, severity_list, appearDate_list, symptom_list, real)
    postgres_insert_query = """INSERT INTO report_details (drugs,fromDate,untilDate, symptoms,severity,appearDate, real_data) VALUES \
    (%s,%s,%s, %s,%s,%s,%s) """
    data_base.insert_data_row(postgres_insert_query, report_data)
