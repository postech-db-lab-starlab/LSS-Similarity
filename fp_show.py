import numpy as np
import psycopg2

ids = np.loadtxt("fp_case_feat.txt")

conn_string = "host='localhost' dbname='kjhong' user='kjhong' password='kjhong'"
conn = psycopg2.connect(conn_string)
curs = conn.cursor()

writeFile = open("fp_case_sql_nl.txt", "w")

for i in ids:
    sql = "select sql, sentence from sqls.naive_tb_0_0 as A, sentences.naive_tb_0 as B where A.id = {} and B.id = {};".format(int(i[0]), int(i[1]))
    curs.execute(sql)
    writeFile.write(str(curs.fetchall()) + "\n")
