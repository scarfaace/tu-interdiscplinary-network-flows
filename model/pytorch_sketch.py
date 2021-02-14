#%%
import pandas as pd
import unicodedata

import random

#%% Load data
df = pd.read_csv("model/data/wednesday_all.csv", sep='\t')

#%% Create list of chars from transcription
# tokenized_transcription = np.array([list(x) for x in df['transcription']])

#%%
def unicode_to_ascii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

#%% Set of all characters in the sequences
# alphabet = set()
# for transcription in tokenized_transcription:
#     for letter in transcription:
#         alphabet.add(letter)
# N_LETTERS = len(alphabet)
# ALL_LETTERS = str(alphabet)

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

#%%
def random_training_example(category_lines, all_categories):
    def random_choice(a):
        random_idx = random.randint(0, len(a) - 1)
        return a[random_idx]

    category = random_choice(all_categories)
    line = random_choice(category_lines[category])
    category_tensor = torch.tensor([all_categories.index(category)], dtype=torch.long)
    line_tensor = line_to_tensor(line)
    return category, line, category_tensor, line_tensor

#%%
import torch
import torch.nn as nn

class RNN(nn.Module):
    # implement RNN from scratch rather than using nn.RNN
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size
        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input_tensor, hidden_tensor):
        combined = torch.cat((input_tensor, hidden_tensor), 1)

        hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def init_hidden(self):
        return torch.zeros(1, self.hidden_size)

#%%
n_categories = 2
n_hidden = 128
rnn = RNN(N_LETTERS, n_hidden, n_categories)

#%%
input_tensor = letter_to_tensor('@')
hidden_tensor = rnn.init_hidden()

output, next_hidden = rnn(input_tensor, hidden_tensor)

#%%
input_tensor = line_to_tensor('BaAaaBaaBaAa--------------aCaaAaaaAAAa')
hidden_tensor = rnn.init_hidden()

output, next_hidden = rnn(input_tensor[0], hidden_tensor)

#%%
def category_from_output(output):
    category_idx = torch.argmax(output).item()
    return all_categories[category_idx]

print(category_from_output(output))

#%%
criterion = nn.NLLLoss()
learning_rate = 0.005
optimizer = torch.optim.SGD(rnn.parameters(), lr=learning_rate)

#%%
def train(line_tensor, category_tensor):
    hidden = rnn.init_hidden()

    for i in range(line_tensor.size()[0]):
        output, hidden = rnn(line_tensor[i], hidden)

    loss = criterion(output, category_tensor)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return output, loss.item()

#%%
import matplotlib.pyplot as plt
current_loss = 0
all_losses = []
plot_steps, print_steps = 1, 2
n_iters = 3
for i in range(n_iters):
    category, line, category_tensor, line_tensor = random_training_example(category_lines, all_categories)

    output, loss = train(line_tensor, category_tensor)
    current_loss += loss

    # if (i + 1) % plot_steps == 0:
    #     current_loss = 0
    all_losses.append(current_loss / plot_steps)

    guess = category_from_output(output)
    correct = "CORRECT" if guess == category else f"WRONG ({category})"
    print(f"{i + 1} {(i + 1) / n_iters * 100} {loss:.4f} / {guess} {correct} {line}")
    # if (i + 1) % print_steps == 0:
    #     pass

plt.figure()
plt.plot(all_losses)
plt.show()