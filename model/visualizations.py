#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from keras.preprocessing import sequence


#%% Read the CSV file.
df = pd.read_csv("model/data/tuesday_sampled.csv", sep=',')

#%% Split the string into array of characters.
df['transcription'] = np.array([list(x) for x in df['transcription']])

#%% Show the values and count of them.
Counter(df['transcription'][10]).keys()
Counter(df['transcription'][10]).values()

#%% Sample only 5 rows
sampled = df['transcription'].sample(n=5, random_state=123)

#%% Cast each character to a integer - preserving it's semantics by using ascii casting.
sampled = sampled.apply(lambda x: [ord(i) for i in x])

#%% Print the whole sampled dataset.
for row in sampled:
    plt.plot(range(len(row)), row)
    plt.show()

#%% Filter only attacks
attacks = df[df.label == 1]
attacks_series = attacks['transcription']

#%%
attacks_series = attacks_series.apply(lambda x: [ord(i) for i in x])

#%% Mean length of sequence
attacks.transcription.str.len().mean()

#%% Plot all attacks
for row in sampled:
    i = 0
    plt.plot(range(len(row)), row, label="line " + str(i))
    i += 1

plt.show()

#%%
padded_seq = sequence.pad_sequences(attacks_series, maxlen=1500, dtype='object', padding='post', value=45)

#%%
for row in padded_seq:
    i = 0
    plt.plot(range(len(row)), row, label="line " + str(i))
    i += 1

plt.legend()
plt.show()