from xgboost import XGBClassifier
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import sys
import pickle
import json

import argparse

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


def main(args):
    # Load feature_label data made by save_feature.py
    feats = np.loadtxt(args.F)
    params = json.load(open(args.P))

    # Parameters
    test_ratio = params['test_ratio']
    num_round = params['num_round']
    model_params = params['model']

    features = feats[:, :5]
    labels = feats[:, 5]

    if model_params['pretrained_model'] != '':
        model_path = model_params['pretrained_model']
        model = pickle.load(open(model_path, 'rb'))
        test_ratio = 1
    else:
        model = XGBClassifier(**model_params)

    train_feature, test_feature, train_label, test_label = train_test_split(features, labels, test_size=test_ratio, random_state=7)

    # Train the model
    train_feature = train_feature[:, 2:5]
    model.fit(train_feature, train_label)

    # Make prediction
    test_pred = test_feature[:, 2:5]
    y_pred = model.predict(test_pred)
    predictions = [round(value) for value in y_pred]

    accuracy = accuracy_score(test_label, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100))
    measure_only_true(test_label, predictions, 0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--features', required=False, dest='F',
                        help='Path to final feature file. Defualt: "./feature_answer_all.txt"',
                        default='feature_answer_all.txt')
    parser.add_argument('--parameters', required=False, dest='P',
                        help='Path to parameter file. Defualt: "./params.json"',
                        default='params.json')
    parser.add_argument('--model', required=True, dest='M',
                        help='Model type to use (xgb/neural)')

    args = parser.parse_args()
    main(args)
