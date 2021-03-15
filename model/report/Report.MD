

# First approach
Allan generated data from CAIA dataset. I preprocessed the data with encoding the sequence characters into integers by 
ASCII standard (this preserved the semantics of the characters). 

Then, a simple LSTM model was applied (https://machinelearningmastery.com/sequence-classification-lstm-recurrent-neural-networks-python-keras/) without dropout. 

This was not predicting the attacks at all (only 0.1% of the training samples were attacks).

Visualizations showed that attacks don't have any common pattern. 

# 29.12.2020
We focused on creating packet length distribution in order to see the difference in attacks vs non-attacks.
I need to try PyTorch since TF is bugged.


# Questions
- Do you think that stratifying the data based on "label" (attack, non-attack) is a good idea? By stratifying in this case I mean that 50% of the training data would be attacks, other 50% not. Utilising this technique would heavily decrease the number of training samples of course. 

- I encoded the sequence with only transforming each character into integer by the ASCII standard (meaning I took ord() function of each char). We discussed this with Allan and we think that this preserves the semantics of the data he is generating. Would you maybe use another approach?

- Since every sequence has different length, we need to pad it. I plotted the sequences of attacks as if it was a time-series dataset and I saw that only the first 1500 characters in the sequence were "important". Is there any evidence that claims only the first/last N minutes of the communication between parties is the most important in determining whether a communication is an attack? Or what value would you pick for padding the sequence?

# Email
We have an assumption that packet length is "clearly determinant for capturing malicious activity" based on the paper Analysis of Lightweight Feature Vectors for Attack Detection in Network Traffic.
Is there a paper/or any other source which elaborates on this? In particular we mean packet length distribution for malicious activities.



# ToDo

- Make a smaller dataset with at least 10% attack samples. 

- Add Dropout to the model

- Try different settings in LSTM


## 7.3.2021
Tried different settings of network architecture + learning rates


Network: tf.keras.layers.Embedding(
            input_dim=input_dimension,
            output_dim=64),
        tf.keras.layers.LSTM(64, dropout=0.2,
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10),
        tf.keras.layers.Dense(1, activation='sigmoid')
Optimizer - SGD with categorical_crossentropy
1.
Learning rate: 9.28578571e-02
CF: [[24  2]
     [20  0]], shape=(2, 2), dtype=int32)
2.
Learning rate: 7.85735714e-02
CF: [[ 4 22]
     [ 3 17]], shape=(2, 2), dtype=int32)

----------------------------------------------------------

## 13.3.2021 
Running preprocessing on top of new schema (with bi-directional data) and debugging why 
kernel is still dropping. The reason is that more neurons take more memory -> kernel drops. (https://stackoverflow.com/questions/60349021/anaconda-jupyter-the-kernel-appears-to-have-died-it-will-restart-automatically)

## 14.3.2021
Trying to find network and dataset size such that it fits to memory and kernel doesn't die.

Network: tf.keras.Sequential([
        tf.keras.layers.Embedding(
            input_dim=input_dimension,
            output_dim=64),
        tf.keras.layers.LSTM(64),
        tf.keras.layers.Dense(64, activation='sigmoid'),
        tf.keras.layers.Dense(1, activation='softmax')
    ])
Optimizer - Adam with categorical_crossentropy
Learning rates - [1, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001]
CF: for each it was the same:
[[   0 1129]
 [   0   90]]

Network: tf.keras.Sequential([
        tf.keras.layers.Embedding(
            input_dim=input_dimension,
            output_dim=64),
        tf.keras.layers.LSTM(64),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='softmax')
    ])
Optimizer - Adam with categorical_crossentropy
Learning rates - [1, 0.1, 0.01, 0.001, 0.0001, 0.00001] 
CF: for each it was the same:
[[1129    0]
 [  90    0]]

Learning rate - 0.000001
[[   0 1129]
 [   0   90]]

Network: tf.keras.Sequential([
        tf.keras.layers.Embedding(
            input_dim=input_dimension,
            output_dim=64),
        tf.keras.layers.LSTM(64),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

Optimizer - Adam with categorical_crossentropy
Learning rates - [[1.00000000e-05, 9.35714286e-06, 8.71428571e-06, 8.07142857e-06,
       7.42857143e-06, 6.78571429e-06, 6.14285714e-06, 5.50000000e-06,
       4.85714286e-06, 4.21428571e-06, 3.57142857e-06, 2.28571429e-06, 1.64285714e-06]
CF:
[[1129    0]
 [  90    0]]

Learning rate - 2.92857143e-06
CF: 
[[1126    3]
 [  89    1]]

### Started using random seed - tf.random.set_seed(123) 
Learning rate - 1.00000000e-06
CF:
[[616 513]
 [ 39  51]]

Learning rate - [1.00000000e-04, 9.47894737e-05, 8.95789474e-05, 8.43684211e-05,
       7.91578947e-05, 7.39473684e-05, 6.87368421e-05, 6.35263158e-05,
       5.83157895e-05, 5.31052632e-05, 4.78947368e-05, 4.26842105e-05,
       3.74736842e-05, 3.22631579e-05, 2.70526316e-05, 2.18421053e-05,
       1.66315789e-05, 1.14210526e-05, 6.21052632e-06
CF:
[[1129    0]
 [  90    0]]

Learning rate -  1.00000000e-06
CF: 
[[187 942]
 [ 15  75]]

Learning rate - 0.000001
CF:
[[1082   47]
 [  87    3]]

Learning rate - 7.75e-07
CF:
[[689 440]
 [ 48  42]]

Learning rate - 5.50e-07
CF:
[[1122    7]
 [  90    0]]

Learning rate - 3.25e-07
CF:
[[   0 1129]
 [   0   90]]

Learning rate - 1.00e-07
CF:
[[996 133]
 [ 86   4]]


Learning rate - 9.47894737e-07
CF:
[[1090   39]
 [  88    2]]

Learning rate - 8.43684211e-07
CF:
[[407 722]
 [ 29  61]]

Learning rate - 7.39473684e-07
CF:
[752 377]
 [ 67  23]]

Learning rate - 6.87368421e-07
CF:
[[462 667]
 [ 38  52]]

Learning rate - 4.26842105e-07
CF:
[[804 325]
 [ 58  32]]

Learning rate - 3.22631579e-07
CF:
[[164 965]
 [ 15  75]]

Learning rate - 2.70526316e-07
CF:
[[658 471]
 [ 63  27]]

Learning rate - 2.18421053e-07
CF:
[[247 882]
 [ 15  75]]

Learning rate - 1.66315789e-07
CF:
[[604 525]
 [ 37  53]]

Learning rate - 1.14210526e-07
CF:
[[968 161]
 [ 72  18]]

Learning rate - 6.21052632e-08
CF:
[[316 813]
 [ 20  70]]

Learning rate - 1.00000000e-08
CF:
[[   5 1124]
 [   0   90]]

Learning rate - 1.00000000e-06
CF:
[[1129    0]
 [  90    0]]


Change to binary_crossentropy

