import os
import boto3
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    filename='logs/ingestion_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# AWS setup
s3 = boto3.client('s3')
BUCKET_NAME = 'ecommerce-raw-bucket'

# Local folder where new CSVs land
landing_zone = 'data/raw/'

def upload_to_s3(file_path, s3_key):
    try:
        s3.upload_file(file_path, BUCKET_NAME, s3_key)
        logging.info(f"✅ Uploaded {file_path} to S3 as {s3_key}")
        return True
    except Exception as e:
        logging.error(f"❌ Failed to upload {file_path}. Error: {str(e)}")
        return False

def main():
    files = [f for f in os.listdir(landing_zone) if f.endswith('.csv')]
    
    if not files:
        logging.warning("⚠️ No CSV files found in landing zone.")
        return

    for file_name in files:
        local_path = os.path.join(landing_zone, file_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        s3_key = f"raw/{timestamp}_{file_name}"
        upload_to_s3(local_path, s3_key)

if __name__ == "__main__":
    main()
