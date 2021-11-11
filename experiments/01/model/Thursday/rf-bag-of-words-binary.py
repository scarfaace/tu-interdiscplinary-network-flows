#%%
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, plot_confusion_matrix, classification_report
from sklearn.experimental import enable_halving_search_cv
from sklearn.model_selection import cross_val_score, HalvingGridSearchCV
from sklearn.model_selection import train_test_split

#%%
# Read data
mergedAllDf = pd.read_csv("experiments/01/transcription/out/Thursday_transcription_labeled.tsv", sep='\t', quoting=3)
nonAttacksDf = mergedAllDf[mergedAllDf.Label == 0].sample(n=20000, random_state=123)
attacksDf = mergedAllDf[mergedAllDf.Label == 1]

nonAttacksDf = nonAttacksDf[['Label', 'transcription']]
attacksDf = attacksDf[['Label', 'transcription']]

#%%
# Samples per class
commonDf = pd.concat([nonAttacksDf, attacksDf])
print("Samples per class: {}".format(np.bincount(commonDf['Label'])))


#%%
# Create train and test data
X_train_attacks, X_test_attacks, y_train_attacks, y_test_attacks = \
    train_test_split(attacksDf, attacksDf.Label, test_size=0.3, random_state=123)
X_train_nonAttacks, X_test_nonAttacks, y_train_nonAttacks, y_test_nonAttacks = \
    train_test_split(nonAttacksDf, nonAttacksDf.Label, test_size=0.3, random_state=123)

X_train = pd.concat([X_train_attacks, X_train_nonAttacks])['transcription']
X_test = pd.concat([X_test_attacks, X_test_nonAttacks])['transcription']
y_train = pd.concat([y_train_attacks, y_train_nonAttacks])
y_test = pd.concat([y_test_attacks, y_test_nonAttacks])


#%%
# Samples per class in TRAIN and TEST data
print("TRAIN: Samples per class: {}".format(np.bincount(y_train)))
print("TEST:  Samples per class: {}".format(np.bincount(y_test)))


#%%
# Create bag of words
# https://www.youtube.com/watch?v=KE53PAfVJ5c
vectorizer = CountVectorizer(token_pattern=r".", lowercase=False)  # possibly add vocabulary parameter

vectorizer.fit(commonDf['transcription'].values.astype('U'))
vocabulary = vectorizer.get_feature_names()
print('Feature names:', vocabulary)


#%%
X_train_words = vectorizer.transform(X_train.values.astype('U'))
X_test_words = vectorizer.transform(X_test.values.astype('U'))


#%%
# # Logistic Regression CV
# cv_scores = cross_val_score(LogisticRegression(), X_train_words, y_train)
# print("Mean CV accuracy: {:.2f}".format(np.mean(cv_scores)))


#%%
model = LogisticRegression()
sample_weight = np.array([13 if i == 1 else 1 for i in y_train])
model = RandomForestClassifier(random_state=20, n_jobs=-1)
model.fit(X_train_words, y_train, sample_weight=sample_weight)
print("Train set score: {:.3f}".format(model.score(X_train_words, y_train)))
# print("Test set score:  {:.3f}".format(model.score(X_test_words, y_test)))

# param_grid = {
#     'max_depth': [None, 10, 11, 12, 13, 14, 15],
#     'min_samples_split': [2, 3, 5, 8, 10, 15, 20, 30]
# }
#
# base_estimator = RandomForestClassifier(n_estimators=100, class_weight='balanced_subsample', verbose=0, n_jobs=-1, random_state=2021)
#
# grid_search = HalvingGridSearchCV(base_estimator, param_grid, cv=5, factor=2, resource='n_estimators', max_resources=20, random_state=2021, n_jobs=-1, verbose=1)
# grid_search.fit(X_train_words, y_train)
# model = grid_search.best_estimator_

#%%
predictions = model.predict(X_test_words)
confusion_matrix_result = confusion_matrix(y_test, predictions)

print(classification_report(y_test, predictions))

# predictionsDf: DataFrame = pd.DataFrame({
#     'transcription': X_test,
#     'Label': y_test,
#     'Label_predicted': predictions
# })
# predictionsDf.to_csv('predictions.csv', index=False, sep="\t", quoting=3)

#%%
# https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
titles_options = [("Confusion matrix, without normalization", None, '.0f'),
                  ("Normalized confusion matrix", 'true', '.3f')]
for title, normalize, values_format in titles_options:
    disp = plot_confusion_matrix(model, X_test_words, y_test,
                                 cmap=plt.cm.Blues,
                                 normalize=normalize,
                                 values_format=values_format)
    disp.ax_.set_title(title)

    print(title)
    print(disp.confusion_matrix)
    plt.show()
