#%%
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

#%%
# Read data
mergedAllDf = pd.read_csv("transcription/out/merged_all.tsv", sep='\t', quoting=3)
nonAttacksDf = mergedAllDf[mergedAllDf.label == 0].sample(n=1200, random_state=123)
attacksDf = mergedAllDf[mergedAllDf.label == 1]

nonAttacksDf = nonAttacksDf[['label', 'transcription']]
attacksDf = attacksDf[['label', 'transcription']]


#%%
# Samples per class
commonDf = pd.concat([nonAttacksDf, attacksDf])
print("Samples per class: {}".format(np.bincount(commonDf['label'])))


#%%
# Create train and test data
X_train_attacks, X_test_attacks, y_train_attacks, y_test_attacks = \
    train_test_split(attacksDf, attacksDf.label, test_size=0.2, random_state=123)
X_train_nonAttacks, X_test_nonAttacks, y_train_nonAttacks, y_test_nonAttacks = \
    train_test_split(nonAttacksDf, nonAttacksDf.label, test_size=0.2, random_state=123)

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
# model = LogisticRegression()
model = RandomForestClassifier()
model.fit(X_train_words, y_train)
print("Train set score: {:.3f}".format(model.score(X_train_words, y_train)))
print("Test set score:  {:.3f}".format(model.score(X_test_words, y_test)))


#%%
predictions = model.predict(X_test_words)
confusion_matrix = confusion_matrix(y_test, predictions)
print("Confusion matrix:\n{}".format(confusion_matrix))
