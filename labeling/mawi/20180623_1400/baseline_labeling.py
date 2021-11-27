import argparse

import pandas as pd

columns_to_select = ['sourceIPAddress', 'destinationIPAddress',
                     "apply(min(ipTotalLength),forward)", "apply(max(ipTotalLength),forward)",
                     "apply(median(ipTotalLength),forward)", "apply(mean(ipTotalLength),forward)",
                     "apply(mode(ipTotalLength),forward)", "apply(stdev(ipTotalLength),forward)",
                     "apply(min(_interPacketTimeSeconds),forward)", "apply(max(_interPacketTimeSeconds),forward)",
                     "apply(median(_interPacketTimeSeconds),forward)", "apply(mean(_interPacketTimeSeconds),forward)",
                     "apply(stdev(_interPacketTimeSeconds),forward)", "apply(min(ipTotalLength),backward)",
                     "apply(max(ipTotalLength),backward)", "apply(median(ipTotalLength),backward)",
                     "apply(mean(ipTotalLength),backward)", "apply(mode(ipTotalLength),backward)",
                     "apply(stdev(ipTotalLength),backward)", "apply(min(_interPacketTimeSeconds),backward)",
                     "apply(max(_interPacketTimeSeconds),backward)", "apply(median(_interPacketTimeSeconds),backward)",
                     "apply(mean(_interPacketTimeSeconds),backward)","apply(stdev(_interPacketTimeSeconds),backward)",
                     'min(_interPacketTimeSeconds)', 'max(_interPacketTimeSeconds)',
                     'median(_interPacketTimeSeconds)', 'mean(_interPacketTimeSeconds)', 'stdev(_interPacketTimeSeconds)', 'Label']


def get_dataframes(baseline_no_label_path: str, attacks_path: str) -> (pd.DataFrame, pd.DataFrame):
    df = pd.read_csv(baseline_no_label_path, sep=",")
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
    df_no_duplicates = df_no_duplicates[columns_to_select]
    return df_no_duplicates


def baseline_postprocessing(baseline: pd.DataFrame) -> pd.DataFrame:
    return baseline.reset_index(drop=True) \
        .fillna(0) \
        .astype({'Label': 'int32'}) \
        # .drop(columns='Unnamed: 0', inplace=True)


def save(baseline_postprocessed: pd.DataFrame, sampled_labeled_output_path: str):
    df_attacks = baseline_postprocessed[baseline_postprocessed.Label == 1]
    df_non_attack = baseline_postprocessed[baseline_postprocessed.Label == 0]
    df_non_attack_sampled = df_non_attack.sample(n=300000, random_state=123)
    df = pd.concat([df_attacks, df_non_attack_sampled])

    df.to_csv(sampled_labeled_output_path, sep=',', index=False)


def get_args():
    """
    Utility method to extract command line arguments used for parametrizing the labeling.
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline_no_label_path', help='Path to the non labeled baseline dataset.')
    parser.add_argument('--attacks_input_path', help='Path to a CSV file containing attacks labeled by MAWI.')
    parser.add_argument('--output_labeled_baseline', help='Desired output path for labeled MAWI baseline dataset.')
    args = parser.parse_args()
    args_dict = vars(args)
    if None in args_dict.values():
        raise Exception("Command line argument missing, please check the documentation.")

    return args_dict['baseline_no_label_path'], args_dict['attacks_input_path'], args_dict['output_labeled_baseline']


baseline_no_label_path, attacks_input_path, output_labeled_baseline = get_args()

df, label_df = get_dataframes(baseline_no_label_path=baseline_no_label_path, attacks_path=attacks_input_path)
attacks_df = merge_attacks_and_non_labeled(df=df, label_df=label_df)

df_no_duplicates = filter_labeled(df=df, attacks_df=attacks_df)

attacks_df = attacks_df[columns_to_select]
baseline = pd.concat([df_no_duplicates, attacks_df], ignore_index=True)

baseline_postprocessed = baseline_postprocessing(baseline=baseline)

save(baseline_postprocessed=baseline_postprocessed, sampled_labeled_output_path=output_labeled_baseline)
