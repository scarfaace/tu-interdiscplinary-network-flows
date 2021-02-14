

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