#%%
import numpy as np
import pandas as pd
np.random.seed(7)

#%% Load the attack dataset
df = pd.read_csv("model/data/Wednesday_attacks.csv", sep='\t')
df_non_attack = pd.read_csv("model/data/wednesday_sampled_nonattacks.csv", sep='\t')
#%%
df_total = df.append(df_non_attack)
#%%
df_total = df_total.sample(frac=1)

#%%
df_total.to_csv("model/data/wednesday_all.csv", sep='\t', encoding='utf8')

#%% Filter the attacks and non-attacks to separate dataframes
df_ones = df[df.label == 1]
df_zeros = df[df.label == 0]
df_zeros_sampled = df_zeros.sample(n=2475, random_state=123)

#%%
df_appended = df_ones.append(df_zeros_sampled)

#%% Reshuffle the data
df_shuffled = df_appended.sample(frac=1)

#%% Save to CSV
df_shuffled.to_csv("model/data/tuesday_sampled.csv", sep=',', encoding='utf8')

#%% Load all "attacks" datasets
df_monday = pd.read_csv("model/data/Monday_attacks.csv", sep=',')
df_tuesday = pd.read_csv("model/data/Tuesday_attacks.csv", sep=',')
df_wednesday = pd.read_csv("model/data/Wednesday_attacks.csv", sep=',')
df_friday = pd.read_csv("model/data/Friday_attacks.csv", sep=',')

#%% Sample non-attacks
df = pd.read_csv("model/data/Wednesday_transcription.csv", sep='\t')
df_zeros = df[df.label == 0]
df_zeros_sampled = df_zeros.sample(n=100, random_state=123)
df_zeros_sampled.to_csv("model/data/wednesday_sampled_nonattacks.csv", sep='\t')

#%% Merge attacks and non-attacks
df_attacks = pd.read_csv("model/data/all_attacks.csv", sep=',')
df_nonattacks = pd.read_csv("model/data/sampled_nonattacks.csv", sep=',')
df_concat = df_attacks.append(df_nonattacks)

#%% Save sampled file
df_concat.to_csv("model/data/10percent_attacks.csv", sep=',')


#%%
from sklearn.preprocessing import normalize
df = pd.read_csv("model/data/10percent_attacks.csv", sep=',')
df['transcription'] = np.array([list(x) for x in df['transcription']])
df_ones = df[df.label == 1]
df_zeros = df[df.label == 0]

#%%
df_all = df_ones.append(df_zeros.sample(n=76, random_state=123))
df_all.to_csv("model/data/training_data.csv", sep=',')

#%%
df = pd.read_csv("model/data/training_data.csv", sep=',')