from xgboost import XGBClassifier
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import sys

# Load feature_label data made by save_feature.py
feats_w = np.loadtxt("feature_answer_all.txt")
feats_c = np.loadtxt("feature_answer_all_crowdsourcing_tf.txt")

feats_w_pd = pd.DataFrame({'sqlid': feats_w[:,0],
                        'nlid': feats_w[:,1],
                        'feat1': feats_w[:,2],
                        'feat2': feats_w[:,3],
                        'feat3': feats_w[:,4],
                        'label': feats_w[:,5]
                        })
feats_c_pd = pd.DataFrame({'sqlid': feats_c[:,0],
                        'nlid': feats_c[:,1],
                        'feat1': feats_c[:,2],
                        'feat2': feats_c[:,3],
                        'feat3': feats_c[:,4],
                        'label': feats_c[:,5]
                        })
#try:
#    c_num = int(sys.argv[2])
#except:
#    c_num = -1
#
#if c_num != -1:
#    feats_c_pd = feats_c_pd.sample(n=c_num)

# feats_pd = feats_w_pd.append(feats_c_pd)


#np.random.shuffle(feats)

# Parameters
test_ratio = 0.2
params = {'objective': 'binary:logistic',
        'eval_metric' : 'auc',
        'learning_rate' : 0.1,
        'max_depth': 1,
        'min_child_weight': 1,
        'subsample': 1,
        'colsample_bytree': 1,
        'gamma' : 0,
        'reg_alpha': 0,
        'reg_lambda': 1}

num_round = 100
tf_ratio = int(sys.argv[1])

def filter_ratio(r, inputs):
    true_data = inputs[inputs.label == 1]
    false_data = inputs[inputs.label == 0]
    t_false_data = false_data.sample(n=true_data.__len__() * r)
    r_false_data = false_data[~false_data.index.isin(t_false_data.index.values)]
    
    traintest_data = true_data.append(t_false_data).values
    remain_data = r_false_data.values

    return traintest_data, remain_data

t_result_w, r_result_w = filter_ratio(tf_ratio, feats_w_pd)
features_w = t_result_w[:, :5]
labels_w = t_result_w[:, 5]
train_feature_w, test_feature_w, train_label_w, test_label_w = train_test_split(features_w, labels_w, test_size=test_ratio, random_state=7)

t_result_c, r_result_c = filter_ratio(tf_ratio, feats_c_pd)
features_c = t_result_c[:, :5]
labels_c = t_result_c[:, 5]
train_feature_c, test_feature_c, train_label_c, test_label_c = train_test_split(features_c, labels_c, test_size=test_ratio, random_state=7)

train_feature = np.vstack([train_feature_w, train_feature_c])
train_label = np.append(train_label_w, train_label_c)

test_feature_w = np.vstack([test_feature_w, r_result_w[:, :5]])
test_label_w = np.vstack([test_label_w.reshape(-1, 1), r_result_w[:, 5].reshape(-1, 1)]).reshape(-1)
test_feature_c = np.vstack([test_feature_c, r_result_c[:, :5]])
test_label_c = np.vstack([test_label_c.reshape(-1, 1), r_result_c[:, 5].reshape(-1, 1)]).reshape(-1)

# Train model
model = XGBClassifier()
train_feature = train_feature[:, 2:5]
#print(train_feature.shape)
model.fit(train_feature, train_label)
#print("Training Done!")

# Make prediction
test_pred_w = test_feature_w[:, 2:5]
test_pred_c = test_feature_c[:, 2:5]
y_pred_w = model.predict(test_pred_w)
y_pred_c = model.predict(test_pred_c)
y_pred = np.append(y_pred_w, y_pred_c)
predictions_w = [round(value) for value in y_pred_w]
predictions_c = [round(value) for value in y_pred_c]
predictions = [round(value) for value in y_pred]

test_label = np.append(test_label_w, test_label_c)

# Measure accuracy
def measure_only_true(true_label, pred, indent):
    numpy_pred = np.array(pred)
    tp = ((numpy_pred == 1) * (true_label == 1)).sum()
    fp = ((numpy_pred == 1) * (true_label == 0)).sum()
    fn = ((numpy_pred == 0) * (true_label == 1)).sum()
    tn = ((numpy_pred == 0) * (true_label == 0)).sum()
#    print("True Positive: %d" % tp)
#    print("False Positive: %d" % fp)
#    print("False Negative: %d" % fn)
#    print("True Negative: %d" % tn)
    if indent:
        print("    Precision: %.2f" % (float(tp) / (tp + fp)))
        print("    Recall: %.2f" % (float(tp) / (tp + fn)))
    else:
        print("  Precision: %.2f" % (float(tp) / (tp + fp)))
        print("  Recall: %.2f" % (float(tp) / (tp + fn)))

def print_fp_case(true_label, pred):
    numpy_pred = np.array(pred)
    fn_case = ((numpy_pred == 1) * (true_label == 0))
    fn_idx = []
    for idx, val in enumerate(fn_case):
        if val == 1:
            fn_idx.append(idx)
    fp_case_feats = None

    for idx in fn_idx:
        if fp_case_feats is None:
            fp_case_feats = test_feature[idx, 0:2]
        else:
            fp_case_feats = np.vstack([fp_case_feats, test_feature[idx, 0:2]])

    np.savetxt("fp_case_feat.txt", fp_case_feats)

accuracy_w = accuracy_score(test_label_w, predictions_w)
accuracy_c = accuracy_score(test_label_c, predictions_c)
accuracy = accuracy_score(test_label, predictions)
print("True-False Ratio: 1:" + sys.argv[1] + ", Crowdsourcing_num: " + str(feats_c_pd.__len__()))
print("  Accuracy: %.2f%%" % (accuracy * 100))
measure_only_true(test_label, predictions, 0)
print("  Web data")
print("    Accuracy_w: %.2f%%" % (accuracy_w * 100.0))
measure_only_true(test_label_w, predictions_w, 1)
print("  Crowdsourcing")
print("    Accuracy_c: %.2f%%" % (accuracy_c * 100.0)) 
measure_only_true(test_label_c, predictions_c, 1)
#print_fp_case(test_label, predictions)
