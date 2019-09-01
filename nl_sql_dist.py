from xgboost import XGBClassifier
from model.neural_model import NeuralClassifier

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, roc_curve, auc
from sklearn.model_selection import train_test_split
import sys
import pickle
import json
import matplotlib.pyplot as plt

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


def run_xgb_model(model_params, train_feature, train_label, test_feature, save_model=False, pretrained_model=''):
    if pretrained_model != '':
        model = pickle.load(open(pretrained_model, 'rb'))
    else:
        model = XGBClassifier(**model_params)
        model.fit(train_feature, train_label)

    return model


def run_neural_model(model_params, train_feature, train_label, test_feature, save_model=False, pretrained_model=''):
    if pretrained_model != '':
        model = torch.load(pretrained_model)
    else:
        model = NeuralClassifier(**model_params)
        model.trainer(train_feature, train_label)

    return model


def draw_roc_curve(pred, target):
    fpr, tpr, threshold = roc_curve(target, pred)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange',
             lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()


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
        model = run_xgb_model(model_params,
                              train_feature, train_label, test_feature,
                              params['pretrained_model'])
        if params['save_model']:
            pickle.dump(model, open('data/saved_model/XGB_MODEL.dat', "wb"))
    elif params['model_type'] == 'neural':
        model = run_neural_model(model_params,
                                 train_feature, train_label, test_feature,
                                 params['pretrained_model'])
        if params['save_model']:
            torch.save(model.state_dict, 'data/saved_model/NEURAL_MODEL.dat')
    else:
        raise Exception("Model should be 'xgb' or 'neural'")

    # Make prediction
    y_pred = model.predict(test_feature)
    predictions = [round(value) for value in y_pred]

    accuracy = accuracy_score(test_label, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100))
    measure_only_true(test_label, predictions, 0)

    draw_roc_curve(y_pred, test_label)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--features', required=False, dest='F',
                        help='Path to final feature file. Defualt: "./feature_answer_all.txt"',
                        default='data/feature_answer_all.txt')
    parser.add_argument('--parameters', required=False, dest='P',
                        help='Path to parameter file. Defualt: "./xgb_params.json"',
                        default='config/xgb_params.json')

    args = parser.parse_args()
    main(args)
