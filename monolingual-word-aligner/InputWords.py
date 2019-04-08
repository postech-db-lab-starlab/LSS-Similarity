import sys
import re
import time
sys.path.append('/usr/local/python2.7/dist-packages/psycopg2')

import psycopg2


conn_string = "host='localhost' dbname='kjhong' user='kjhong' password='kjhong'"
conn = psycopg2.connect(conn_string)
curs = conn.cursor()

def inputLemmaPosTagged(sentence_id, start_offset, end_offset, index, word, lemma, postag):
  sql_string = "insert into sql_features.dls_cu_tb_0_0_0(sentence_id, start_offset, end_offset, index, word, lemma, postag) values("
  sql_string += str(sentence_id) + "," + str(start_offset) + "," + str(end_offset) + "," + str(index) + ",'"
  sql_string += word[:149].replace("'", "''") + "', '" + lemma[:149].replace("'", "''") + "', '" + postag.replace("'", "''") + "');"
  curs.execute(sql_string)
  

def inputRelation(sentence_id, rel_name, l_idx, r_idx):
  sql_string = "insert into sql_features.dls_cu_tb_0_0_1(sentence_id, rel_name, left_index, right_index) values("
  sql_string += str(sentence_id) + ",'" + rel_name.replace("'", "''") + "'," + str(l_idx) + "," + str(r_idx) + ");"
  curs.execute(sql_string)

def inputNamed(sentence_id, indexes, tag):
  sql_string = "insert into sql_features.dls_cu_tb_0_0_2(sentence_id, indexes, tag) values("
  sql_string += str(sentence_id) + ",'" + str(indexes) + "','" + str(tag) + "');"
  curs.execute(sql_string)

fname = sys.argv[1]
f = open(fname, 'r')

sentence_id = -1
while True:
  line = f.readline()
  if not line: break
  line = line.strip()
  if line.find('<sentence_id>:') == 0:
    sentence_id = int(line[14:])
  elif line.find('<sentence>:') == 0:
    pass
  elif line.find('<time>:') == 0:
    pass
  elif line.strip() == 'error':
    pass
  elif line.find('<changed sentence>:') == 0:
    pass
  else:
    items = line.split('\t\t')
    if len(items) == 6:
      inputLemmaPosTagged(sentence_id, items[0], items[1], items[2], items[3], items[4], items[5])
    elif len(items) == 9:
      inputRelation(sentence_id, items[0], items[4], items[8])
    elif len(items) == 2:
      inputNamed(sentence_id, items[0], items[1])      

conn.commit()
