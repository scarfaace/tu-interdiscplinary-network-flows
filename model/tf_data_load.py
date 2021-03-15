#%%
from sklearn.utils import class_weight
from tensorflow.python.keras.preprocessing.text import Tokenizer
import tensorflow as tf
import numpy as np

#%%
import model.tf_helper as helper

#%%
def perform_experiment(learning_rate):
    df = helper.get_dataframe()
    train_texts, train_label, validation_texts, validation_label = helper.load_dataset(df)

    tokenizer = Tokenizer(num_words=None, char_level=True, oov_token='UNK')
    tokenizer.fit_on_texts(train_texts)
    N_LETTERS, ALL_LETTERS = helper.create_alphabet(df)

    char_dict = {}
    for i, char in enumerate(ALL_LETTERS):
        char_dict[char] = i + 1

    tokenizer.word_index = char_dict
    tokenizer.word_index[tokenizer.oov_token] = max(char_dict.values()) + 1
    data, validation_data = helper.sequence_to_embeddings(tokenizer=tokenizer, train_texts=train_texts,
                                                          validation_texts=validation_texts)
    # validation_tuple = (validation_data, validation_label)

    input_dimension = len(char_dict.values())
    model = helper.define_model(input_dimension=input_dimension, learning_rate=learning_rate)
    class_weights = dict(zip(np.unique(train_label), class_weight.compute_class_weight('balanced', np.unique(train_label), train_label)))
    model.fit(x=data, y=train_label, epochs=3, class_weight=class_weights)
    test_loss, test_acc = model.evaluate(x=validation_data, y=validation_label)
    print(test_acc)
    predictions = model.predict_classes(x=validation_data)
    confusion = tf.math.confusion_matrix(labels=validation_label, predictions=predictions, num_classes=2)
    print(confusion)

#%%
# learning_rates = np.linspace()
# for learning_rate in learning_rates:
perform_experiment(learning_rate=0.0001)



#%%
import pandas as pd
df = pd.read_csv("model/data/Wednesday_transcription_sampled_10percent.csv", sep='\t')


#%%
train_texts, train_label, validation_texts, validation_label = helper.load_dataset(df)

#%%
tokenizer = Tokenizer(num_words=None, char_level=True, oov_token='UNK', lower=False)
tokenizer.fit_on_texts(train_texts)

# #%%
# print(tokenizer.oov_token)
# print(tokenizer.word_index)

#%% Create alphabet
N_LETTERS, ALL_LETTERS = helper.create_alphabet(df)

#%%
char_dict = {}
for i, char in enumerate(ALL_LETTERS):
    char_dict[char] = i + 1
print(char_dict)

#%%
tokenizer.word_index = char_dict
tokenizer.word_index[tokenizer.oov_token] = max(char_dict.values()) + 1

#%%
data, validation_data = helper.sequence_to_embeddings(tokenizer=tokenizer, train_texts=train_texts,
                                           validation_texts=validation_texts)
# sequences = tokenizer.texts_to_sequences(train_texts)
# validation_sequences = tokenizer.texts_to_sequences(validation_texts)
# # print(train_texts[0])
# # print(sequences[0])
#
# #%%
# data = pad_sequences(sequences, maxlen=750, padding='post')
# validation_data = pad_sequences(validation_sequences, maxlen=750, padding='post')

#%%
validation_tuple = (validation_data, validation_label)

#%% Get input dimension into embedding
input_dimension = len(char_dict.values())

#%%
model = helper.define_model(input_dimension=input_dimension)

#%%
history = model.fit(x=data, y=train_label, epochs=20, validation_data=validation_tuple)

#%%
test_loss, test_acc = model.evaluate(x=validation_data, y=validation_label)

#%%
predictions = model.predict(x=validation_data)
confusion = tf.math.confusion_matrix(labels=validation_label, predictions=predictions, num_classes=2)
print(confusion)