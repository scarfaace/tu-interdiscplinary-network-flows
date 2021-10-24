#%%
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, plot_confusion_matrix
from sklearn.model_selection import train_test_split

#%%
# Read data
mergedAllDf = pd.read_csv("./model/data/Friday_transcription_no-labels_labeled.tsv", sep='\t', quoting=3)
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
    train_test_split(attacksDf, attacksDf.Label, test_size=0.2, random_state=123)
X_train_nonAttacks, X_test_nonAttacks, y_train_nonAttacks, y_test_nonAttacks = \
    train_test_split(nonAttacksDf, nonAttacksDf.Label, test_size=0.2, random_state=123)

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
sample_weight = np.array([8 if i == 1 else 1 for i in y_train])

#%%
# model = LogisticRegression()
model = RandomForestClassifier(random_state=20)
model.fit(X_train_words, y_train, sample_weight=sample_weight)
print("Train set score: {:.3f}".format(model.score(X_train_words, y_train)))
print("Test set score:  {:.3f}".format(model.score(X_test_words, y_test)))


#%%
predictions = model.predict(X_test_words)
cf1 = confusion_matrix(y_test, predictions)
print("Confusion matrix:\n{}".format(cf1))


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


#%%
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegressionCV, PassiveAggressiveClassifier, RidgeClassifierCV, SGDClassifier, Perceptron
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import ExtraTreeClassifier, DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score

random_seed = 123
MLA = [
    #Ensemble Methods
    AdaBoostClassifier(random_state=random_seed),
    BaggingClassifier(random_state=random_seed),
    ExtraTreesClassifier(random_state=random_seed),
    GradientBoostingClassifier(random_state=random_seed),
    RandomForestClassifier(random_state=random_seed),

    # GLM
    LogisticRegressionCV(random_state=random_seed),
    PassiveAggressiveClassifier(random_state=random_seed),
    RidgeClassifierCV(),
    SGDClassifier(random_state=random_seed),
    Perceptron(random_state=random_seed),

    # Navies Bayes
    BernoulliNB(),

    # SVM
    SVC(probability=True, random_state=random_seed),
    # NuSVC(probability=True, random_state=random_seed),
    LinearSVC(random_state=random_seed),

    # Trees
    DecisionTreeClassifier(random_state=random_seed),
    ExtraTreeClassifier(random_state=random_seed)

]

MLA_columns = ['MLA Name', 'MLA Parameters', 'MLA Test Accuracy', 'MLA Test F1', 'MLA Confusion Matrix']
MLA_compare = pd.DataFrame(columns = MLA_columns)

row_index = 0
for alg in MLA:
    # set name and parameters
    MLA_name = alg.__class__.__name__
    MLA_compare.loc[row_index, 'MLA Name'] = MLA_name
    MLA_compare.loc[row_index, 'MLA Parameters'] = str(alg.get_params())

    # score model with cross validation: http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html#sklearn.model_selection.cross_validate
    # cv_results = model_selection.cross_validate(alg, X_train, y_train)
    alg.fit(X_train_words, y_train)
    y_pred = alg.predict(X_test_words)
    score = accuracy_score(y_test, y_pred)
    cf = confusion_matrix(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    MLA_compare.loc[row_index, 'MLA Test Accuracy'] = score
    MLA_compare.loc[row_index, 'MLA Confusion Matrix'] = cf
    MLA_compare.loc[row_index, 'MLA Test F1'] = f1

    row_index += 1

MLA_compare.to_csv("classifier.csv")