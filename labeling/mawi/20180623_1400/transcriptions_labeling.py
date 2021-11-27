import argparse

import pandas as pd


def get_dataframes(transcription_no_label_path: str, attacks_path: str) -> (pd.DataFrame, pd.DataFrame):
    df = pd.read_csv(transcription_no_label_path, sep="\t", quoting=3)
    label_df = pd.read_csv(attacks_path, sep=',')  # "./src/mawi/dataset_utils/20180623_anomalous_suspicious.csv"
    label_df["Label"] = 1

    return df, label_df


def merge_attacks_and_non_labeled(df: pd.DataFrame, label_df: pd.DataFrame) -> pd.DataFrame:
    attacks_df = pd.merge(df, label_df, how='inner', left_on=['sourceIPAddress', 'destinationIPAddress'],
                          right_on=['sourceIPAddress', 'destinationIPAddress'])
    return attacks_df


def filter_labeled(df: pd.DataFrame, attacks_df: pd.DataFrame) -> pd.DataFrame:
    df_no_duplicates = pd.concat([df, attacks_df]).drop_duplicates(['sourceIPAddress', 'destinationIPAddress'],
                                                                   keep=False)
    df_no_duplicates = df_no_duplicates[['sourceIPAddress', 'destinationIPAddress', 'transcription', 'Label']]
    return df_no_duplicates


def transcription_postprocessing(transcription: pd.DataFrame) -> pd.DataFrame:
    return transcription.reset_index(drop=True) \
        .fillna(0) \
        .astype({'Label': 'int32'}) \
        # .drop(columns='Unnamed: 0', inplace=True)


def sample_and_save(transcription_postprocessed: pd.DataFrame, sampled_labeled_output_path: str):
    df_attacks = transcription_postprocessed[transcription_postprocessed.Label == 1]
    df_non_attack = transcription_postprocessed[transcription_postprocessed.Label == 0]
    df_non_attack_sampled = df_non_attack.sample(n=300000, random_state=123)
    df = pd.concat([df_attacks, df_non_attack_sampled])

    df.to_csv(sampled_labeled_output_path, sep='\t', index=False, quoting=3)


def get_args():
    """
    Utility method to extract command line arguments used for parametrizing the labeling.
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--transcription_no_label_path', help='Path to the non labeled transcription dataset.')
    parser.add_argument('--attacks_input_path', help='Path to a CSV file containing attacks labeled by MAWI.')
    parser.add_argument('--output_labeled_transcription', help='Desired output path for labeled MAWI transcription dataset.')
    args = parser.parse_args()
    args_dict = vars(args)
    if None in args_dict.values():
        raise Exception("Command line argument missing, please check the documentation.")

    return args_dict['transcription_no_label_path'], args_dict['attacks_input_path'], args_dict['output_labeled_transcription']


transcription_no_label_path, attacks_input_path, output_labeled_transcription = get_args()

df, label_df = get_dataframes(transcription_no_label_path=transcription_no_label_path, attacks_path=attacks_input_path)
attacks_df = merge_attacks_and_non_labeled(df=df, label_df=label_df)

df_no_duplicates = filter_labeled(df=df, attacks_df=attacks_df)

attacks_df = attacks_df[['sourceIPAddress', 'destinationIPAddress', 'transcription', 'Label']]
transcription = pd.concat([df_no_duplicates, attacks_df], ignore_index=True)

transcription_postprocessed = transcription_postprocessing(transcription=transcription)

sample_and_save(transcription_postprocessed=transcription_postprocessed, sampled_labeled_output_path=output_labeled_transcription)
