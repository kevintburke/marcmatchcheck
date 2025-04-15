"""NEW SIMILARITY CHECK FOR MARC RECORDS USING KEY FIELDS"""

KEYFIELDS = ['001', '020', '100', '110', '111', '130', '245', '250', '260', '264', '300']

import pandas as pd
from pymarc import MARCReader
from fuzzywuzzy import fuzz
import datetime
import numpy as np

def retrieve_data(filename : str):
    #Define function to retrieve data from field for each record in a given file and add to a dataframe
    #Create a dictionary to receive data
    recorddata = {}
    with open(f'{filename}.mrc', 'rb') as fh:
        reader = MARCReader(fh)
        for record in reader:
            ##NOT SURE HOW TO GET ALL 020 FIELDS; MAY MATTER FOR RECORDS WITH MULTIPLES (CURRENTLY RETURNS FIRST)
            recorddata[str(record['001'])] = [str(record['001']).lstrip('=001  '), record.isbn, record.author, record.title, record.publisher, record.pubyear]
            if record.physicaldescription:
                recorddata[str(record['001'])].append(str(record['300']).strip(r'=300  \\\\\$a'))
            else:
                recorddata[str(record['001'])].append("")
            try: 
                recorddata[str(record['001'])].insert(4, str(record['250']).strip(r'=250  \\\\\$a'))
            except:
                recorddata[str(record['001'])].insert(4, "")
    #Return dataframe
    df = pd.DataFrame.from_dict(recorddata, orient = 'index', columns= ['001','isbn','author','title','edition','publisher','pubdate','physicaldescription'], dtype = str)
    print(df)
    df.to_csv('dataframetest.csv', index = False)
    return df

def merge_df(df1 : pd.DataFrame, df2 : pd.DataFrame):
    #Accept two dataframes from retrieve_data and merge using 001 as key
    merged = pd.merge(df1, df2, how='inner', on='001', suffixes=('_a','_b'))
    #Sort columns
    column_order = ['001','isbn_a','isbn_b','author_a','author_b','title_a','title_b','edition_a','edition_b','publisher_a','publisher_b','pubdate_a','pubdate_b','physicaldescription_a','physicaldescription_b']
    merged = merged[column_order]
    #Return a single dataframe
    print(merged)
    merged.to_csv('mergedtest.csv', index = False)
    return merged

def calculate_similarity(row):
    similarities = []
    #Calculate ISBN similarity as 0 or 100 for exact match
    isbn_a = row.get('isbn_a')
    isbn_b = row.get('isbn_b')
    if isbn_a and isbn_b:
        if isbn_a.strip() == isbn_b.strip():
            similarities.append(100)
        else:
            similarities.append(0)
    elif not isbn_a and not isbn_b:
        similarities.append(100)
    else:
        similarities.append(0)
    #Calculate other field similarities using WRatio
    fields = ['author','title','edition','publisher','pubdate','physicaldescription']
    for field in fields:
        fa = row.get(f'{field}_a')
        fb = row.get(f'{field}_b')
        if not fa and not fb:
            similarities.append(100)
        else:
            sim = fuzz.WRatio(str(fa), str(fb))
            similarities.append(sim)
    #Return average of similarities
    if similarities:
        similarities = f'{np.mean(similarities):.2f}'
        return float(similarities)
    else:
        return 0

def compare_records(df : pd.DataFrame):
    #Insert similarity column at start of df
    df.insert(0, 'similarity', value=None)
    #Call similarity using apply to calculate similarity for each row
    df['similarity'] = df.apply(calculate_similarity, axis=1)
    #Sort df by similarity scores
    df.sort_values(by=['similarity'], inplace = True, na_position = 'first')
    #Return df with similarity scores
    return df

def main():
    #Accept inputs of filenames and test open via try-except to catch errors
    filename1 = ""
    while filename1 == "":
        filename1 = input("Enter the file name of original records in MARC binary (no extension): ")
        try:
            file1 = open(f'{filename1}.mrc','r')
            print(f'{filename1}.mrc found!')
            file1.close()
            break
        except Exception as e:
            print(e)
            filename1 = ""
            continue
    filename2 = ""
    while filename2 == "":
        filename2 = input("Enter the file name of updated records in MARC binary (no extension): ")
        try:
            file2 = open(f'{filename2}.mrc','r')
            print(f'{filename2}.mrc found!')
            file2.close
            break
        except Exception as e:
            print(e)
            filename2 = ""
            continue
    #Call create_df on files
    records1 = retrieve_data(filename1)
    print(records1)
    records2 = retrieve_data(filename2)
    print(records2)
    #Merge dataframes
    records_merged = merge_df(records1, records2)
    #Call compare_records on merged dataframe returned by create_df
    output = compare_records(records_merged)
    #Write output to .csv with unique filename using datetime to avoid overwriting
    timestamp = datetime.datetime.today().strftime('%m%d%H%M')
    output.to_csv(f'MARCMatchOutput{timestamp}.csv', index = False)
    print(f'Results saved to MARCMatchOutput{timestamp}.csv')

if __name__ == "__main__":
    main()