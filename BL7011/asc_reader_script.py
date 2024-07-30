"""
    This file contains a script to read and plot asc data from the photon
    correlation spectroscopy setup at the ALS (i forget which room it's in)

    Authors: Dayne Sasaki
"""

# Import packages
from BL7011 import file_processing as fp

def main():
    dir = '/Users/yoshikisd/Documents/ALS-MIT/Data/Tabletop PCS setup/20240528 - Blackbox testing/'
    file = 'With rubber cap on.ASC'
    path = dir + file

    data_correlation, data_count_rate, data_instrument = fp.read_asc(path)


if __name__ == '__main__':
    main()