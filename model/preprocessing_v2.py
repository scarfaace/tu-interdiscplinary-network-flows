#%%
from sklearn.utils import class_weight
from tensorflow.python.keras.preprocessing.text import Tokenizer
import tensorflow as tf
import numpy as np

#%%
import model.tf_helper as helper

#%%
import pandas as pd
df = pd.read_csv("model/data/Wednesday_transcription_sampled.csv", sep='\t')

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

#%%
input_dimension = len(char_dict.values())
#%%
model = helper.define_model(input_dimension=input_dimension, learning_rate=0.0001)
#%%
class_weights = dict(zip(np.unique(train_label), class_weight.compute_class_weight('balanced', np.unique(train_label), train_label)))
#%%
model.fit(x=data, y=train_label, epochs=3, class_weight=class_weights)
#%%
test_loss, test_acc = model.evaluate(x=validation_data, y=validation_label)

#%%
predictions = model.predict_classes(x=validation_data)
confusion = tf.math.confusion_matrix(labels=validation_label, predictions=predictions, num_classes=2)
print(confusion)