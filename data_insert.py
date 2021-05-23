from DB import DB

# Example
# (['DAKTARIN', 'TARODENT'],
# ['2021-05-05', '2021-04-27'],
# ['2021-05-10', '2021-05-04'],
# ['sever', 'notSever'],
# ['2021-04-25', '2021-05-23'],
# ['עייפות', 'דפיקות לב מהירות'], False)

if __name__ == '__main__':
    data_base = DB()

    real = False
    drug_list = []
    untilDate_list = []
    fromDate_list = []
    symptom_list = []
    severity_list = []
    appearDate_list = []

    report_data = (drug_list, fromDate_list, untilDate_list, severity_list, appearDate_list, symptom_list, real)
    postgres_insert_query = """INSERT INTO report_details (drugs,fromDate,untilDate,severity, appearDate,symptoms, real_data) VALUES \
    (%s,%s,%s, %s,%s,%s,%s) """
    data_base.insert_data_row(postgres_insert_query, report_data)
