#-*-coding:utf-8
import psycopg2
import pandas as pd
import numpy as np

def execute(query):
    pc.execute(query)
    return pc.fetchall()

user = 'kjhong'
password = 'kjhong'
host_product = 'localhost'
dbname = 'kjhong'
port='5432'

conn_string = "dbname={dbname} user={user} host={host} password={password} port={port}"\
              .format(dbname=dbname, user=user, host=host_product, password=password, port=port)

try:
    conn = psycopg2.connect(conn_string)
except:
    print("I am unable to connect to the database")

curs = conn.cursor()

# query = "SELECT * FROM answers.sql_0_0_nl_0;" 
# print(pd.read_sql(query, conn))

feats_raw = np.loadtxt("features.txt")

query = "SELECT * FROM answers.sql_0_0_nl_0;"
answs_raw = pd.read_sql(query, conn)

"""
feats_raw['sql_id']
feats_raw['sentence_id']
feats_raw['feature1']
feats_raw['feature2']
feats_raw['feature3']

answs_raw['sql_id']
answs_raw['sentence_id']
"""

feats = np.array([])
false_num = 0
true_num = 0
for idx in range(0, feats_raw.shape[0]):
    sql_id = int(feats_raw[idx, 0])
    nl_id = int(feats_raw[idx, 1])
    row = feats_raw[idx, :]

    a = answs_raw.query('sql_id == "' + str(sql_id) + '" & sentence_id == "' + str(nl_id) + '"')
    
    true_row = 0
    if not a.empty:
        row = np.hstack([row, np.array([1])])
        true_num += 1
    else:
        row = np.hstack([row, np.array([0])])
        false_num += 1

    if feats.size == 0:
        feats = row
    else:
        feats = np.vstack([feats, row])

print("True data: {}, False data: {}".format(true_num, false_num))
np.savetxt("feature_answer_all.txt", feats)
