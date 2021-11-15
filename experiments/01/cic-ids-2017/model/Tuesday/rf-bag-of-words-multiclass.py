#%%
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pandas import DataFrame, Series
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, plot_confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

#%%
# Read data
mergedAllDf = pd.read_csv("experiments/01/transcription/out/Tuesday_transcription_labeled.tsv", sep='\t', quoting=3)
nonAttacksDf = mergedAllDf[mergedAllDf.Attack == 'Normal'].sample(n=5500, random_state=123)
attacksDf = mergedAllDf[mergedAllDf.Attack != 'Normal']

nonAttacksDf = nonAttacksDf[['Attack', 'transcription']]
attacksDf = attacksDf[['Attack', 'transcription']]

#%%
# Samples per class
def get_sample_counts_per_class(label_series: Series):
    bins, counts = np.unique(label_series, return_counts=True)
    bin_counts = {}
    for i in range(0, len(bins)):
        bin_counts[bins[i]] = counts[i]
    return dict(sorted(bin_counts.items()))

commonDf = pd.concat([nonAttacksDf, attacksDf])
print("Samples per class: {}".format(get_sample_counts_per_class(commonDf['Attack'])))

#%%
# Create train and test data
X_train_attacks, X_test_attacks, y_train_attacks, y_test_attacks = \
    train_test_split(attacksDf, attacksDf.Attack, test_size=0.3, random_state=123)
X_train_nonAttacks, X_test_nonAttacks, y_train_nonAttacks, y_test_nonAttacks = \
    train_test_split(nonAttacksDf, nonAttacksDf.Attack, test_size=0.3, random_state=123)

X_train = pd.concat([X_train_attacks, X_train_nonAttacks])['transcription']
X_test = pd.concat([X_test_attacks, X_test_nonAttacks])['transcription']
y_train = pd.concat([y_train_attacks, y_train_nonAttacks])
y_test = pd.concat([y_test_attacks, y_test_nonAttacks])


#%%
# Samples per class in TRAIN and TEST data
print('TRAIN: Samples per class: {}'.format(get_sample_counts_per_class(y_train)))
print('TEST: Samples per class: {}'.format(get_sample_counts_per_class(y_test)))


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
model = RandomForestClassifier(random_state=20, n_jobs=-1)
model.fit(X_train_words, y_train)
print("Train set score: {:.3f}".format(model.score(X_train_words, y_train)))
print("Test set score:  {:.3f}".format(model.score(X_test_words, y_test)))


#%%
predictions = model.predict(X_test_words)
confusion_matrix_result = confusion_matrix(y_test, predictions)
print("Confusion matrix:\n{}".format(confusion_matrix_result))

predictionsDf: DataFrame = pd.DataFrame({
    'transcription': X_test,
    'Attack': y_test,
    'Attack_predicted': predictions
})
predictionsDf.to_csv('predictions.csv', index=False, sep="\t", quoting=3)

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
