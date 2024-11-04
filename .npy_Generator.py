import os
import argparse
import csv
import numpy as np
from sessions_plotter import *

TPS = 60
DELTA_T = 60
MIN_TPS = 50

def export_dataset(dataset, session_name):
    print(f"Exporting dataset for session: {session_name}")
    np.save(session_name, dataset)
    print(dataset.shape)

def traffic_csv_converter(file_path):
    print("Running on " + file_path)
    session_data = {}
    counter = 0

    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            session_name = row[0]
            session_tuple_key = tuple(row[:8])
            length = int(row[7])
            ts = np.array(row[8:8 + length], dtype=float)
            sizes = np.array(row[9 + length:], dtype=int)

            if length > 10:
                for t in range(int(ts[-1] / DELTA_T - TPS / DELTA_T) + 1):
                    mask = ((ts >= t * DELTA_T) & (ts <= (t * DELTA_T + TPS)))
                    ts_mask = ts[mask]
                    sizes_mask = sizes[mask]
                    
                    if len(ts_mask) > 10 and ts_mask[-1] - ts_mask[0] > MIN_TPS:
                        h = session_2d_histogram(ts_mask, sizes_mask)
                        
                        if session_name not in session_data:
                            session_data[session_name] = []
                        session_data[session_name].append([h])
                        
                        counter += 1
                        if counter % 100 == 0:
                            print(counter)

    for session_name, dataset in session_data.items():
        if dataset:
            session_array = np.asarray(dataset)
            export_dataset(session_array, os.path.splitext(session_name)[0])

if __name__ == '__main__':
    input_file_path = r"..."
    traffic_csv_converter(input_file_path)
