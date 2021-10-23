import sys

import numpy as np
import pandas as pd
from pandas import DataFrame

infile = sys.argv[1]
labels_file_path = sys.argv[2]
filecore = infile.split(".")[0]
outfile = filecore + "_labeled"


def read_data(day):
	print(">> Labeling {}".format(day))
	print(">> Loading the data")
	data = pd.read_csv(infile.format(day), sep="\t", quoting=3, quotechar="")
	data['Attack'] = 'Normal'
	data['Label'] = '0'
	return data


def save_data(data: DataFrame, day):
	print(">> Saving {}".format(day))
	data.to_csv("{}.tsv".format(day), index=False, sep='\t', quoting=3)
	print("#"*20)


def label_data(dataDf: DataFrame, labelsDf: DataFrame):
	# TODO join datasets - https://pandas.pydata.org/docs/user_guide/merging.html#database-style-dataframe-or-named-series-joining-merging
	setting_label()


def setting_label(sip, dip, attack):
	
	# print(">> Adding {}".format(attack))

	data['Attack'] = np.where((data['sourceIPAddress'] == sip) &
							  (data['destinationIPAddress'] == dip),
							  attack,
							  data['Attack'])

# here start ######################################################################

print(">> Welcome to the labeling script <<")
###################################################################
data: DataFrame = read_data(infile)
labelsDf = pd.read_csv(labels_file_path)

labeledData: DataFrame = label_data(data, labelsDf)

setting_label(sip="172.16.0.1", dip="192.168.10.50",
	          st=time_fixing(4, 9, 18), et=time_fixing(4, 9, 22),
	          attack="Brute Force:FTP-Patator")

data['Label'] = np.where(data['Attack'] == "Normal", 0, 1)

#save_data(sys.argv[1])
save_data(outfile)
###################################################################
