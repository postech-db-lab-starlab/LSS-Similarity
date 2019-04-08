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

# query = "SELECT e.sql_id as sql_id, e.sentence_id as sentence_id, feature1, feature2, feature3 FROM experiment1.dls_cu_raw as e, sqls.naive_tb_0_0 as sq where e.sql_id = sq.id and e.sentence_id != sq.sentence_id;"
# query = "SELECT * FROM experiment1.dls_cu_raw as e, urls.experiment_tb_0 as u, sentences.naive_tb_0 as se where u.url_id = se.url_id and se.sentence_id = e.sentence_id and  e.sentence_id not in (SELECT sentence_id from sqls.naive_tb_0_0 as sq where sq.is_valid = true);"

query = "select ex.sql_id, ex.sentence_id, feature1, feature2, feature3 from experiment1.dls_cu_raw as ex, sentences.naive_tb_0 as se1 where ex.sentence_id not in (select sq.sentence_id from sqls.naive_tb_0_0 as sq where sq.is_valid = true) and se1.id = ex.sentence_id and se1.url_id != 15546 and ex.sql_id in (select sentence_id from sql_features.dls_cu_tb_0_0_0 as nlf) and ex.sentence_id in (select sentence_id from nl_features.dls_cu_tb_0_0);"
feats_raw = pd.read_sql(query, conn)

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
for idx in range(0, feats_raw['sql_id'].__len__()):
    sql_id = feats_raw.at[idx, 'sql_id']
    nl_id = feats_raw.at[idx, 'sentence_id']
    row = feats_raw.ix[idx, ['feature1', 'feature2', 'feature3']].values

    a = answs_raw.query('sql_id == "' + str(sql_id) + '" & sentence_id == "' + str(nl_id) + '"')
    
    if not a.empty:
        row = np.hstack([sql_id, nl_id, row, np.array([1])])
    else:
        row = np.hstack([sql_id, nl_id, row, np.array([0])])

    if feats.size == 0:
        feats = row
    else:
        feats = np.vstack([feats, row])
    #b = answs_raw.query('sql_id == "' + str(sql_id) + '"')

    #if not b.empty:
    #    if feats.size == 0:
    #        feats = row
    #    else:
    #        feats = np.vstack([feats, row])
    #else:
    #    continue

np.savetxt("feature_answer.txt", feats)
