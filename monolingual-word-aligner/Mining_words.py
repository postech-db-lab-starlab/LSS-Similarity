from wordSim import *
from util import *
from coreNlpUtil import *
import sys
import re
import time
sys.path.append('/usr/local/python2.7/dist-packages/psycopg2')

import psycopg2
import config

##############################################################################################################################
def align(sentence1, cnlp):

    if isinstance(sentence1, list):
        sentence1 = ' '.join(sentence1)
        
    sentence1ParseResult = parseTexts(sentence1, cnlp)

    sentence1Lemmatized = lemmatize(sentence1ParseResult)

    sentence1PosTagged = posTag(sentence1ParseResult)

    sentence1LemmasAndPosTags = []
    for i in xrange(len(sentence1Lemmatized)):
        sentence1LemmasAndPosTags.append([])    
    for i in xrange(len(sentence1Lemmatized)):
        for item in sentence1Lemmatized[i]:
            sentence1LemmasAndPosTags[i].append(item)
        sentence1LemmasAndPosTags[i].append(sentence1PosTagged[i][3])
 
    try:
      ((start_offset, end_offset), index, word, lemma, postag) = sentence1LemmasAndPosTags[-1]
      print (str(start_offset) + '\t\t' +  str(end_offset) + '\t\t' + str(0) + '\t\t' + 'ROOT' + '\t\t' +  'root' + '\t\t' +  'ROOT')
    except:
      pass

    for ((start_offset, end_offset), index, word, lemma, postag) in sentence1LemmasAndPosTags:
      print (str(start_offset) + '\t\t' +  str(end_offset) + '\t\t' + str(index) + '\t\t' + word + '\t\t' +  lemma + '\t\t' +  postag)

    for (rel_name, a, b) in dependencyParseAndPutOffsets(sentence1ParseResult):
      aa = a.replace('{',' ').replace('}',' ').split()
      bb = b.replace('{',' ').replace('}',' ').split()
      print rel_name + '\t\t' +  aa[0] + '\t\t' + aa[1] + '\t\t' + aa[2] + '\t\t' + aa[3] + '\t\t' +  bb[0] + '\t\t' +  bb[1] + '\t\t' +  bb[2] + '\t\t' +  bb[3]
        
    for (offsets, idxs, words, tag) in ner(sentence1ParseResult):
      text = str(idxs[0])
      for i in range(1, len(idxs)):
        text += ',' + str(idxs[i])
      text += '\t\t' + str(tag)
      print (text)
##############################################################################################################################

conn_string = config.conn_string
conn = psycopg2.connect(conn_string)
curs = conn.cursor()

def get_url_ids():
  sql_string = "select u.url_id from urls.experiment_tb_1 as u, sentences.sentences_tb_0 as se1, sentences.sentences_tb_0 as se2, sqls.sqls_tb_0_0 as sq where u.url_id = se1.url_id and u.url_id = se2.url_id and se2.id = sq.sentence_id and sq.is_valid = true group by u.url_id order by u.url_id;"
  curs.execute(sql_string)
  return curs.fetchall()

def get_sentencess():
  sql_string = "select se.id, se.is_select, se.sentence from (select u.url_id from urls.experiment_tb_1 as u, sentences.sentences_tb_0 as se1, sqls.sqls_tb_0_0 as sq where u.url_id = se1.url_id and se1.id = sq.sentence_id and sq.is_valid = true group by u.url_id) as t, sentences.sentences_tb_0 as se  where t.url_id = se.url_id order by se.id;"
  curs.execute(sql_string)
  return curs.fetchall()

def get_sqls():
  sql_string = "select sq.id, is_valid, sql from urls.experiment_tb_1 as u, sentences.sentences_tb_0 as se1, sqls.sqls_tb_0_0 as sq where u.url_id = se1.url_id and se1.id = sq.sentence_id and sq.is_valid = true order by sq.id;"
  curs.execute(sql_string)
  return curs.fetchall()

def get_sentences(url_id):
  sql_string = "select id, sentence, is_select from sentences.sentences_tb_0 where url_id = " + str(url_id) + " order by id;"
  curs.execute(sql_string)
  return curs.fetchall()

def print_mining(mode):
  total_time = 0
  total_num = 0

  if mode == "sql":
    sentences = get_sqls()
  elif mode == "nl":
    sentences = get_sentencess()
  else:
    raise Exception("Set mode as 'sql' or 'nl'")

  num = len(sentences) / 16
  if n < 15: sentences = sentences[n * num : n*num + num]
  else: sentences = sentences[15 * num : ]

  print n * num, n * num + num

  for (sentence_id, is_select, sentence) in sentences:
    start_time = time.time()
    if len(sentence.split()) == 0:
      continue
    print '<sentence_id>:' + str(sentence_id)
    print '<sentence>:' + str(sentence)
    sentence = re.sub('[Ss][Ee][Ll][Ee][Cc][Tt][ ]+\*', 'select all', sentence)  
    if is_select: sentence = re.sub('\*,', 'all,', sentence)
    for word in re.findall('[A-Za-z0-9]*[A-Za-z][A-Za-z0-9]*\.[A-Za-z0-9]*[A-Za-z][A-Za-z0-9]*', sentence):
      sentence = sentence.replace(word, word.replace('.', ' '))
    print '<changed sentence>:' + str(sentence)
    try:
      align(sentence, cnlp)
    except: 
      print 'error'
    end_time = time.time()
    print '<time>:' + str(end_time - start_time)
    total_time += end_time - start_time
    total_num += 1
  print '<total_time>:' + str(total_time)
  print '<total_num>:' + str(total_num)

n = int(sys.argv[1])
port = 18080 + n
cnlp = StanfordNLP(port)

sys.stdout = open("Mined_words/Mined_words.sql_" + str(n) + ".txt", "w")
print_mining('sql')

sys.stdout = open("Mined_words/Mined_words.nl_" + str(n) + ".txt", "w")
print_mining('nl')