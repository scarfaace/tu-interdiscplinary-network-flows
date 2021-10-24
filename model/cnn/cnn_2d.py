#%%
import numpy as np
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from keras.layers import Input, Embedding, Activation, Flatten, Dense
from keras.layers import Conv1D, MaxPooling1D, Dropout
from keras.models import Model

#%%
df = pd.read_csv("./model/data/Friday_transcription_no-labels_labeled.tsv", sep='\t', quoting=3)

#%%
from sklearn.model_selection import train_test_split
train, test = train_test_split(df[['transcription', 'Label']], train_size=0.8, random_state=123)

train_texts = train['transcription'].values
train_label = train['Label'].values

test_texts = test['transcription'].values
test_label = test['Label'].values

#%%
tk = Tokenizer(num_words=None, char_level=True, oov_token='UNK', lower=False)
tk.fit_on_texts(train_texts)

# %%
def create_alphabet(dataframe):
    category_lines = {1: [], 0: []}
    all_categories = [0, 1]
    alphabet = set()

    for index, row in dataframe.iterrows():
        ascii_transcription = row['transcription']
        tokenized_transcription = [char for char in ascii_transcription]
        for token in tokenized_transcription:
            alphabet.add(token)

        category_lines[row['Label']].append(ascii_transcription)

    N_LETTERS = len(alphabet)
    ALL_LETTERS = ''.join(alphabet)
    return N_LETTERS, ALL_LETTERS

#%%
N_LETTERS, ALL_LETTERS = create_alphabet(df)
char_dict = {}
for i, char in enumerate(ALL_LETTERS):
    char_dict[char] = i + 1

#%%
tk.word_index = char_dict.copy()
# Add 'UNK' to the vocabulary
tk.word_index[tk.oov_token] = max(char_dict.values()) + 1

#%%
train_sequences = tk.texts_to_sequences(train_texts)
test_texts = tk.texts_to_sequences(test_texts)

# Padding
train_data = pad_sequences(train_sequences, maxlen=1014, padding='post')
test_data = pad_sequences(test_texts, maxlen=1014, padding='post')

#%%
from sklearn.preprocessing import LabelBinarizer
import keras
# Transform labels to one-hot
lb = LabelBinarizer()
Y = lb.fit_transform(train_label)
Y_test = lb.fit_transform(test_label)
Cat_y=keras.utils.to_categorical(Y,num_classes=2)
Y_test_cat = keras.utils.to_categorical(Y_test,num_classes=2)


#%%
import tensorflow as tf
X_train = tf.expand_dims(train_texts, axis=-1)
X_test = tf.expand_dims(test_texts, axis=-1)

#%%
from keras.layers import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.layers.core import Activation

# create the model
model = Sequential()
model.add(Conv2D(16,kernel_size = (1,1),input_shape=(96,26,1)))
model.add(Activation("relu"))
model.add(Conv2D(32,kernel_size = (1,1),input_shape=(96,26,1)))
model.add(Activation("relu"))

model.add(MaxPooling2D(pool_size=(2, 2),strides=2, padding='same', data_format=None))
model.add(Dropout(0.2))

model.add(Conv2D(64,kernel_size = (2,2),input_shape=(96,26,1)))
model.add(Activation("relu"))
model.add(Conv2D(82,kernel_size = (2,2),input_shape=(96,26,1)))
model.add(Activation("relu"))



model.add(Flatten())
model.add(Dense(64, activation='relu'))

model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
X_train, X_test, y_train, y_test = train_test_split(X_train, Cat_y, test_size=.8)
model.fit(X_train, y_train, validation_data=(X_test, Y_test_cat), epochs=30, batch_size=1)