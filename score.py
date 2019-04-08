import sys
import psycopg2
import time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier, XGBRegressor

#  sql_string = "select sentence_id, (" + str(a2) + " * feature2 + " + str(a3) + " * feature3) as score "
def get_best_sentence(sql_id, a1, a2, a3):
  sql_string = "select ex.sentence_id, se1.sentence, (" + str(a1) + " * feature1 + " + str(a2) + " * feature2  + " + str(a3) + " * feature3) as score, feature1, feature2, feature3 "
  sql_string += "from experiment1.dls_cu_raw as ex, sqls.naive_tb_0_0 as sq1, sentences.naive_tb_0 as se1 "
  sql_string += "where ex.sentence_id not in (select sq.sentence_id from sqls.naive_tb_0_0 as sq where sq.is_valid = true) "
  sql_string += "and ex.sql_id = " + str(sql_id) + " and sq1.id = ex.sql_id and se1.id = ex.sentence_id and se1.url_id != 15546"
  sql_string += "order by score desc limit 1;"
  curs.execute(sql_string)
  try:return curs.fetchall()[0]
  except:return None

def get_all_nl_feat():
  sql_string = "select ex.sql_id, ex.sentence_id, feature1, feature2, feature3, (an.sentence_id = ex.sentence_id) as label "
  sql_string += "from experiment1.dls_cu_raw as ex, sqls.naive_tb_0_0 as sq1, sentences.naive_tb_0 as se1, answers.sql_0_0_nl_0 as an "
  sql_string += "where ex.sentence_id not in (select sq.sentence_id from sqls.naive_tb_0_0 as sq where sq.is_valid = true) "
  sql_string += "and sq1.id = ex.sql_id and se1.id = ex.sentence_id and se1.url_id != 15546 and an.sql_id = ex.sql_id;"
  curs.execute(sql_string)
  try:return curs.fetchall()
  except:return None

def get_answer_score(sql_id, sentence_id, a1, a2, a3):
  sql_string = "select (" + str(a1) + " * feature1 + " + str(a2) + " * feature2  + " + str(a3) + " * feature3) as score, feature1, feature2, feature3 "
  sql_string += "from experiment1.dls_cu_raw as ex "
  sql_string += "where ex.sql_id = " + str(sql_id) + " and ex.sentence_id = " + str(sentence_id) + ";"
  curs.execute(sql_string)
  try:return curs.fetchall()[0]
  except: return None

def get_dependency_available(kind):
  sql_string = "select sentence_id "
  if kind == 0: sql_string += "from nl_features.dls_cu_tb_0_0 "
  else: sql_string += "from sql_features.dls_cu_tb_0_0_0 "
  sql_string += "group by sentence_id order by sentence_id;"
  curs.execute(sql_string.replace('\n',''))
  try: return curs.fetchall()
  except: return []

def get_alignments(sql_id, sentence_id):
  sql_string = "select sf.word, nf.word "
  sql_string += "from alignments.dls_cu as al, sql_features.dls_cu_tb_0_0_0 as sf, nl_features.dls_cu_tb_0_0 as nf "
  sql_string += "where al.sql_id = sf.sentence_id and al.sql_idx = sf.index and  al.sentence_id = nf.sentence_id and al.sentence_idx = nf.index "
  sql_string += "and al.sql_id = " + str(sql_id) + " and al.sentence_id = " + str(sentence_id) + " "
  sql_string += "order by sf.index, nf.index;"
  curs.execute(sql_string)
  try: return curs.fetchall()
  except: return None

def get_sqls():
  #sql_string = "select sq.id, sql from experiemtns1.dls_cu_raw as ex, sqls.naive_tb_0_0 as sq, senteces.naive_tb_0 as se where ex.sql_id = sq.id and sq.sentence_id = se.id and sq.is_valid = true order by sq.id;"
  sql_string = "select sq.id, sql "
  sql_string += "from urls.experiment_tb_0 as u, sentences.naive_tb_0 as se, sqls.naive_tb_0_0 as sq "
  sql_string += "where u.url_id = se.url_id and sq.sentence_id = se.id and sq.is_valid = true "
  sql_string += "order by sq.id;"
  curs.execute(sql_string)
  return curs.fetchall()

def get_answers():
  sql_string = "select an.sql_id, an.sentence_id, se.sentence "
  sql_string += "from urls.experiment_tb_0 as u, answers.sql_0_0_nl_0 as an, sentences.naive_tb_0 as se "
  sql_string += "where u.url_id = se.url_id and an.sentence_id = se.id;"
  curs.execute(sql_string)
  return curs.fetchall()

def make_dict(answers):
  pool = {}
  for answer in answers:
    pool[answer[0]] = answer[1:]
  return pool

def make_pool(items):
  pool = []
  for (item,) in items:
    pool.append(item)
  return set(pool)

stime = time.time()
conn_string = "host='localhost' dbname='kjhong' user='kjhong' password='kjhong' port=5432"
conn = psycopg2.connect(conn_string)
curs = conn.cursor()

sqls = get_sqls()
answers = get_answers()
answer_dict = make_dict(answers)
answer_pool = set(answer_dict.keys())
nls_available = make_pool(get_dependency_available(0))
sqls_available = make_pool(get_dependency_available(1))

a1 = 1.0
a2 = -0.1
a3 = 0.0
total_sql_count = 0
import csv
f = open('out.csv', 'w')
wr = csv.writer(f)
total_sql_count = 0
available_sql_count = 0
answer_sql_count = 0
available_answer_count = 0
best_count = 0
correct_count =0
uncorrect_count =0
tp = 0
prec_base = 0
reca_base = 0
negative = 0
row = ['sql id', 'sql', 'available sql', 'there is answer', 'answer id', 'answer', 'available answer' ]
row += ['answer score', 'answer f1', 'answer f2', 'answer f3']
row += ['there is top', 'top is answer', 'top id', 'top sentence', 'top score', 'top f1', 'top f2', 'top f3']
wr.writerow(row)
for (sql_id, sql) in sqls:
  total_sql_count += 1
  row = [sql_id, sql]
  if sql_id not in sqls_available:
    if True: wr.writerow(row + [False])
    continue
  available_sql_count += 1
  row += [True]
  (a_id, a_sentence) = (-1, '')
  if sql_id not in answer_pool:
    row += [False, a_id, a_sentence]
  else:
    answer_sql_count += 1
    (a_id, a_sentence) = answer_dict[sql_id]
    row += [True, a_id, a_sentence]
  if a_id is -1:
    row += [False, -1, -1, -1, -1]
  elif a_id not in nls_available:
    if True: wr.writerow(row + [False])
    continue
  else:
    available_answer_count += 1
    row += [True]
    #print sql_id, a_id
  #  if sql_id == 10896:
  #    print("check")
    (a_score, a_f1, a_f2, a_f3) = get_answer_score(sql_id, a_id, a1, a2, a3)
    #print sql_id, a_score
    row += [a_score, a_f1, a_f2, a_f3]
  best = get_best_sentence(sql_id, a1, a2, a3)
  #if sql_id == 10896:
  #  print(best[2], a_score, a_id)
  if best is None:
  #  if sql_id == 10896:
  #    print('no best')
    if True: wr.writerow(row + [False])
    continue
  best_count += 1
  row += [True]
  (b_id, b_sentence, b_score, b_f1, b_f2, b_f3) = best
  if b_id != -1:
    prec_base += 1
  if a_id != -1:
    reca_base += 1
  else:
    negative += 1
  if b_id == a_id and b_id != -1:
  #  print(sql_id, b_id, b_score)
    tp += 1
  if b_id == a_id:
    row += [True]
    correct_count += 1
  elif a_id != -1:
    row += [False]
    uncorrect_count += 1
  else:
    row += [False]
  row += [b_id, b_sentence, b_score, b_f1, b_f2, b_f3]
  b_alignments = get_alignments(sql_id, b_id)
  for (sw, nw) in b_alignments:
    row += [sw, nw] 
  wr.writerow(row)
#print 'total_sql', total_sql_count
#print 'available_sql', available_sql_count
#print 'answer_sql', answer_sql_count
#print 'available_answer', available_answer_count
#print 'best', best_count
print("Precision: %.2f"%(float(tp)/prec_base))
print("Recall: %.2f"%(float(tp)/reca_base))
print("TP: %d"%tp)
print("positive: %d"%(reca_base))
print("negative: %d"%(negative))
print("precision base: %d"%(prec_base))
print 'correct', correct_count
print 'uncorrect', uncorrect_count
rate = float(correct_count) / float(correct_count + uncorrect_count)
print 'rate', rate
f.close()
#print 'time', time.time() - stime

def filter_ratio(r, inputs):
  true_data = inputs[inputs.label == 1]
  false_data = inputs[inputs.label == 0]
  t_false_data = false_data.sample(n=true_data.__len__() * r)
  r_false_data = false_data[~false_data.index.isin(t_false_data.index.values)]

  traintest_data = true_data.append(t_false_data).values
  remain_data = r_false_data.values

  return traintest_data, remain_data

def rank_result(result, label):
  rank_dict = {}
  for row in result:
    sql_id = int(row[0])
    nl_id = int(row[1])
    if sql_id not in rank_dict.keys():
      rank_dict[sql_id] = {}
    rank_dict[sql_id][nl_id] = row[2]

  test_dict = {}
  for row in label:
    sql_id = int(row[0])
    nl_id = int(row[1])
    if sql_id not in test_dict.keys():
      test_dict[sql_id] = {}
    test_dict[sql_id][nl_id] = row[2]

  # print(rank_dict[10867])
  pred_dict = {}
  for sqlid in rank_dict:
    max_score = 0
    max_nl = -1
    for nlid in rank_dict[sqlid]:
      if max_score < rank_dict[sqlid][nlid]:
        max_score = rank_dict[sqlid][nlid]
        max_nl = nlid
    for nlid in rank_dict[sqlid]:
      if max_score >= threshold:
        if nlid == max_nl:
          rank_dict[sqlid][nlid] = 1
        else:
          rank_dict[sqlid][nlid] = 0
      else:
        rank_dict[sqlid][nlid] = 0
    if max_score >= threshold:
      pred_dict[sqlid] = nlid
    else:
      pred_dict[sqlid] = -1
  answ_dict = {}
  for sqlid in test_dict:
    answ_dict[sqlid] = -1
    for nlid in test_dict[sqlid]:
      if test_dict[sqlid][nlid] == 1:
        answ_dict[sqlid] = nlid

  precision_base = 0
  recall_base = 0
  true_positive = 0
  correct = 0
  wrong = 0
  negative = 0
  for sqlid in pred_dict:
    if pred_dict[sqlid] != -1:
      precision_base += 1
    if answ_dict[sqlid] != -1:
      recall_base += 1
    else:
      negative += 1
    if pred_dict[sqlid] == answ_dict[sqlid] and pred_dict[sqlid] != -1:
      true_positive += 1
    if pred_dict[sqlid] == answ_dict[sqlid]:
      correct += 1
    elif answ_dict[sqlid] != -1:
      wrong += 1
 
  print("positive: %d"%recall_base)
  print("negative: %d"%negative)
  print("Precision base: %d"%precision_base)
  print("Correct: %d"%correct)
  print("Wrong: %d"%wrong)
  print("Precision: %.2f"%(true_positive / float(precision_base)))
  print("Recall: %.2f"%(true_positive / float(recall_base)))
  print("Rate: %.2f"%(float(correct) / (correct+wrong)))

threshold = 0.2
test_ratio = 0.2
tf_ratio = 3

feats_all = np.array(get_all_nl_feat())
feats_pd = pd.DataFrame({'sqlid': feats_all[:,0],
                         'nlid': feats_all[:,1],
                         'feat1': feats_all[:,2],
                         'feat2': feats_all[:,3],
                         'feat3': feats_all[:,4],
                         'label': feats_all[:,5]
                         })
feats_pd = feats_pd[['sqlid', 'nlid', 'feat1', 'feat2', 'feat3', 'label']]

t_result, r_result = filter_ratio(tf_ratio, feats_pd)
features = t_result[:, :5]
labels = t_result[:, 5]
train_feature, test_feature, train_label, test_label = train_test_split(features, labels, test_size=test_ratio, random_state=7)

# print(feats_pd[feats_pd.label==1])
test_data = np.vstack([test_feature, r_result[:, :5]])
test_feature = np.vstack([test_feature[:, 2:5], r_result[:, 2:5]])
test_label = np.append(test_label, r_result[:, 5])

model = XGBRegressor(objective='binary:logistic')
#model = XGBClassifier()
train_feature = train_feature[:, 2:5]
model.fit(train_feature, train_label)

y_pred = model.predict(test_feature)

test_result = np.hstack([test_data[:, :2], y_pred.reshape(-1, 1)])
indexed_label = np.hstack([test_data[:, :2], test_label.reshape(-1, 1)])
rank_result(test_result, indexed_label)

