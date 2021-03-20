#%%
import pandas
import matplotlib.pyplot as plt
import numpy as np
import statistics
import seaborn as sns

#%%
attacksDf = pandas.read_csv("transcription/data_analysis/Wednesday_attacks_lengths.csv", sep='\t')
featuresDf = pandas.read_csv("transcription/data_analysis/Wednesday_features_lengths.csv", sep=',')
transcriptionsDf = pandas.read_csv("transcription/data_analysis/Wednesday_transcription_lengths.csv", sep='\t')

#%%
attacksLengths = attacksDf.transcription
featuresLengths = featuresDf.ipTotalLength
transcriptionsLengths = transcriptionsDf.transcription

#%%
# CDF for transcription lengths for Wednesday attacks, all Wednesday transcriptions
attacksLengths.hist(cumulative=True, density=1, bins=100)
plt.show()
transcriptionsLengths.hist(cumulative=True, density=1, bins=100)
plt.show()
# CDF for packet lengths of Wednesday communications
featuresLengths.hist(cumulative=True, density=1, bins=100)
plt.show()

#%%
ipPacketLengthsUniqueSorted = np.sort(featuresLengths.unique())
print('min:', min(ipPacketLengthsUniqueSorted))
print('max:', max(ipPacketLengthsUniqueSorted))
print('median:', statistics.median(ipPacketLengthsUniqueSorted))

#%%
sns.boxplot(x=attacksLengths)
plt.show()
sns.boxplot(x=featuresLengths)
plt.show()
sns.boxplot(x=transcriptionsLengths)
plt.show()

#%%
# attacksLengths.plot.kde()
# plt.show()
# transcriptionsLengths.plot.kde()
# plt.show()
# featuresLengths.plot.kde()
