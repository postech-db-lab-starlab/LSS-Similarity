import json
import psycopg2

conn_string = "host='localhost' dbname='kjhong' user='kjhong' password='kjhong'"
conn = psycopg2.connect(conn_string)
curs = conn.cursor()

with open("crowdsourcing_data_sql.txt", "r") as sql_file:
	while (True):
		line = sql_file.readline()
		if not line:
			break
		dic_line = json.loads(line)

		sql_insert = "insert into crowdsourcing.sqls (id, sentence_id, sql) values (" + str(dic_line["id"]) + ", " + str(int(dic_line["sentence_id"])) + ", '" + dic_line["sql"].replace("'", "''") + "');"
		curs.execute(sql_insert)

with open("crowdsourcing_data_sentence.txt", "r") as nl_file:
	while (True):
		line = nl_file.readline()
		if not line:
			break
		dic_line = json.loads(line)

		nl_insert = "insert into crowdsourcing.sentences (id, url_id, position, sentence) values (" + str(int(dic_line["id"])) + ", '" + dic_line["table_id"] + "', '" + str(dic_line["position"]) + "', '" + dic_line["sentence"].replace("'", "''") + "');"
		curs.execute(nl_insert)

conn.commit()
curs.close()
conn.close()
