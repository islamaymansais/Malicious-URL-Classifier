#------------------------------------------------------------------------------------------------#
#                                            Imports                                             #
#------------------------------------------------------------------------------------------------#

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request, make_response

#------------------------------------------------------------------------------------------------#
#                                     Pre-processing methods                                     #
#------------------------------------------------------------------------------------------------#

def down_sample(raw_df, column_name):
    """
        Down samples the dataset to balance the densities of each target. First, this method begins by
        ingesting the dataframe and name of the target column. Next, the dataset is split into groups 
        based on the target column. The groups are then reduced to the size of the smallest group. Finally,
        the groups are concated together into a single dataframe and returned.

        Args:
            raw_df: raw dataframe 
            column_name: target column name

        Returns:
            sampled_df: downsampled dataframe
    """
    dfs = raw_df.groupby([column_name])
    sampled_df = dfs.apply(lambda x: x.sample(dfs.size().min()))
    sampled_df = sampled_df.reset_index(drop=True)
    return sampled_df

def clean_df(df, column_name, balance=False):
    """
        Cleans dataset and preprocesses it in preparation for ML model ingestion, training testing. This method
        starts off by filling in empty values with zeros. Next, it converts all columns' datatype to numeric as
        some columns' datatype is by default set to objects during ingestion. Next, columns that are all zero are
        removed from the dataset. Finally, the dataset is sampled to balance the targets before being returned.
    """
    balanced=False
    df = df.fillna(0.0)
    df.loc[:, (df.columns != column_name)] = df.loc[:, (df.columns != column_name)].apply(pd.to_numeric)
    # remove all zero columns
    df = df.loc[:, (df != 0).any(axis=0)]
    df.drop_duplicates(subset=None, keep='first', inplace=True)
    if balance==True:
        balanced=True
        df = down_sample(df, column_name)
    return df, balanced