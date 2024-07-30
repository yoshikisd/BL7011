"""
    This file contains a script to read and plot asc data from the photon
    correlation spectroscopy setup at the ALS (i forget which room it's in)

    Authors: Dayne Sasaki
"""

# Import packages
import pandas as pd
from io import StringIO

def main():
    MARKER = '\n\n' # This string occurs between the different data sections
    dir = '/Users/yoshikisd/Documents/ALS-MIT/Data/Tabletop PCS setup/20240528 - Blackbox testing/'
    file = 'With rubber cap on.ASC'
    path = dir + file

    row_start_correlation = None
    row_end_correlation = None
    row_start_counts = None
    row_end_counts = None
    duration = None
    duration_float = None
    runs = None
    temperature = None
    data_correlation = None
    data_count_rate = None
    data_instrument = None

    with open(path,
              mode='r',
              encoding='latin-1') as data_file:
        # Break up text file into sections which different data
        separated_data = (data_file.read()).split(MARKER)
        for idx, data_string in enumerate(separated_data):
            if 'Correlation' in data_string:
                # Remove the string '"Correlation"\n' from data_string
                temp_string = data_string.replace('"Correlation"\n','')

                # Read temp_string as a csv by using StringIO
                data_correlation = pd.read_csv(StringIO(temp_string),
                                               sep='\t',
                                               lineterminator='\n',
                                               usecols=[0,1],
                                               names=['Tau [ms]',
                                                      'Correlation'])
            elif 'Count Rate' in data_string:
                # Remove the string '"Count Rate"\n' from data_string
                temp_string = data_string.replace('"Count Rate"\n', '')

                # Read temp_string as a csv by using StringIO
                data_count_rate = pd.read_csv(StringIO(temp_string),
                                              sep='\t',
                                              lineterminator='\n',
                                              usecols=[0, 1],
                                              names=['Time [ms]',
                                                     'Count rate [kHz]'])

            elif 'ALV-7004/USB-FAST' in data_string:
                # Remove the header string and any spaces
                temp_string = data_string.replace('ALV-7004/USB-FAST\n', '')
                temp_string = temp_string.replace(' ', '')

                # Read temp_string as a csv by using StringIO
                data_instrument = pd.read_csv(StringIO(temp_string),
                                              sep=':\t',
                                              lineterminator='\n',
                                              names=['Parameter', 'Value'])

    pass



if __name__ == '__main__':
    main()