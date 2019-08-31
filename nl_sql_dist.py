from xgboost import XGBClassifier
from neural_model import NeuralClassifier

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


def run_xgb_model(model_params, train_feature, train_label, test_feature, pretrained_model=''):
    if pretrained_model != '':
        model = pickle.load(open(pretrained_model, 'rb'))
    else:
        model = XGBClassifier(**model_params)
        model.fit(train_feature, train_label)

    # Make prediction
    y_pred = model.predict(test_feature)
    predictions = [round(value) for value in y_pred]

    return predictions


def run_neural_model(model_params, train_feature, train_label, test_feature, pretrained_model=''):
    if pretrained_model != '':
        model = torch.load(pretrained_model)
    else:
        model = NeuralClassifier(**model_params)
        model.train(train_feature, train_label)

    y_pred = model.predict(test_feature)
    predictions = [round(value) for value in y_pred]

    return predictions


def main(args):
    # Load feature_label data made by save_feature.py
    feats = np.loadtxt(args.F)
    params = json.load(open(args.P))

    # Parameters
    model_params = params['model']
    test_ratio = 1 if params['pretrained_model'] != '' else params['test_ratio']

    features = feats[:, :5]
    labels = feats[:, 5]

    train_feature, test_feature, train_label, test_label = train_test_split(features, labels, test_size=test_ratio, random_state=7)

    # Remove SQL id and NL id
    train_feature = train_feature[:, 2:5]
    test_feature = test_feature[:, 2:5]

    if params['model_type'] == 'xgb':
        predictions = run_xgb_model(model_params, train_feature, train_label, test_feature, params['pretrained_model'])
    elif params['model_type'] == 'neural':
        predictions = run_neural_model(model_params, train_feature, train_label, test_feature, params['pretrained_model'])
    else:
        raise Exception("Model should be 'xgb' or 'neural'")

    accuracy = accuracy_score(test_label, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100))
    measure_only_true(test_label, predictions, 0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--features', required=False, dest='F',
                        help='Path to final feature file. Defualt: "./feature_answer_all.txt"',
                        default='feature_answer_all.txt')
    parser.add_argument('--parameters', required=False, dest='P',
                        help='Path to parameter file. Defualt: "./xgb_params.json"',
                        default='xgb_params.json')

    args = parser.parse_args()
    main(args)
