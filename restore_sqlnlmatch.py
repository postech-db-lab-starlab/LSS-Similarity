#-*-coding:utf-8
import psycopg2
import json

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

with open("sqlnlmatch_data_sql.txt","r") as dfile:
    ls = dfile.readlines()
    for l in ls:
        jdic = json.loads(l)
        query = "insert into sqlnlmatch.sqls (id, url_id, sql, position) values (" + str(jdic['id']) + ", '" + str(jdic['url_id'])  + "', '" + jdic['sql'].replace("'", "''") + "', " + str(jdic['position']) + ");"
        curs.execute(query)

with open("sqlnlmatch_data_sentence.txt","r") as dfile:
    ls = dfile.readlines()
    for l in ls:
        jdic = json.loads(l)
        query = "insert into sqlnlmatch.sentences (id, url_id, sentence, position) values (" + str(jdic['id']) + ", '" + str(jdic['url_id'])  + "', '" + jdic['sentnece'].replace("'", "''") + "', " + str(jdic['position']) + ");"
        curs.execute(query)
   
conn.commit()
curs.close()
conn.close()
