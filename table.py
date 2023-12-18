import pandas as pd
import numpy as np
from functions import head_tail_breaks

table_path = r''
output_table_path = r''
col = 'lr'

try:
    df = pd.read_file(table_path)
    if col not in pd.columns:
        raise ValueError(f"Column '{col}' not found in the data.")

    attribute_values = df[col].values

    ht_index, cuts = head_tail_breaks(attribute_values, break_per=0.4)
    print("Cuts:", cuts)

    df['ht_class'] = 0
    for i, threshold in enumerate(cuts):
        df.loc[df[col] > threshold, 'ht_class'] = i + 1

    df.to_file(output_table_path)
    print(f"New table saved to {output_table_path}")

except Exception as e:
    print(f"Error: {e}")
