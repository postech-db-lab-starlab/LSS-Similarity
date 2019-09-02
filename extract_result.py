import psycopg2
import config.config as config
import numpy as np

conn_string = config.conn_string

try:
    conn = psycopg2.connect(conn_string)
except:
    print("I am unable to connect to the database")

curs = conn.cursor()
final_result = np.load('data/test_result.dat')

sql_ids = final_result[:, 0]
nl_ids = final_result[:, 1]
preds = final_result[:, 2]

sqls = []
nls = []

for sid in nl_ids:
    query = "SELECT sentence FROM sentences.sentences_tb_0 WHERE id = %d"%sid
    curs.execute(query)
    result = curs.fetchall()
    nls.append(result[0])

for sid in sql_ids:
    query = "SELECT sentence FROM sqls.sqls_tb_0_0 WHERE id = %d"%sid
    curs.execute(query)
    result = curs.fetchall()
    sqls.append(result[0])

result_file = open("data/final_result.txt", "w")

for i in range(final_result.shape[0]):
    result_file.write("NL   : %s\n"%nls[i])
    result_file.write("SQL  : %s\n"%sqls[i])
    result_file.write("Score: %f\n\n"%preds[i])

result_file.close()