#------------------------------------------------------------------------------------------------#
#                                           Imports                                              #
#------------------------------------------------------------------------------------------------#

import numpy as np
import pandas as pd

from sklearn.preprocessing import scale
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import make_scorer, accuracy_score, balanced_accuracy_score, f1_score, precision_score, recall_score

from flask import Flask, jsonify, request, make_response

#------------------------------------------------------------------------------------------------#
#                                       Modelling methods                                        #
#------------------------------------------------------------------------------------------------#

def log_reg_grid_search(hyperparameters, x_train, y_train, balanced=False, refit="accuracy_score"):
    """
        Perform multiclass logistic regression cross validation grid search to obtain the best parameters.
        The refit parameter is performed on accuracy by default. 

        Args:

            hyperparameters: <dict>
                Dictionary of multiple hyperparameters to perform grid search on.

            x_train: <numpy.ndarray>
                multidimensional array containing the training dataset.

            y_train: <numpy.ndarray>
                multidimensional array containing the target classification data.

            balanced: <bool>, default=False
                Parameter defining dataset was balanced during preprocessing or not. 

            refit: <bool>, <str>, or callable, default=True
                Refit an estimator using the best found parameters on the whole dataset.

        Attributes:

            best_params_: <dict>
                Parameter setting that gave the best results on the hold out data.
                For multi-metric evaluation, this is present only if refit is specified.

    """

    if balanced == False:
        hyperparameters.update({"class_weight":["balanced"]})

        scoring = {
            'accuracy_score': make_scorer(balanced_accuracy_score),
            'f1_score': make_scorer(f1_score, average="weighted"),
            'precision_score': make_scorer(precision_score, average="weighted"),
            'recall_score': make_scorer(recall_score, average="weighted")
        }

    else:
        hyperparameters.pop("class_weight",None)

        scoring = {
            'accuracy_score': make_scorer(accuracy_score),
            'f1_score': make_scorer(f1_score, average="macro"),
            'precision_score': make_scorer(precision_score, average="macro"),
            'recall_recall_score': make_scorer(recall_score, average="macro")
        }

    log_reg = GridSearchCV(
            estimator = LogisticRegression(), 
            param_grid = hyperparameters, 
            scoring=scoring,
            verbose=2, 
            n_jobs=-1,
            cv=5,
            refit=refit
        )

    training_results = log_reg_final_model.fit(x_train, y_train)
    
    return training_results.best_params_

