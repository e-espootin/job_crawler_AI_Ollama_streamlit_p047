import pandas as pd
import os


class DataFramePersist:
    def __init__(self, directory):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def save_dataframe(self, df: pd.DataFrame, filename: str):
        filepath = os.path.join(self.directory, filename)
        df = df[df['title'].notna()]
        df.to_csv(filepath, index=False, mode='w')

    def load_dataframes(self, filename: str):
        filepath = os.path.join(self.directory, filename)
        if os.path.exists(filepath):
            return pd.read_csv(filepath)
        elif filename == 'all':
            # concat csv files
            csv_files = [f for f in os.listdir(
                self.directory) if f.endswith('.csv')]
            df_list = [pd.read_csv(os.path.join(self.directory, f))
                       for f in csv_files]
            return pd.concat(df_list, ignore_index=True)
        else:
            raise FileNotFoundError(f"No such file: '{filepath}'")
