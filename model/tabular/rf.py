#%%
import numpy as np
import pandas as pd

#%% Setting initial constants
filename = "model/tabular/Friday_labeled_training.csv"
target = "Label"

#%% Loading the data from directory
print("Loading training dataset...")
df = pd.read_csv(filename)
y = df[target].to_numpy()

#%% Counting the number of attacks in the source file
unique, counts = np.unique(y, return_counts=True)
dict(zip(unique, counts))

#%%
X = df.drop(columns=['flowStartMilliseconds','sourceIPAddress','destinationIPAddress','Label','Attack']).to_numpy()

X = np.nan_to_num(X)
y = np.nan_to_num(y)

#%% Classifier definition
from sklearn.ensemble import RandomForestClassifier
base_estimator = RandomForestClassifier(n_estimators=100, class_weight='balanced_subsample', verbose=0, n_jobs=-1, random_state=2021)
base_estimator.fit(X, y)

#%% Reading test data
df_test = pd.read_csv('model/tabular/Friday_labeled_test.csv')
y_true = df_test[target].to_numpy()

#%%
X_test = df_test.drop(columns=['flowStartMilliseconds','sourceIPAddress','destinationIPAddress','Label','Attack']).to_numpy()
X_test = np.nan_to_num(X)
y_true = np.nan_to_num(y)

#%% Create predictions
y_pred = base_estimator.predict(X_test)

#%%
from sklearn.metrics import classification_report, confusion_matrix
print("\n *************** X-VALIDATION ****************")
print("\n Confusion matrix:")
print(confusion_matrix(y_true=y_true, y_pred=y_pred))
print(classification_report(y_true=y_true, y_pred=y_pred))

#%%
from sklearn.metrics import average_precision_score, f1_score
print("Average precision (AP):", average_precision_score(y, y_pred))
print("F1:", f1_score(y, y_pred))