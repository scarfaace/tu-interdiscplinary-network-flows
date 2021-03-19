import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from keras.optimizers import SGD
import tensorflow as tf
import numpy as np

def get_dataframe():
    df = pd.read_csv("model/data/Wednesday_transcription_sampled_5percent.csv", sep='\t').sample(frac=0.1, random_state=123)
    return df

def load_dataset(df):
    train, test = train_test_split(df[['transcription', 'label']], train_size=0.7, random_state=123)

    train_texts = train['transcription'].values
    train_label = train['label'].values

    validation_texts = test['transcription'].values
    validation_label = test['label'].values

    return train_texts, train_label, validation_texts, validation_label


def create_alphabet(dataframe):
    category_lines = {1: [], 0: []}
    all_categories = [0, 1]
    alphabet = set()

    for index, row in dataframe.iterrows():
        ascii_transcription = row['transcription']
        tokenized_transcription = [char for char in ascii_transcription]
        for token in tokenized_transcription:
            alphabet.add(token)

        category_lines[row['label']].append(ascii_transcription)

    N_LETTERS = len(alphabet)
    ALL_LETTERS = ''.join(alphabet)
    return N_LETTERS, ALL_LETTERS


def sequence_to_embeddings(tokenizer, train_texts, validation_texts):
    sequences = tokenizer.texts_to_sequences(train_texts)
    validation_sequences = tokenizer.texts_to_sequences(validation_texts)
    # print(train_texts[0])
    # print(sequences[0])
    data = pad_sequences(sequences, maxlen=750, padding='post')
    validation_data = pad_sequences(validation_sequences, maxlen=750, padding='post')
    return data, validation_data


def define_model(input_dimension, learning_rate):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(
            input_dim=input_dimension,
            output_dim=100),
        tf.keras.layers.LSTM(100, dropout=0.2, recurrent_dropout=0.2),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(250, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # %%
    # model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
    #               optimizer=tf.keras.optimizers.Adam(1),
    #               metrics=['}accuracy'])

    # opt = SGD(lr=learning_rate)
    model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(learning_rate), metrics=['accuracy'])

    return model


def remove_float_instances(texts):
    tmp_train_texts = []
    for w in texts:
        if type(w) is str:
            tmp_train_texts.append(w)
    train_texts = np.asarray(tmp_train_texts)
    return train_texts

