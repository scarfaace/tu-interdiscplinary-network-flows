#%%
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
np.random.seed(7)
from sklearn.model_selection import train_test_split
import tensorflow as tf

#%% Load the dataset
df = pd.read_csv("model/data/transcription_Tuesday.csv", sep=',')

#%% Split the dataset into train/test
train, test = train_test_split(df[['transcription', 'label']], train_size=0.7, random_state=123)

#%% Create raw X matrices
X_train_raw = train['transcription']
X_test_raw = test['transcription']

#%%
Y_train = train['label']
Y_test = test['label']

#%%
X_train = []
for input_sequence in X_train_raw:
    onehot = tf.keras.preprocessing.text.one_hot(input_sequence, 547)
    X_train.append(onehot)

X_test = []
for input_sequence in X_test_raw:
    onehot = tf.keras.preprocessing.text.one_hot(input_sequence, 547)
    X_test.append(onehot)

#%%
X_padded = sequence.pad_sequences(X_train, maxlen=750, dtype='object', value=0, padding='post')
X_test_padded = sequence.pad_sequences(X_test, maxlen=750, dtype='object', value=0, padding='post')


#%%
X_padded = np.asarray(X_padded).astype('float32')
Y_train = np.asarray(Y_train).astype('float32')

#%%
X_test_padded = np.asarray(X_test_padded).astype('float32')
Y_test = np.asarray(Y_test).astype('float32')

#%%
emb_vecor_length = 547
modelClass = Sequential()
modelClass.add(Embedding(547, emb_vecor_length, input_length=750))
modelClass.add(LSTM(100))
modelClass.add(Dense(1, activation='sigmoid'))
modelClass.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(modelClass.summary())
#%% Train
modelClass.fit(X_padded, Y_train, epochs=3, batch_size=64)

#%% Predict
scores = modelClass.evaluate(X_test_padded, Y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))


# Helper commands below
#%%
X_train = sequence.pad_sequences(X_train_raw, maxlen=100, dtype='object')
X_train = np.where(X_train=='-', 'z', X_train)
X_test = sequence.pad_sequences(X_test_raw, maxlen=100, dtype='object')
#X_train = np.where(X_train=='-', 'z', X_train)
VOCAB_SIZE=1000
encoder = tf.keras.layers.preprocessing.TextVectorization(
    max_tokens=VOCAB_SIZE)
encoder.adapt(X_train)

# #%% Cast
# df['attack'] = df['attack'].replace('Normal', 0)
# df['attack'] = df['attack'].replace('Infiltration:Dropbox download - (Portscan + Nmap) from victim', 1)
# df['attack'] = df['attack'].replace('DDoS:LOIT', 1)

#%% Tokenize the sequence into array
df['transcription'] = np.array([list(x) for x in df['transcription']])

#%% Determine the length of the shortest flow
shortest_flow_length = df.transcription.map(lambda x: len(x)).min()
