import os
import boto3
import pandas as pd
from datetime import datetime
import logging

# Setup logging
log_dir = '/usr/local/airflow/dags/logs'
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'ingestion.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# AWS setup
s3 = boto3.client('s3')
BUCKET_NAME = 'ecommerce-raw-bucket'

# Folder setup
source_folder = '/usr/local/airflow/dags/data/source/'
raw_folder = '/usr/local/airflow/dags/data/raw/'

def upload_to_s3(file_path, s3_key):
    """Uploads file to S3"""
    try:
        s3.upload_file(file_path, BUCKET_NAME, s3_key)
        logging.info(f"✅ Uploaded {file_path} to S3 as {s3_key}")
        return True
    except Exception as e:
        logging.error(f"❌ Failed to upload {file_path}. Error: {str(e)}")
        return False


def partial_ingest(file_path):
    """Reads 10% of the data first for initial load."""
    try:
        df = pd.read_csv(file_path)
        ten_percent = int(0.1 * len(df))
        if ten_percent == 0:
            logging.warning(f"⚠️ File {file_path} too small for partial ingest.")
            return df
        
        df_10 = df.iloc[:ten_percent]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        partial_file = os.path.join(raw_folder, f"partial_{timestamp}_{os.path.basename(file_path)}")
        df_10.to_csv(partial_file, index=False)
        logging.info(f"📦 Loaded 10% ({ten_percent} rows) of {file_path} to {partial_file}")
        return df
    except Exception as e:
        logging.error(f"❌ Error during partial ingestion of {file_path}: {str(e)}")
        return None


def full_ingest(df, file_path):
    """Loads the full data into the raw folder."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_file = os.path.join(raw_folder, f"{timestamp}_{os.path.basename(file_path)}")
        df.to_csv(full_file, index=False)
        logging.info(f"✅ Fully ingested {file_path} → {full_file}")
        return full_file
    except Exception as e:
        logging.error(f"❌ Error during full ingestion of {file_path}: {str(e)}")
        return None


def main():
    files = [f for f in os.listdir(source_folder) if f.endswith('.csv')]
    
    if not files:
        logging.warning("⚠️ No CSV files found in source folder.")
        return

    for file_name in files:
        file_path = os.path.join(source_folder, file_name)

        # Step 1: Load 10% of data first
        df = partial_ingest(file_path)
        if df is None:
            continue

        # Step 2: Ingest full data to raw
        full_file = full_ingest(df, file_path)
        if full_file:
            # Step 3: Upload to S3
            s3_key = f"raw/{os.path.basename(full_file)}"
            upload_to_s3(full_file, s3_key)


if __name__ == "__main__":
    main()
