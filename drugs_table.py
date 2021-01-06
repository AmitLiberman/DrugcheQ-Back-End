import pandas as pd
from sqlalchemy import create_engine


'''
In the current script I build the drug table from an Excel file
I received from the Ministry of Health
'''


def main():
    relevant_cols = ['remedy_number', 'english_name', 'hebrew_name', 'ingredients', 'details', 'dosage_form',
                     'how_taking',
                     'prescription', 'health_basket', 'veterinary_preparation']
    # read excel file to Data Frame
    df = pd.read_excel('Israel_Drurgs.xlsx', usecols=relevant_cols)
    # delete rows with the same english drug name
    df = df.drop_duplicates(subset=['english_name'])
    # delete rows with veterinary medications
    df = (df.loc[df['veterinary_preparation'] != 'VET'])
    # make final dataframe
    final_df = df[['remedy_number', 'english_name', 'hebrew_name', 'ingredients', 'details', 'dosage_form','how_taking',
                     'prescription', 'health_basket']]
    engine = create_engine('postgres://vrlaozxymgbowo:57941d7c9247c6cd0bc40e4467ed998eece037cc7c5dcafe6515820ec4095f0f@ec2-54-76-215-139.eu-west-1.compute.amazonaws.com:5432/d984k5vt1jr9rs')
    final_df.to_sql('drug_name', engine)

if __name__ == '__main__':
    main()
