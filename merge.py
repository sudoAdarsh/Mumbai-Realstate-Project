
import pandas as pd
import glob
import os

# 1. Define the folder where your 4 CSVs are stored
# Make sure this folder contains ONLY these 4 files
DATA_FOLDER = "final_datasets"
output_file = "mumbai_real_estate_dataset.csv"

# 2. Get a list of all CSV files in that folder
all_files = glob.glob(os.path.join(DATA_FOLDER, "*.csv"))

# 3. Read each CSV into a list of DataFrames
df_list = []
for filename in all_files:
    df = pd.read_csv(filename)
    df_list.append(df)
    print(f"Loaded {filename} with {len(df)} rows.")

# 4. Concatenate all data into one DataFrame
master_df = pd.concat(df_list, axis=0, ignore_index=True)

# 5. Final Cleanup (Crucial for a clean open-source dataset)

master_df = master_df.drop_duplicates()  # Remove accidental duplicates
# master_df = master_df.dropna(subset=['Lat', 'Long']) # Remove rows with no location

# 6. Save the master file
master_df.to_csv(output_file, index=False)

print(f"Success! Master dataset saved with {len(master_df)} total rows.")

# 7. Check Merged Dataset
df = pd.read_csv("master_real_estate_dataset.csv")
print(df.info())
print(df.isnull().sum())
print(df.describe())
