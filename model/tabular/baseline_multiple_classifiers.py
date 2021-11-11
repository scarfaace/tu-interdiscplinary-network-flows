#%%
import numpy as np
import pandas as pd

#%% Setting initial constants
filename = "model/tabular/Friday_labeled_training.csv"
target = "Label"

#%% Loading the data from directory
print("Loading training dataset...")
df = pd.read_csv(filename)
y_train = df[target].to_numpy()

#%%
X_train = df.drop(columns=['flowStartMilliseconds', 'sourceIPAddress', 'destinationIPAddress', 'Label', 'Attack']).to_numpy()

X_train = np.nan_to_num(X_train)
y_train = np.nan_to_num(y_train)

#%% Reading test data
df_test = pd.read_csv('model/tabular/Friday_labeled_test.csv')
y_test = df_test[target].to_numpy()

X_test = df_test.drop(columns=['flowStartMilliseconds','sourceIPAddress','destinationIPAddress','Label','Attack']).to_numpy()
X_test = np.nan_to_num(X_train)
y_test = np.nan_to_num(y_train)

#%% Counting the number of attacks in the source file
unique, counts = np.unique(y_train, return_counts=True)
dict(zip(unique, counts))


#%% Classifier definition
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier, ExtraTreesClassifier, GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import PassiveAggressiveClassifier, RidgeClassifierCV, SGDClassifier, Perceptron
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import ExtraTreeClassifier, DecisionTreeClassifier
from sklearn.linear_model import LogisticRegressionCV
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

#%%
MLA_columns = ['MLA Name', 'MLA Parameters', 'MLA Test Report', 'MLA Test F1', 'MLA Test Average Precision']
MLA_compare = pd.DataFrame(columns = MLA_columns)

#%%
from sklearn.metrics import classification_report, average_precision_score, f1_score
row_index = 0
for alg in MLA:
    # set name and parameters
    MLA_name = alg.__class__.__name__
    MLA_compare.loc[row_index, 'MLA Name'] = MLA_name
    MLA_compare.loc[row_index, 'MLA Parameters'] = str(alg.get_params())

    # score model with cross validation: http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html#sklearn.model_selection.cross_validate
    # cv_results = model_selection.cross_validate(alg, X_train, y_train)
    alg.fit(X_train, y_train)
    y_pred = alg.predict(X_test)
    # score = accuracy_score(y_test, y_pred)
    report = classification_report(y_true=y_test, y_pred=y_pred)
    ap = average_precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    importance = alg.coef_

    MLA_compare.loc[row_index, 'MLA Test Report'] = report
    MLA_compare.loc[row_index, 'MLA Test F1'] = f1
    MLA_compare.loc[row_index, 'MLA Test Average Precision'] = ap

    row_index += 1


MLA_compare.to_csv("baseline_classifiers.csv")
