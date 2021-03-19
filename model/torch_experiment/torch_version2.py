#%%
import pandas as pd

#%% Load data
df = pd.read_csv("model/data/wednesday_all.csv", sep='\t')

#%% Create category_lines and alphabet
category_lines = {1: [], 0: []}
all_categories = [0, 1]
alphabet = set()

for index, row in df.iterrows():
    ascii_transcription = row['transcription']
    tokenized_transcription = [char for char in ascii_transcription]
    for token in tokenized_transcription:
        alphabet.add(token)

    category_lines[row['label']].append(ascii_transcription)

N_LETTERS = len(alphabet)
ALL_LETTERS = ''.join(alphabet)

#%%
import torch
# Find letter index from all_letters
def letter_to_index(letter):
    return ALL_LETTERS.find(letter)

# Just for demonstration, turn a letter into a <1 x n_letters> Tensor
def letter_to_tensor(letter):
    tensor = torch.zeros(1, N_LETTERS)
    tensor[0][letter_to_index(letter)] = 1
    return tensor

# Turn a line into a <line_length x 1 x n_letters>,
# or an array of one-hot letter vectors
def line_to_tensor(line):
    tensor = torch.zeros(len(line), 1, N_LETTERS)
    for i, letter in enumerate(line):
        tensor[i][0][letter_to_index(letter)] = 1
    return tensor

#%% Turn each row of DF into tensor
