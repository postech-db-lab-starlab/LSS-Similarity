#-*-coding:utf-8
import psycopg2
import pandas as pd
import numpy as np

conn_string = "host='localhost' dbname='kjhong' user='kjhong' password='kjhong'"
conn = psycopg2.connect(conn_string)
curs = conn.cursor()

sql_query = "select e.sql_id, e.nl_id, e.feat1, e.feat2, e.feat3, (e.nl_id = sq.sentence_id) as t from crowdsourcing.experiment as e, crowdsourcing.sqls as sq where e.sql_id = sq.id;"
curs.execute(sql_query)
rows = curs.fetchall()
#print(np.array(rows)[8])
feats = np.array(rows)

# feats_raw = np.loadtxt("features_crowdsourcing.txt")

"""
feats_raw['sql_id']
feats_raw['sentence_id']
feats_raw['feature1']
feats_raw['feature2']
feats_raw['feature3']

answs_raw['sql_id']
answs_raw['sentence_id']
"""

#feats = np.hstack([feats_raw, np.ones((feats_raw.shape[0], 1))])
np.savetxt("feature_answer_all_crowdsourcing_tf.txt", feats)
