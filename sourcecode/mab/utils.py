import os
import glob
import pandas as pd


def read_partitions(path: str):
    """Reads the data from several equally structured parquet files"""
    for file in glob.glob(path):
        partition = pd.read_parquet(file)
        try:
            df = pd.concat([df, partition], axis=0)
        except:
            df = partition.copy()

    return df


def save_dataframe_to_parquet(df: pd.DataFrame, path):
    """Saves a dataframe to parquet format"""
    df.to_parquet(path, index=False)


def remove_directory_contents(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            remove_directory_contents(file_path)
            os.rmdir(file_path)
