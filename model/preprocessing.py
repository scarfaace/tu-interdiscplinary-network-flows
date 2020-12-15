#%%
import numpy as np
import pandas as pd
np.random.seed(7)

#%% Load the dataset
df = pd.read_csv("model/data/Tuesday_transcription.csv", sep=',')

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