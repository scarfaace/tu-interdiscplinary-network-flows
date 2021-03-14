#%%
import pandas
import matplotlib.pyplot as plt
import numpy as np
import statistics
import seaborn as sns

#%%
transcriptionsDf = pandas.read_csv("transcription/out/Wednesday_transcription_cut.csv", sep='\t')

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
