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
train_data = np.array(train_data, dtype='float32')
test_data = np.array(test_data, dtype='float32')

#%%
from keras.utils import to_categorical
train_classes = to_categorical(train_label)
test_classes = to_categorical(test_label)

#%%
# parameter
input_size = 1014
vocab_size = len(tk.word_index)
embedding_size = 53
conv_layers = [[256, 7, 3],
               [256, 7, 3],
               [256, 3, -1],
               [256, 3, -1],
               [256, 3, -1],
               [256, 3, 3]]

fully_connected_layers = [1024, 1024]
num_of_classes = 2
dropout_p = 0.5
optimizer = 'adam'
loss = 'categorical_crossentropy'

#%%
embedding_weights = []  # (70, 69)
embedding_weights.append(np.zeros(vocab_size))  # (0, 69)

for char, i in tk.word_index.items():  # from index 1 to 69
    onehot = np.zeros(vocab_size)
    onehot[i - 1] = 1
    embedding_weights.append(onehot)

embedding_weights = np.array(embedding_weights)
print('Load')

#%%
embedding_layer = Embedding(vocab_size + 1,
                            embedding_size,
                            input_length=input_size,
                            weights=[embedding_weights])

#%%
inputs = Input(shape=(input_size,), name='input', dtype='int64')  # shape=(?, 1014)
# Embedding
x = embedding_layer(inputs)

#%%
for filter_num, filter_size, pooling_size in conv_layers:
    x = Conv1D(filter_num, filter_size)(x)
    x = Activation('relu')(x)
    if pooling_size != -1:
        x = MaxPooling1D(pool_size=pooling_size)(x)  # Final shape=(None, 34, 256)
x = Flatten()(x)  # (None, 8704)

#%%
for dense_size in fully_connected_layers:
    x = Dense(dense_size, activation='relu')(x)  # dense_size == 1024
    x = Dropout(dropout_p)(x)

#%%
predictions = Dense(num_of_classes, activation='softmax')(x)

#%%
model = Model(inputs=inputs, outputs=predictions)
model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])  # Adam, categorical_crossentropy
model.summary()

#%%
indices = np.arange(train_data.shape[0])
np.random.shuffle(indices)

#%%
x_train = train_data[indices]
y_train = train_classes[indices]

x_test = test_data
y_test = test_classes

#%%
model.fit(x_train, y_train,
          validation_data=(x_test, y_test),
          batch_size=128,
          epochs=3,
          verbose=2)

#%%
