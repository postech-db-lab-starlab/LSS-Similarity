from xgboost import XGBClassifier
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import sys
import pickle

# Load feature_label data made by save_feature.py
feats = np.loadtxt("feature_answer_all.txt")

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

features = feats[:, :5]
labels = feats[:, 5]


if len(sys.argv) > 1:
    model_path = sys.argv[1]
    model = pickle.load(open(model_path, 'rb'))
    test_ratio = 1
else:
    model = XGBClassifier()

train_feature, test_feature, train_label, test_label = train_test_split(features, labels, test_size=test_ratio, random_state=7)

# Train the model
train_feature = train_feature[:, 2:5]
model.fit(train_feature, train_label)

# Make prediction
test_pred = test_feature[:, 2:5]
y_pred = model.predict(test_pred)
predictions = [round(value) for value in y_pred]

# Measure accuracy
def measure_only_true(true_label, pred, indent):
    numpy_pred = np.array(pred)
    tp = ((numpy_pred == 1) * (true_label == 1)).sum()
    fp = ((numpy_pred == 1) * (true_label == 0)).sum()
    fn = ((numpy_pred == 0) * (true_label == 1)).sum()
    tn = ((numpy_pred == 0) * (true_label == 0)).sum()
    print("  True Positive: %d" % tp)
    print("  False Positive: %d" % fp)
    print("  False Negative: %d" % fn)
    print("  True Negative: %d" % tn)
    print("-----------------------------")
    print("  Precision: %.2f" % (float(tp) / (tp + fp)))
    print("  Recall: %.2f" % (float(tp) / (tp + fn)))
    print("=============================")

accuracy = accuracy_score(test_label, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100))
measure_only_true(test_label, predictions, 0)
