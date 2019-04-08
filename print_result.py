import numpy as np
import psycopg2
import xgboost as xgb
import pickle

data = np.loadtxt("feature_answer_all.txt")
model = pickle.load(open("XGB_TEST1.dat", 'rb'))
low_true = []
f1r = [-0.05,  0.06, 0.17, 0.28, 0.39, 0.5, 0.61, 0.72, 0.83, 0.94, 1.05]
high_false = []
strange_nl = []
for row in data:
    if row[2] < f1r[1] and row[5] == 1:
        score = model.predict([(row[2], row[3], row[4])])[0]
        low_true.append((row[0], row[1], row[2], score))
        strange_nl.append(int(row[1]))

print(set(strange_nl))
    
# for i in range(2,10):
#     hft = []
#     for row in data:
#         if row[2] > f1r[i] and row[2] < f1r[i+1] and row[5] == 0:
#             score = model.predict([(row[2], row[3], row[4])])[0]
#             hft.append((row[0], row[1], row[2], score))
#     if hft != []:
#         high_false.append(hft)
   
# print(high_false)

user = 'kjhong'
password = 'kjhong'
host_product = 'localhost'
dbname = 'kjhong'
port='5432'

conn_string = "dbname={dbname} user={user} host={host} password={password} port={port}"\
              .format(dbname=dbname, user=user, host=host_product, password=password, port=port)

conn = psycopg2.connect(conn_string)
curs = conn.cursor()
writeFile = open("true_data.txt", "w")
query = "select sq.id, se.id, sq.sql, se.sentence from sqls.naive_tb_0_0 as sq, sentences.naive_tb_0 as se,  answers.sql_0_0_nl_0 as an where an.sql_id = sq.id and an.sentence_id = se.id;"
curs.execute(query)
for sqlid, nlid, sql, nl in curs.fetchall():
#     writeFile.write(str(int(sqlid)) + ": " + sql + "\n" + str(int(nlid)) + ": " + nl + "\n\n")
    writeFile.write(str(int(nlid)) + ":\t" + nl + "\n" + str(int(sqlid)) + ":\t" + sql + "\n\n")

writeFile.close()

# writeFile = open("true_under_0.06.txt", "w")
# 
# for sqlid, nlid, f1, score in low_true:
#     query = "select sq.sql, se.sentence from sentences.naive_tb_0 as se, sqls.naive_tb_0_0 as sq where se.id = " + str(nlid) + " and sq.id = " + str(sqlid) + ";"
#     curs.execute(query)
#     result = curs.fetchall()[0]
#     writeFile.write(str(int(sqlid)) + ": " + result[0] + "\n" + str(int(nlid)) + ": " + result[1] + "\n" + "f1: " + str(f1) + "\tscore: " + str(score) + "\n\n")
# 
# for i in range(2,10):
#     writeFile = open("high_above_" + str(f1r[i]) + ".txt", "w")
# 
#     for sqlid, nlid, score in high_false[i-2]:
#         query = "select se.sentence, sq.sql from sentences.naive_tb_0 as se, sqls.naive_tb_0_0 as sq where se.id = " + str(nlid) + " and sq.id = " + str(sqlid) + ";"
#         curs.execute(query)
#         result = curs.fetchall()[0]
#         writeFile.write(result[0] + "\n" + result[1] + "\n" + str(score) + "\n\n")
# 
