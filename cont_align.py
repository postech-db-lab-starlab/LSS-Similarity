import psycopg2
import json

user = 'kjhong'
password = 'kjhong'
host_product = 'localhost'
dbname = 'kjhong'
port='5432'

conn_string = "dbname={dbname} user={user} host={host} password={password} port={port}"\
.format(dbname=dbname, user=user, host=host_product, password=password, port=port)

conn = psycopg2.connect(conn_string)
curs = conn.cursor()

cfile = open("contents.txt", "r")
wfile = open("cont_align.txt", "w")
for line in cfile:
    dic = json.loads(line)
    query = "select sql_idx, sentence_idx from alignments.dls_cu where sql_id = " + str(dic['sqlid']) + " and sentence_id = " + str(dic['nlid']) + ";"
    curs.execute(query)
    align = str(curs.fetchall())

    w_str = str(dic['sqlid']) + '\t' + str(dic['nlid']) + '\n' + str(dic['sql_content']) + '\n' + str(dic['nl_content']) + '\n' + align + '\n'
    wfile.write(w_str)

