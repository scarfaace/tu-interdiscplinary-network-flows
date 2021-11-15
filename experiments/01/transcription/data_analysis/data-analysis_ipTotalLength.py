#%%
import matplotlib.pyplot as plt
import pandas

#%%
Monday_ipTotalLength = pandas.read_csv("experiments/01/transcription/data_analysis/Monday_ipTotalLength.csv")
Tuesday_ipTotalLength = pandas.read_csv("experiments/01/transcription/data_analysis/Tuesday_ipTotalLength.csv")
Wednesday_ipTotalLength = pandas.read_csv("experiments/01/transcription/data_analysis/Wednesday_ipTotalLength.csv")
Thursday_ipTotalLength = pandas.read_csv("experiments/01/transcription/data_analysis/Thursday_ipTotalLength.csv")
Friday_ipTotalLength = pandas.read_csv("experiments/01/transcription/data_analysis/Friday_ipTotalLength.csv")

#%%
# CDF for packet lengths
def plot_packet_lengths_cdf(df, day_name):
    df.hist(cumulative=True, density=1, bins=100)
    plt.title('CDF for packet sizes for all {} transcriptions'.format(day_name))
    plt.xlabel('Packet Size (in bytes)')
    plt.ylabel('Probability')
    plt.show()

plot_packet_lengths_cdf(Monday_ipTotalLength, 'Monday')
plot_packet_lengths_cdf(Tuesday_ipTotalLength, 'Tuesday')
plot_packet_lengths_cdf(Wednesday_ipTotalLength, 'Wednesday')
plot_packet_lengths_cdf(Thursday_ipTotalLength, 'Thursday')
plot_packet_lengths_cdf(Friday_ipTotalLength, 'Friday')
