import sys
sys.path.append('/usr/local/python2.7/dist-packages/psycopg2')
import psycopg2
import aligner_modified
import time

def getLemmasAndPosTagsData(sentence_id):
  sql_string = "select start_offset, end_offset, index, word, lemma, postag from crowdsourcing.nl_features0 "
  sql_string += "where sentence_id = " + str(sentence_id) + " and index > 0 order by index;"
  curs.execute(sql_string)
  return curs.fetchall()

def getLemmasAndPosTags(sentence_id):
  LemmasAndPosTags = []
  for (start_offset, end_offset, index, word, lemma, postag) in getLemmasAndPosTagsData(sentence_id):
    LemmasAndPosTags.append([[start_offset, end_offset], index, word, lemma, postag])
  return LemmasAndPosTags

def getDParseData(sentence_id):
  sql_string = "select rel.rel_name, da1.word, da1.start_offset, da1.end_offset, da1.index, da2.word, da2.start_offset, da2.end_offset, da2.index "
  sql_string += "from crowdsourcing.nl_features1 as rel, crowdsourcing.nl_features0 as da1, crowdsourcing.nl_features0 as da2 "
  sql_string += "where rel.sentence_id = da1.sentence_id and rel.left_index = da1.index and "
  sql_string += "rel.sentence_id = da2.sentence_id and rel.right_index = da2.index and "
  sql_string += "rel.sentence_id = " + str(sentence_id) + " "
  sql_string += "order by rel.left_index, rel.right_index"
  curs.execute(sql_string)
  return curs.fetchall()

def getDParse(sentence_id):
  DParse = []
  for (rel_name, l_word, l_s_off, l_e_off, l_idx, r_word, r_s_off, r_e_off, r_idx) in getDParseData(sentence_id):
    l_text = str(l_word) + '{' + str(l_s_off) + ' ' + str(l_e_off) + ' ' + str(l_idx) + '}'
    r_text = str(r_word) + '{' + str(r_s_off) + ' ' + str(r_e_off) + ' ' + str(r_idx) + '}'
    DParse.append([str(rel_name), l_text, r_text])
  return DParse

def getWordInfo(sentence_id, index):
  sql_string = "select start_offset, end_offset, word from crowdsourcing.nl_features0 where sentence_id = " + str(sentence_id) + " and index = " + str(index) + ";"
  curs.execute(sql_string)
  try: return curs.fetchall()[0]
  except: return None

def getNamedEntitiesData(sentence_id):
  sql_string = "select indexes, tag from crowdsourcing.nl_features2 where sentence_id = " + str(sentence_id) + ";"
  curs.execute(sql_string)
  return curs.fetchall()

def getNamedEntities(sentence_id):
  NamedEntities = []
  for (indexes, tag) in getNamedEntitiesData(sentence_id):
    NamedEntity = [[],[],[], tag]
    for index in indexes.split(','):
      (s_off, e_off, word) = getWordInfo(sentence_id, index)
      NamedEntity[0].append([int(s_off), int(e_off)])
      NamedEntity[1].append(int(index))
      NamedEntity[2].append(word)
    NamedEntities.append(NamedEntity)
  return NamedEntities

def getLemmasAndPosTagsData2(sentence_id):
  sql_string = "select start_offset, end_offset, index, word, lemma, postag from crowdsourcing.sql_features0 "
  sql_string += "where sentence_id = " + str(sentence_id) + " and index > 0 order by index;"
  curs.execute(sql_string)
  return curs.fetchall()

def getLemmasAndPosTags2(sentence_id):
  LemmasAndPosTags = []
  for (start_offset, end_offset, index, word, lemma, postag) in getLemmasAndPosTagsData2(sentence_id):
    LemmasAndPosTags.append([[start_offset, end_offset], index, word, lemma, postag])
  return LemmasAndPosTags

def getDParseData2(sentence_id):
  sql_string = "select rel.rel_name, da1.word, da1.start_offset, da1.end_offset, da1.index, da2.word, da2.start_offset, da2.end_offset, da2.index "
  sql_string += "from crowdsourcing.sql_features1 as rel, crowdsourcing.sql_features0 as da1, crowdsourcing.sql_features0 as da2 "
  sql_string += "where rel.sentence_id = da1.sentence_id and rel.left_index = da1.index and "
  sql_string += "rel.sentence_id = da2.sentence_id and rel.right_index = da2.index and "
  sql_string += "rel.sentence_id = " + str(sentence_id) + " "
  sql_string += "order by rel.left_index, rel.right_index"
  curs.execute(sql_string)
  return curs.fetchall()

def getDParse2(sentence_id):
  DParse = []
  for (rel_name, l_word, l_s_off, l_e_off, l_idx, r_word, r_s_off, r_e_off, r_idx) in getDParseData2(sentence_id):
    l_text = str(l_word) + '{' + str(l_s_off) + ' ' + str(l_e_off) + ' ' + str(l_idx) + '}'
    r_text = str(r_word) + '{' + str(r_s_off) + ' ' + str(r_e_off) + ' ' + str(r_idx) + '}'
    DParse.append([str(rel_name), l_text, r_text])
  return DParse

def getWordInfo2(sentence_id, index):
  sql_string = "select start_offset, end_offset, word from crowdsourcing.sql_features0 where sentence_id = " + str(sentence_id) + " and index = " + str(index) + ";"
  curs.execute(sql_string)
  try: return curs.fetchall()[0]
  except: return None

def getNamedEntitiesData2(sentence_id):
  sql_string = "select indexes, tag from crowdsourcing.sql_features2 where sentence_id = " + str(sentence_id) + ";"
  curs.execute(sql_string)
  return curs.fetchall()

def getNamedEntities2(sentence_id):
  NamedEntities = []
  for (indexes, tag) in getNamedEntitiesData2(sentence_id):
    NamedEntity = [[],[],[], tag]
    for index in indexes.split(','):
      (s_off, e_off, word) = getWordInfo2(sentence_id, index)
      NamedEntity[0].append([int(s_off), int(e_off)])
      NamedEntity[1].append(int(index))
      NamedEntity[2].append(word)
    NamedEntities.append(NamedEntity)
  return NamedEntities


def getSqlNl_id(url_id):
  sql_string = "select sqi, sei "
  sql_string += "from (select u.url_id as ui1, sq.id as sqi from urls.experiment_tb_1 as u, sentences.naive_tb_0 as se, sqls.naive_tb_0_0 as sq where u.url_id = se.url_id and sq.sentence_id = se.id and sq.is_valid = true) as t, "
  sql_string += "(select u1.url_id as ui2, se1.id as sei from urls.experiment_tb_1 as u1, sentences.naive_tb_0 as se1 where u1.url_id = se1.url_id) as t1 "
  sql_string += "where t.ui1 = t1.ui2 and t.ui1 = " + str(url_id) + " order by sei, sqi;"
  curs.execute(sql_string)
  return curs.fetchall()

def getSqlNl():
  sql_string = "select id, sentence_id from crowdsourcing.sqls"
  curs.execute(sql_string)
  return curs.fetchall()


def get_url_id(sentence_id):
  sql_string = "select url_id "
  sql_string += "from sentences.naive_tb_0 where id = " + str(sentence_id) + " group by url_id;"
  curs.execute(sql_string)
  return curs.fetchall()

conn_string = "host='localhost' dbname='kjhong' user='kjhong' password='kjhong'"
conn = psycopg2.connect(conn_string)
curs = conn.cursor()


#fname = sys.argv[2]
#f = open(fname, "r")
#url_ids = set([])
#while True:
#  line = f.readline()
#  if len(line.strip()) == 0: break
#  (url_id,) = get_url_id(line.strip())[0]
#  url_ids.add(url_id)

sqlnls = []
#for url_id in url_ids:
#  sqlnls += getSqlNl_id(url_id)

sqlnls = getSqlNl()
num = len(sqlnls) / 32
n = int(sys.argv[1])
if n < 31: sqlnls = sqlnls[n*num : n*num + num]
else: sqlnls = sqlnls[n*num : ]

(csql_id, csql_okay) = (-1, False)
(cnl_id, cnl_okay) = (-1, False)
for (sql_id, nl_id) in sqlnls:
  sttime = time.time()
#  print ('<ids>:' + str(nl_id) + ',' +  str(sql_id))
  if (sql_id, nl_id) == (csql_id, cnl_id): continue
  if nl_id != cnl_id:
    cnl_id = nl_id
    LemmasAndPosTags1 = getLemmasAndPosTags(nl_id)  
    if len(LemmasAndPosTags1) == 0: 
#      print('error')
      cnl_okay = False
      continue
    DParse1 = getDParse(nl_id) 
    NamedEntities1 = getNamedEntities(nl_id)
    cnl_okay = True
  if sql_id != csql_id:
    csql_id = sql_id
    LemmasAndPosTags2 = getLemmasAndPosTags2(sql_id)
    if len(LemmasAndPosTags2) == 0:
#      print('error')
      csql_okay = False
      continue
    DParse2 = getDParse2(sql_id) 
    NamedEntities2 = getNamedEntities2(sql_id)
    csql_okay = True
  if csql_okay and cnl_okay: 
    stime = time.time()
    results = aligner_modified.align((LemmasAndPosTags1, DParse1, NamedEntities1), (LemmasAndPosTags2, DParse2, NamedEntities2))
#    print 'align', time.time() - stime
#    text = ''
    for (lid, rid) in results:
      insert_query = "insert into crowdsourcing.alignments (sql_id, sql_idx, sentence_id, sentence_idx) values (" + str(sql_id) + ", " + str(rid) + ", " + str(nl_id) + ", " + str(lid) + ");"
      curs.execute(insert_query)
#      text += str(lid) + ',' + str(rid) + '\t'
#    print (text)
  else:
	  pass
#    print ('error')
#  print 'total', time.time() - sttime

conn.commit()
curs.close()
conn.close()
