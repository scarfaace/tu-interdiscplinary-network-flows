#%%
import pandas
import matplotlib.pyplot as plt

#%%
attacksDf = pandas.read_csv("transcription/out/Wednesday_attacks_lengths.csv", sep='\t')
featuresDf = pandas.read_csv("transcription/out/Wednesday_features_lengths.csv", sep=',')
transcriptionsDf = pandas.read_csv("transcription/out/Wednesday_transcription_lengths.csv", sep='\t')

#%%
attacksLengths = attacksDf.transcription
featuresLengths = featuresDf.ipTotalLength
transcriptionsLengths = transcriptionsDf.transcription

#%%
attacksLengths.hist(cumulative=True, density=1, bins=100)
plt.show()
transcriptionsLengths.hist(cumulative=True, density=1, bins=100)
plt.show()
featuresLengths.hist(cumulative=True, density=1, bins=100)
plt.show()

#%%
# attacksLengths.plot.kde()
# plt.show()
# transcriptionsLengths.plot.kde()
# plt.show()
# featuresLengths.plot.kde()
