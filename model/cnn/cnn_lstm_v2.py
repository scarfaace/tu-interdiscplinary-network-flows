#%%
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from sklearn.utils import class_weight
from sklearn.metrics import f1_score
from tensorflow.python.keras.preprocessing.text import Tokenizer
import tensorflow as tf
import numpy as np
tf.random.set_seed(123)
np.random.seed(7)

#%%
def get_dataframe():
    # df1 = pd.read_csv("./data/Monday_transcription.tsv", sep='\t', quoting=3)
    # df2 = pd.read_csv("./data/Tuesday_transcription.tsv", sep='\t', quoting=3)
    # df3 = pd.read_csv("./data/Wednesday_transcription.tsv", sep='\t', quoting=3)
    # df4 = pd.read_csv("./data/Thursday_transcription.tsv", sep='\t', quoting=3)
    df5 = pd.read_csv("./model/data/Friday_transcription_no-labels_labeled.tsv", sep='\t', quoting=3)

    # dfs = [df1, df2, df3, df4, df5]
    dfs = [df5]
    df_temp = pd.concat(dfs)
    df_attacks = df_temp[df_temp.Label == 1]
    df_non_attack = df_temp[df_temp.Label == 0]
    df_non_attack_sampled = df_non_attack.sample(n=10000, random_state=123)
    df = pd.concat([df_attacks, df_non_attack_sampled])

    return df

#%%
def load_dataset(df):
    train, test = train_test_split(df[['transcription', 'Label']], train_size=0.8, random_state=123)

    train_texts = train['transcription'].values
    train_label = train['Label'].values

    validation_texts = test['transcription'].values
    validation_label = test['Label'].values

    return train_texts, train_label, validation_texts, validation_label

#%%
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
def sequence_to_embeddings(tokenizer, train_texts, validation_texts):
    sequences = tokenizer.texts_to_sequences(train_texts)
    validation_sequences = tokenizer.texts_to_sequences(validation_texts)
    data = pad_sequences(sequences, maxlen=375, padding='post')
    validation_data = pad_sequences(validation_sequences, maxlen=375, padding='post')
    return data, validation_data

#%%
def define_model(input_dimension, learning_rate):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(
            input_dim=input_dimension,
            output_dim=375),
        tf.keras.layers.Conv1D(filters=375, kernel_size=3, padding='same', activation='relu'),
        tf.keras.layers.MaxPooling1D(pool_size=2),
        tf.keras.layers.LSTM(64),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
        ])
    model.compile(loss="binary_crossentropy", optimizer=tf.keras.optimizers.Adam(learning_rate), metrics=['accuracy', tf.keras.metrics.TruePositives()])
    return model

#%%
df = get_dataframe()
train_texts, train_label, validation_texts, validation_label = load_dataset(df)
tokenizer = Tokenizer(num_words=None, char_level=True, oov_token='UNK', lower=False)
tokenizer.fit_on_texts(train_texts)

#%%
N_LETTERS, ALL_LETTERS = create_alphabet(df)
char_dict = {}
for i, char in enumerate(ALL_LETTERS):
    char_dict[char] = i + 1
print(char_dict)

#%%
tokenizer.word_index = char_dict
tokenizer.word_index[tokenizer.oov_token] = max(char_dict.values()) + 1

#%%
data, validation_data = sequence_to_embeddings(tokenizer=tokenizer, train_texts=train_texts,
                                           validation_texts=validation_texts)

#%%
learning_rates = [0.01, 0.001, 0.0001, 0.00001, 0.000001]  # np.linspace(0.001, 0.00000001, 20) #[1, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]
accuracies = []
confusion_matrices = []
tf.random.set_seed(123)
np.random.seed(123)

for learning_rate in learning_rates:
    input_dimension = len(char_dict.values())
    model = define_model(input_dimension=input_dimension, learning_rate=learning_rate)
    class_weights = dict(
        zip(np.unique(train_label), class_weight.compute_class_weight('balanced', np.unique(train_label), train_label)))
    print('Weight for class 0: {:.2f}'.format(class_weights[0]))
    print('Weight for class 1: {:.2f}'.format(class_weights[1]))

    history = model.fit(x=data, y=train_label, epochs=3, class_weight=class_weights)

    test_loss, test_acc, test_tp = model.evaluate(x=validation_data, y=validation_label)

    predictions = model.predict_classes(x=validation_data)
    confusion = tf.math.confusion_matrix(labels=validation_label, predictions=predictions, num_classes=2)
    print(learning_rate)
    print(confusion)

    accuracies.append(test_acc)
    confusion_matrices.append(confusion)