import pandas as pd

#%%
transcription_df = pd.read_csv("./experiments/01/transcription/MAWI/out/MAWI/201806231400_transcription.tsv", sep="\t", quoting=3, quotechar="")
label_df = pd.read_csv("./resources/MAWI/20180623_anomalous_suspicious.csv", sep=',')

#%%
label_df["label"] = 1
transcription_df['label'] = 0

#%%
attacks_df = pd.merge(transcription_df, label_df,  how='inner', left_on=['sourceIPAddress', 'destinationIPAddress'], right_on = ['sourceIPAddress', 'destinationIPAddress'])

#%%
attacks_df_to_write = attacks_df[['sourceIPAddress', 'destinationIPAddress', 'transcription', 'label']]

#%%
attacks_df_to_write.to_csv("./model/mawi/attacks.csv")

#%%
transcription_df_to_write = transcription_df[['sourceIPAddress', 'destinationIPAddress', 'transcription', 'label']]

#%%
appended = transcription_df_to_write.append(attacks_df_to_write)

#%%
appended.drop_duplicates(subset=['sourceIPAddress', 'destinationIPAddress'], inplace=True, keep='last')

#%%
filtered_df = appended[appended['transcription'].map(len) > 2]

#%%
filtered_df.to_csv("./model/mawi/full_dataset.csv")


#%%
transcription_df = pd.read_csv("./model/mawi/full_dataset.csv")[['sourceIPAddress', 'destinationIPAddress', 'transcription', 'label']]