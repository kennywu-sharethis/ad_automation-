import pandas as pd
import os

def split_file(file_path_in: str, directory_output: str, chunk_size: int = 30000):
    chunks = pd.read_csv(file_path_in, chunksize=chunk_size)
    for i, chunk in enumerate(chunks):
        if i == 21:
            break
        chunk.to_csv(os.path.join(directory_output, f'sharethis_domains_{i}.csv'), index=False)

def process_extracted_data(folder_path_in: str, folder_path_out, filename: str):
    data_frames = []
    for file in os.listdir(folder_path_in):
        file_path = os.path.join(folder_path_in, file)
        df = pd.read_csv(file_path, low_memory=False, header=None)
        data_frames.append(df)
    df = pd.concat(data_frames, ignore_index=True)
    filtered_df = df[~df[0].str.contains('<br')]
    col_to_check = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    are_all_empty = df[col_to_check].isnull().all(axis=1)
    filtered_df = filtered_df[~are_all_empty]
    filtered_df.to_csv(os.path.join(folder_path_out, filename), index=False)


