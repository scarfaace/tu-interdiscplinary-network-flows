#%%
from argparse import ArgumentParser

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, classification_report, plot_confusion_matrix
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import HalvingGridSearchCV
from sklearn.model_selection import train_test_split


def read_data(dataset_filepath: str, nonAttacks_subsample_size: int):
    mergedAllDf = pd.read_csv(dataset_filepath, sep='\t', quoting=3)

    nonAttacksDf = mergedAllDf[mergedAllDf.Label == 0].sample(n=nonAttacks_subsample_size, random_state=123)
    attacksDf = mergedAllDf[mergedAllDf.Label == 1]

    nonAttacksDf = nonAttacksDf[['Label', 'transcription']]
    attacksDf = attacksDf[['Label', 'transcription']]

    commonDf = pd.concat([nonAttacksDf, attacksDf])
    print("Samples per class: {}".format(np.bincount(commonDf['Label'])))

    return commonDf, attacksDf, nonAttacksDf


#%%
def create_train_test_split(attacksDf: DataFrame, nonAttacksDf: DataFrame):
    X_train_attacks, X_test_attacks, y_train_attacks, y_test_attacks = \
        train_test_split(attacksDf, attacksDf.Label, test_size=0.3, random_state=123)
    X_train_nonAttacks, X_test_nonAttacks, y_train_nonAttacks, y_test_nonAttacks = \
        train_test_split(nonAttacksDf, nonAttacksDf.Label, test_size=0.3, random_state=123)

    X_train = pd.concat([X_train_attacks, X_train_nonAttacks])['transcription']
    X_test = pd.concat([X_test_attacks, X_test_nonAttacks])['transcription']
    y_train = pd.concat([y_train_attacks, y_train_nonAttacks])
    y_test = pd.concat([y_test_attacks, y_test_nonAttacks])

    print("TRAIN: Samples per class: {}".format(np.bincount(y_train)))
    print("TEST:  Samples per class: {}".format(np.bincount(y_test)))

    return X_train, y_train, X_test, y_test


def create_bag_of_words(X_train, X_test, commonDf: DataFrame):
    # https://www.youtube.com/watch?v=KE53PAfVJ5c
    vectorizer = CountVectorizer(token_pattern=r".", lowercase=False)  # possibly add vocabulary parameter

    vectorizer.fit(commonDf['transcription'].values.astype('U'))
    vocabulary = vectorizer.get_feature_names()
    print('Feature names:', vocabulary)

    X_train_words = vectorizer.transform(X_train.values.astype('U'))
    X_test_words = vectorizer.transform(X_test.values.astype('U'))

    return X_train_words, X_test_words

def fit_model(X_train_words, y_train, is_halving_grid_search_cv: bool):
    if is_halving_grid_search_cv:
        param_grid = {
            'max_depth': [10, 11, 12, 13, 14, 15],
            'min_samples_split': [3, 5, 8, 10, 15, 20, 30]
        }

        base_estimator = RandomForestClassifier(n_estimators=100, class_weight='balanced_subsample', verbose=0, n_jobs=-1, random_state=2021)

        grid_search = HalvingGridSearchCV(base_estimator, param_grid, cv=5, factor=2, resource='n_estimators', max_resources=20, random_state=2021, n_jobs=-1, verbose=1)
        grid_search.fit(X_train_words, y_train)
        model = grid_search.best_estimator_
    else:
        sample_weight = np.array([1 if i == 1 else 1 for i in y_train])
        model = RandomForestClassifier(random_state=20)
        model.fit(X_train_words, y_train, sample_weight=sample_weight)
        # print("Train set score: {:.3f}".format(model.score(X_train_words, y_train)))
        # print("Test set score:  {:.3f}".format(model.score(X_test_words, y_test)))

    return model


def predict(model, X_test, y_test):
    predictions = model.predict(X_test)
    return predictions

    # predictionsDf: DataFrame = pd.DataFrame({
    #     'transcription': X_test,
    #     'Label': y_test,
    #     'Label_predicted': predictions
    # })
    # predictionsDf.to_csv('predictions.csv', index=False)


def print_prediction_results(model, predictions, X_test, y_test):
    confusion_matrix_result = confusion_matrix(y_test, predictions)
    print("Confusion matrix:\n{}".format(confusion_matrix_result))

    print(classification_report(y_test, predictions))

    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    titles_options = [("Confusion matrix, without normalization", None, '.0f'),
                      ("Normalized confusion matrix", 'true', '.3f')]
    for title, normalize, values_format in titles_options:
        disp = plot_confusion_matrix(model, X_test, y_test,
                                     cmap=plt.cm.Blues,
                                     normalize=normalize,
                                     values_format=values_format)
        disp.ax_.set_title(title)

        print(title)
        print(disp.confusion_matrix)
        # plt.show()


def main():
    parser = ArgumentParser(description="")
    parser.add_argument("--dataset-path", type=str, required=True, help="Path to the dataset CSV file.")
    parser.add_argument("--non-attacks-subsample-size", type=int, required=False, help="Size of the non-attacks subsample.", default=5000)
    parser.add_argument("--HalvingGridSearchCV", help="Path to the dataset CSV file.", default=False, type=lambda x: (str(x).lower() == 'true'))
    arguments = parser.parse_args()

    dataset_path = arguments.dataset_path
    nonAttacks_subsample_size = arguments.non_attacks_subsample_size
    is_halving_grid_search_cv = arguments.HalvingGridSearchCV

    commonDf, attacksDf, nonAttacksDf = read_data(dataset_path, nonAttacks_subsample_size)
    X_train, y_train, X_test, y_test = create_train_test_split(attacksDf, nonAttacksDf)

    model = fit_model(X_train, y_train, is_halving_grid_search_cv)
    predict(model, X_test, y_test)

main()

