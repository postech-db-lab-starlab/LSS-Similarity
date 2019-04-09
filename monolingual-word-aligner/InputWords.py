import sys
import re
import time
sys.path.append('/usr/local/python2.7/dist-packages/psycopg2')

import psycopg2
import config

conn_string = config.conn_string
conn = psycopg2.connect(conn_string)
curs = conn.cursor()

def inputLemmaPosTagged(sentence_id, start_offset, end_offset, index, word, lemma, postag, mode):
  if mode == "sql":
    table_name = "sql_features.dls_cu_tb_0_0_0"
  elif mode == "nl":
    table_name = "nl_features.dls_cu_tb_0_0"
  else:
    raise Exception("Specify mode as 'sql' or 'nl'")

  sql_string = "insert into " + table_name + "(sentence_id, start_offset, end_offset, index, word, lemma, postag) values("
  sql_string += str(sentence_id) + "," + str(start_offset) + "," + str(end_offset) + "," + str(index) + ",'"
  sql_string += word[:149].replace("'", "''") + "', '" + lemma[:149].replace("'", "''") + "', '" + postag.replace("'", "''") + "');"
  curs.execute(sql_string)
  

def inputRelation(sentence_id, rel_name, l_idx, r_idx, mode):
  if mode == "sql":
    table_name = "sql_features.dls_cu_tb_0_0_1"
  elif mode == "nl":
    table_name = "nl_features.dls_cu_tb_0_1"
  else:
    raise Exception("Specify mode as 'sql' or 'nl'")

  sql_string = "insert into " + table_name + "(sentence_id, rel_name, left_index, right_index) values("
  sql_string += str(sentence_id) + ",'" + rel_name.replace("'", "''") + "'," + str(l_idx) + "," + str(r_idx) + ");"
  curs.execute(sql_string)

def inputNamed(sentence_id, indexes, tag, mode):
  if mode == "sql":
    table_name = "sql_features.dls_cu_tb_0_0_2"
  elif mode == "nl":
    table_name = "nl_features.dls_cu_tb_0_2"
  else:
    raise Exception("Specify mode as 'sql' or 'nl'")

  sql_string = "insert into " + table_name + "(sentence_id, indexes, tag) values("
  sql_string += str(sentence_id) + ",'" + str(indexes) + "','" + str(tag) + "');"
  curs.execute(sql_string)

def insert_to_db(file, mode):
  sentence_id = -1
  if mode == "nl":
    f_sid = open("sentence_ids.txt", "w")
  while True:
    line = f.readline()
    if not line: break
    line = line.strip()
    if line.find('<sentence_id>:') == 0:
      sentence_id = int(line[14:])
      if mode == "nl":
        f_sid.write(str(sentence_id) + "\n")
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
        inputLemmaPosTagged(sentence_id, items[0], items[1], items[2], items[3], items[4], items[5], mode)
      elif len(items) == 9:
        inputRelation(sentence_id, items[0], items[4], items[8], mode)
      elif len(items) == 2:
        inputNamed(sentence_id, items[0], items[1], mode)

fname = "Mined_words.sql.txt"
f = open(fname, 'r')
insert_to_db(f, "sql")

fname = "Mined_words.nl.txt"
f = open(fname, 'r')
insert_to_db(f, "nl")

conn.commit()
