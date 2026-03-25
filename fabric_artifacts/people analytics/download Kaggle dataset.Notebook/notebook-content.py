# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "b94d792f-0f2a-42b5-81e8-b4582c606795",
# META       "default_lakehouse_name": "people_analytics_lakehouse",
# META       "default_lakehouse_workspace_id": "aca4b91c-3a43-4f0a-b169-85f40788c6e7",
# META       "known_lakehouses": [
# META         {
# META           "id": "b94d792f-0f2a-42b5-81e8-b4582c606795"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Install the Kaggle library
%pip install kaggle

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Kaggle API Credentials
import os
os.environ['KAGGLE_USERNAME'] = 'amigomusa'
os.environ['KAGGLE_KEY'] = 'KGAT_a82661150f9614976194e255b027e20d'
#KAGGLE_API_TOKEN = 'KGAT_a82661150f9614976194e255b027e20d'

# 2. Define the dataset and target path
dataset_path = "pavansubhasht/ibm-hr-analytics-attrition-dataset"
file_name = "WA_Fn-UseC_-HR-Employee-Attrition.csv"
target_path = "/lakehouse/default/Files/raw_uploads"


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Download the dataset
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

def download_and_extract(dataset, file, target):
    try:
        # 1. Initialize and Authenticate
        api = KaggleApi()
        api.authenticate()

        print(f"Starting download from {dataset}...")
        
        # 2. Download the file
        api.dataset_download_file(dataset_path, file, path=target)

        # 3. Check if the file arrived as ZIP
        zip_path = os.path.join(target, f"{file}.zip")

        if os.path.exists(zip_path):
            print(f"Detected ZIP file: {zip_path}. Extracting...")
            with zipfile.ZipFile(zip_path, 'r') as zif_ref:
                zip_ref.extractall(target)

            # Remove the zip file after extraction to save space
            os.remove(zip_path)
            print(f"Extraction complete. ZIP removed.")
        else:
            print("File downloaded directly (not zipped)")

        # Final verification
        final_file_path = os.path.join(target, file)
        if os.path.exists(final_file_path):
            print(f"Success! File is read at: {final_file_path}.")
        else:
            print(f"Error: Could not find {file} in {target} after process.")
    
    except Exception as e:
        if "401" in str(e):
            print("Auth Error: Check your kaggle Username/Key.")
        elif "404" in str(e):
            print("Path Error: Dataset path or filename is incorrect.")
        else:
            print(f"Unexpected Error: {e}")
        

# Run the function
download_and_extract(dataset_path, file_name, target_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
